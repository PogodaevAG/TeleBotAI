import sys,os
sys.path.append(os.getcwd())

import logging

from aiogram import types, F, Router
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.db import update_quiz_index, get_quiz_index, get_top_ranks, get_user_score
from app.db import get_user_record, update_user_record, update_user_score, update_user_data
from app.questions import quiz_data

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

router = Router()

# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # Создаем сборщика клавиатур типа Reply
    builder = ReplyKeyboardBuilder([
        [types.KeyboardButton(text="Начать новую игру"), types.KeyboardButton(text="Продолжить игру")],
        [types.KeyboardButton(text="Показать рейтинг")],
    ])
    # Прикрепляем кнопки к сообщению
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команды /quiz
@router.message(F.text=="Начать новую игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Давайте начнем квиз!")
    # Запускаем новый квиз
    await new_quiz(message)


# Хэндлер на команды /cont
@router.message(F.text=="Продолжить игру")
@router.message(Command("cont"))
async def cmd_quiz(message: types.Message):
    # Отправляем новое сообщение без кнопок
    await message.answer(f"Продолжаем квиз на том месте, где Вы остановились!")
    #Продолжаем квиз
    await get_question(message, message.from_user.id)


# Хэндлер на команды /ranks
@router.message(F.text=="Показать рейтинг")
@router.message(Command("ranks"))
async def cmd_quiz(message: types.Message):
    # Считываем пользователей и их рекорды из таблицы
    # и выводим ответ пользователю.
    top_ranks = await get_top_ranks()
    answer = 'Рейтинг лучших игроков:\n'
    for index, rank in enumerate(top_ranks):
        answer += f'{index + 1}) {rank[0]} - {rank[1]}\n'
    await message.answer(answer)
 

@router.callback_query(F.data.contains("right_answer"))
async def right_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    # Получение текущего балла для данного пользователя
    user_score = await get_user_score(callback.from_user.id)
    # Получение рекорда для данного пользователя
    user_record = await get_user_record(callback.from_user.id)

    # Отправляем в чат сообщение, что ответ верный
    await callback.message.answer(f'Ваш ответ: "{callback.data.split('#')[1]}" - верно!')

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)
    # Обновление балл текущего пользователя
    user_score += 1
    await update_user_score(callback.from_user.id, user_score)

    # Обновляем рекорд, если он ещё не инициализирован или он меньше текущего балла
    if user_record is None or user_record < user_score:
        await update_user_record(callback.from_user.id, user_score)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


@router.callback_query(F.data.contains("wrong_answer"))
async def wrong_answer(callback: types.CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    # Получение текущего вопроса для данного пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)

    correct_option = quiz_data[current_question_index]['correct_option']

    # Отправляем в чат сообщение об ошибке с указанием верного ответа
    await callback.message.answer(f'Ваш ответ: "{callback.data.split('#')[1]}" - неправильно. Правильный ответ: "{quiz_data[current_question_index]['options'][correct_option]}"')

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(callback.from_user.id, current_question_index)

    # Проверяем достигнут ли конец квиза
    if current_question_index < len(quiz_data):
        # Следующий вопрос
        await get_question(callback.message, callback.from_user.id)
    else:
        # Уведомление об окончании квиза
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")


def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data=("right_answer#" + option) if option == right_answer else ("wrong_answer#" + option))
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()


async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза и балл в 0
    current_question_index = 0
    score = 0
    user_record = await get_user_record(message.from_user.id)
    await update_user_data(message.from_user.id, message.from_user.username, current_question_index, score, user_record)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)


async def get_question(message, user_id):
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

