from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram.utils.formatting import Bold
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from langchain_core.messages import SystemMessage, HumanMessage

from bot.core import chat
from bot.state_groups import MainDialogSG
from utils.converter import conv_voice


##################################################################
# Геттеры
##################################################################

async def getter_start(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data['messages'] = []
    return {}


async def getter_text(dialog_manager: DialogManager, **kwargs):
    messages: list = dialog_manager.dialog_data.get('messages')

    print(messages)
    if messages:
        result = chat.invoke(messages)
        print(result)
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
        Const("\nВведите текст"),
        MessageInput(
            text_handler,
            content_types=[ContentType.TEXT, ContentType.VOICE]
        ),
        getter=getter_text,
        state=MainDialogSG.dialog
    ),
)