import telebot
from telebot import types
import os
from databases import Database
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI

load_dotenv(find_dotenv())

bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))
app = FastAPI()

database_url = os.getenv("DATABASE_URL")
database = Database(database_url)

async def connect_to_database():
    await database.connect()

async def disconnect_from_database():
    await database.disconnect()

chat_id = os.getenv("MY_CHAT_ID")

def check_messages():
    time_threshold = datetime.datetime.now() - datetime.timedelta(hours=24)
    with connect_to_database() as connect:
        cursor = connect.cursor()
        cursor.execute("SELECT text, link FROM messages WHERE date_time >= ?", (time_threshold,))
        rows = cursor.fetchall()
        for row in rows:
            message = row[0]
            link = row[1]
            text_message = f"{message}\n{link}"
            bot.send_message(chat_id=chat_id, text=text_message)
            connect.commit()

@app.on_event("startup")
async def startup_event():
    await connect_to_database()

@app.on_event("shutdown")
async def shutdown_event():
    await disconnect_from_database()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users")
async def get_users():
    query = "SELECT * FROM users"
    return await database.fetch_all(query)

@app.post("/register")
async def register_user(id: int, username: str, table_name: str):
    query = f"INSERT INTO {table_name} VALUES (:id, :username)"
    values = {"id": id, "username": username}
    await database.execute(query, values)
    return {"message": "User registered"}

@bot.message_handler(commands=["start"])
def start_action(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Старт')
    markup.add(button1)
    bot.send_message(message.chat.id,
                     f"Вітаю, {message.from_user.first_name}! Натисніть Старт для реєстрації, як студента",
                     reply_markup=markup)

@bot.message_handler(content_types=["text"])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Старт':
            register_user(message.chat.id, message.chat.first_name, 'groups')
            bot.send_message(message.chat.id, 'Вас зареєстровано!')
        if message.text == '/reg':
            register_user(message.chat.id, message.chat.first_name, 'lectors')
            bot.send_message(message.chat.id, 'Вас зареєстровано, як Ликладача!')

bot.polling(none_stop=True)
