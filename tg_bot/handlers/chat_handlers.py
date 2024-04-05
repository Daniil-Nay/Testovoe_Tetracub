from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router

r: Router = Router()
@r.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text='Данный бот предназначен для изучения требуемой информации по стране из датасета\n'
             'в рамках тестового задания.\n'
             '/help - помощь по командам'
    )
@r.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer(
        text='/get_info - команда для получения информации о стране\n'
             '/list_countries - список всех доступных стран для изучения\n'

    )