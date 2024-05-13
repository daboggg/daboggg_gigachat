from aiogram import F
from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import Bold
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Cancel, Button
from aiogram_dialog.widgets.text import Const, Format
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage, HumanMessage

from bot.core import get_chat
from bot.state_groups import MainDialogSG
from settings import settings
from utils.converter import conv_voice


##################################################################
# Геттеры
##################################################################

async def getter_start(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data['messages'] = []
    chat = get_chat(credentials=settings.sber.sber_auth, verify_ssl_certs=False)
    dialog_manager.dialog_data['chat'] = chat
    return {}


async def getter_text(dialog_manager: DialogManager, **kwargs):
    messages: list = dialog_manager.dialog_data.get('messages')
    chat: GigaChat = dialog_manager.dialog_data.get('chat')

    if messages:
        result = chat.invoke(messages)
        messages.append(result)
    return {'message': messages[-1].content if messages else ''}


##################################################################
# Хэндлеры
##################################################################


async def role_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        if message.text:
            text = message.text
        else:
            text = await conv_voice(message, message.bot)
        messages: list = manager.dialog_data.get('messages')
        messages.append(SystemMessage(content=text))
        await manager.switch_to(MainDialogSG.dialog)
    except Exception as e:
        print(e)
        await manager.switch_to(MainDialogSG.get_role)


async def text_handler(message: Message, message_input: MessageInput, manager: DialogManager) -> None:
    manager.show_mode = ShowMode.DELETE_AND_SEND
    try:
        if message.text:
            text = message.text
        else:
            text = await conv_voice(message, message.bot)
        messages: list = manager.dialog_data.get('messages')
        messages.append(HumanMessage(content=text))
        await manager.switch_to(MainDialogSG.dialog)
    except Exception as e:
        print(e)
        await manager.switch_to(MainDialogSG.dialog)


async def on_click_cancel(cq: CallbackQuery,
                          button: Button,
                          dialog_manager: DialogManager):
    await cq.message.edit_text("Диалог закончен, чтобы начать новый нажмите menu -> /start")


##################################################################
# Диалог
##################################################################

main_dialog = Dialog(
    Window(
        Const(Bold("До начала диалога вы можете задать роль ИИ, или нажмите начать").as_html()),
        SwitchTo(Const("Задать роль ИИ"), state=MainDialogSG.get_role, id='get_role'),
        SwitchTo(Const("Начать диалог"), state=MainDialogSG.dialog, id='dialog'),

        state=MainDialogSG.start,
        getter=getter_start,
    ),
    Window(
        Const("Введите роль ИИ"),
        MessageInput(
            role_handler,
            content_types=[ContentType.TEXT, ContentType.VOICE]
        ),
        state=MainDialogSG.get_role
    ),
    Window(
        Format(text="{message}"),
        Const("==|==|==|==|==", when=F['message']),
        Const("Введите текст или закройте диалог👇"),
        MessageInput(
            text_handler,
            content_types=[ContentType.TEXT, ContentType.VOICE]
        ),
        Cancel(text=Const('закрыть диалог'), on_click=on_click_cancel),
        getter=getter_text,
        state=MainDialogSG.dialog
    ),
)
