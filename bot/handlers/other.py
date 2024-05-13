from aiogram import Router
from aiogram.types import Message

other_router = Router()


@other_router.message()
async def other(message: Message):
    await message.answer('чтобы начать новый диалог нажмите menu -> /start')
