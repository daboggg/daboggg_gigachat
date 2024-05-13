from aiogram import Bot
from langchain_community.chat_models import GigaChat

from settings import settings

bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')

chat = GigaChat(credentials=settings.sber.sber_auth, verify_ssl_certs=False)

def get_chat(**kwargs) -> GigaChat:
    return GigaChat(**kwargs)
