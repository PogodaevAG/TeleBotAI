import sys,os
sys.path.append(os.getcwd())

import aiosqlite

DB_PATH = 'app/quiz_bot.db'

async def create_table():
    await execute_query('''CREATE TABLE IF NOT EXISTS quiz_state 
                        (user_id INTEGER PRIMARY KEY, 
                        user_name TEXT,
                        question_index INTEGER, 
                        score INTEGER,
                        record INTEGER
                        )''')


async def update_quiz_index(user_id, index):
    await execute_query('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))


async def update_user_data(user_id, user_name, index, score):
    await execute_query('INSERT OR REPLACE INTO quiz_state (user_id, user_name, question_index, score) VALUES (?, ?, ?, ?)', 
                        (user_id, user_name, index, score))

async def update_user_record(user_id, record):
    await execute_query('UPDATE quiz_state SET record = (?) WHERE user_id = (?)', (record, user_id))

async def get_user_score(user_id):
    return await get_value('SELECT score FROM quiz_state WHERE user_id = (?)', (user_id, ))


async def get_user_record(user_id):
    return await get_value('SELECT record FROM quiz_state WHERE user_id = (?)', (user_id, ))


async def get_quiz_index(user_id):
    return await get_value('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, ))


async def get_top_ranks():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute('SELECT user_name, record FROM quiz_state ORDER BY record DESC') as cursor:
            results = await cursor.fetchall()
            if results is not None:
                return results
            else:
                return []
            

async def execute_query(query, params=None):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(query, params)
        await db.commit()


async def get_value(query, params=None):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(query, params) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0



            

