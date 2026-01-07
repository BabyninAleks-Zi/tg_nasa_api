import os
import telegram
from dotenv import load_dotenv


load_dotenv()
tg_token = os.environ['TG_TOKEN']

bot = telegram.Bot(token=tg_token)
updates = bot.get_updates()
bot.send_message(text='Привет всем!', chat_id='@incredible_space')


# print(bot.get_me())
# print(updates[0])