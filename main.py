import os
import sqlalchemy
from pyrogram import Client, filters
from pyrogram.types import User
import langchainEvent as langKP
import helpForSellAgent as helper
import agentCheckMsg
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import sessionmaker
import threading
import vars


lock = threading.Lock()

current_directory = os.getcwd()
database_name = 'clients.db'
engine = create_engine("sqlite:///"+database_name, echo=True)
Base = sqlalchemy.orm.declarative_base()

class Clientik(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    telegram_id = Column(Integer)
    send_kp = Column(Boolean)
    deal_completed = Column(Boolean)
    messages = Column(Text)
    bot_responses = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

#variables
api_id = vars.api_id
api_hash = vars.api_hash

app = Client('bot2', api_id=api_id, api_hash=api_hash)

with open("product.txt", "r", encoding="utf-8") as file:
    products = file.readlines()
"-1297327410""Мега Драйв Маркетплейс. Спецтехника. Легковые авто."


@app.on_message(filters.chat(-1297327410))
async def read_messages(client, message):
    lock.acquire()
    try:
        sender = message.from_user
        message_text = message.text
        user_id = sender.id
        sender_name = sender.first_name
        check_msg = agentCheckMsg.check_client_message(message_text)
        kp_text = langKP.KP_create(check_msg, sender_name)
        client_m = session.query(Clientik).filter_by(telegram_id=user_id).first()
        if client_m is None:
            client_m = Clientik(telegram_id=user_id, name=sender_name, send_kp=True, deal_completed=False, messages='', bot_responses='')
            session.add(client_m)
        await client.send_message(user_id, kp_text["text"]+"\n"+check_msg)
        print("end")
        session.commit()
    finally:
        lock.release()

@app.on_message(filters.private)
async def read_messages(client, message):
    lock.acquire()
    try:
        sender = message.from_user
        message_text = message.text
        user_id = sender.id
        sender_name = sender.first_name
        if message.chat.type.value == 'private':
            client_m = session.query(Clientik).filter_by(telegram_id=user_id).first()
            send_msg = helper.check_client_message(message_text)
            await client.send_message(user_id, send_msg)
            client_m.messages += message_text + '\n'
            session.add(client_m)
            session.commit()
            print("end")
    finally:
        lock.release()


# Запуск клиента Telegram
app.run()
