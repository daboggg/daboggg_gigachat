from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.formatting import Italic
from aiogram_dialog import DialogManager, StartMode
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage

from bot.state_groups import MainDialogSG
from settings import settings

cmd_router = Router()


# @cmd_router.message(CommandStart())
# async def cmd_start(message: Message) -> None:
#     messages.append(HumanMessage(content='Что-то мне плохо сегодня'))
#     res = chat.invoke(messages)
#     messages.append(res)
#     # print(chat)
#     # print(type(chat))
#
#     await message.answer(res.content)

@cmd_router.message(CommandStart())
async def settings_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainDialogSG.start, mode=StartMode.RESET_STACK)