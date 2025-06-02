# Структура квиза
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'Какая команда отвечает за вывод информации на экран?',
        'options': ['for', 'is', 'writeline', 'print'],
        'correct_option': 3
    },
    {
        'question': 'Какой тип лучше всего подходит для выделения уникальных слов в тексте',
        'options': ['кортеж (tuple)', 
                    'список (list)', 
                    'множество (set)', 
                    'словарь (dict)', 
                    ],
        'correct_option': 2
    },
    {
        'question': 'Как вывести список методов и атрибутов объекта Х',
        'options': ['help(x)', 
                    'info(x)', 
                    '?x', 
                    'dir(x)', 
                    ],
        'correct_option': 3
    },
    {
        'question': 'Какая из перечисленных инструкций выполнится быстрее всего, если n = 10**6?',
        'options': ['a = list(i for i in range(n))', 
                    'a = [i for i in range(n)]', 
                    'a = (i for i in range(n))', 
                    'a = {i for i in range(n)}', 
                    ],
        'correct_option': 2
    },
    {
        'question': 'Какой модуль нужно импортировать для работы с регулярными выражениями?',
        'options': ['regex', 're', 'regexp', 'pyre'],
        'correct_option': 1
    },
    {
        'question': 'Какой оператор используется для импорта модуля под другим именем?',
        'options': ['import module as alias', 
                    'import module alias', 
                    'alias module import', 
                    'import alias module', 
                    ],
        'correct_option': 0
    },
    {
        'question': 'Как получить текущую дату и время в Python?',
        'options': ['datetime.now()', 
                    'time.current()', 
                    'datetime.today()', 
                    'Варианты 1 и 3 верны', 
                    ],
        'correct_option': 3
    },
    {
        'question': 'Какой оператор используется для возведения в степень?',
        'options': ['^', '**', 'pow()', 'Варианты 2 и 3 верны'],
        'correct_option': 3
    },
]
