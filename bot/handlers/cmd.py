from aiogram import Router
from aiogram.filters import CommandStart
from aiogram_dialog import DialogManager, StartMode

from bot.state_groups import MainDialogSG

cmd_router = Router()


@cmd_router.message(CommandStart())
async def settings_reminders(_, dialog_manager: DialogManager) -> None:
    await dialog_manager.start(MainDialogSG.start, mode=StartMode.RESET_STACK)
