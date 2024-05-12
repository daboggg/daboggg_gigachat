from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage

from settings import settings

cmd_router = Router()


chat = GigaChat(credentials=settings.sber.sber_auth, verify_ssl_certs=False)
# chat = GigaChat()
# chat.credentials = settings.sber.sber_auth
# chat.verify_ssl_certs = False

messages = [
    SystemMessage(
        content="Ты эмпатичный бот-психолог, который помогает пользователю решить его проблемы."
    )
]


@cmd_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    messages.append(HumanMessage(content='Что-то мне плохо сегодня'))
    res = chat.invoke(messages)
    messages.append(res)
    # print(chat)
    # print(type(chat))

    await message.answer(res.content)

