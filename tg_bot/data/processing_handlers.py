import json
from typing import Any, Dict

from aiogram.filters import Command
from aiogram.types import Message
from aiogram.dispatcher.router import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from config import load_config

r: Router = Router()
config = load_config()
path_to_data = config.data_path.path


class States(StatesGroup):
    """
    Машина конечных состояний (FSM)
    """
    country_typing = State()
    period_typing = State()


async def fetch_data_from_file(filename: str) -> Dict[str, Any]:
    """
    Для чтения json файла, где хранится информация о странах
    :param filename:
    :return: Dict[str, Any]
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    return {entry['Country_']: entry for entry in data}


@r.message(Command("get_info"))
async def DataProcess_1(message: Message, state: FSMContext) -> None:
    """
    Функция FSM для ловли команды get_info
    :param message:
    :param state:
    :return:
    """
    await message.answer(
        text="Напишите страну для извлечения информации о ней"
    )
    await state.set_state(States.country_typing)


@r.message(States.country_typing)
async def DataProccess_2(message: Message, state: FSMContext) -> None:
    """
    Функция FSM для извлечении информации о стране из текста сообщения
    :param message:
    :param state:
    :return:
    """
    country_data = await fetch_data_from_file(
        path_to_data)
    country = message.text.strip()
    if country in country_data:
        await message.answer(
            text="Успешно! Теперь введите период, который вас интересует"
        )
        await state.update_data(country_info=country_data[country])
        await state.set_state(States.period_typing)

    else:
        await message.answer("Нет информации о данной стране")
        await state.clear()


@r.message(States.period_typing)
async def DataProccess_3(message: Message, state: FSMContext) -> None:
    """
    Функция FSM для получения информации о периоде из текста сообщения
    :param message:
    :param state:
    :return:
    """
    data = (await state.get_data()).get('country_info')
    message_text = message.text.strip().split()

    try:
        start_year, end_year = map(int, message_text)
    except ValueError:
        await message.answer(
            text="Пожалуйста, введите корректный период. \nНапример, 1978 2000."
        )
        return
    available_years = [int(year) for year in data.keys() if year.isdigit()]
    country_info = "\n".join([f"{key}: {value}" for key, value in data.items() if not key.isdigit()])
    if (start_year in available_years and end_year in available_years) and start_year <= end_year:
        filtered_data = {year: data[f"{year}"] for year in range(start_year, end_year + 1)}
        formatted_data = "\n".join([f"{year}: {info}" for year, info in filtered_data.items()])
        await message.answer(
            text=f"<b>Страна:</b>: {data['Country_']}\n"
                 f"<b>Информация об изменения температуры за указанный период:</b>:\n"
                 f"{formatted_data}\n"
                 f"<b>Остальная информация:</b>\n"
                 f"{country_info}",
            parse_mode='HTML'

        )
        await state.clear()
    else:
        await message.answer(
            text="Указан некорректный период. Пример правильного ввода:\n"
                 "1978 2000"
        )


@r.message(Command('list_countries'))
async def get_list(message: Message) -> None:
    """
    Вывод списка всех доступных стран
    :param message:
    :return:
    """
    countries = await fetch_data_from_file(path_to_data)
    countries_list = '\n'.join([f"{i + 1}. {country}" for i, country in enumerate(countries.keys())])
    await message.answer(f"Список стран:\n{countries_list}")
