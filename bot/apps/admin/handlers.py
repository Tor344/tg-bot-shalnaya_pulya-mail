import json
from io import BytesIO

from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession


import bot.core.keyboards as keyboards_core
from bot.apps.admin import keyboards as keyboards_admin
from bot.apps.admin.state_fms import *

from bot.database.repository import UserRepository


import config.settings 
router = Router()


@router.message(Command("admin"))
async def admin(message: Message, session: AsyncSession,state:FSMContext):
    repo = UserRepository(session)
    await state.clear()
    await message.answer("""Админ панель

/count - количество пользователей 
/addmails - отправка файла с почтами
/pause - бот поставлен на пазу
/pauseoff бот снят с паузы               
                         """)


@router.message(Command("pause"))
async def admin(message: Message, session: AsyncSession):
    config.settings.spot = 1
    await message.answer("Бот остановлен")

@router.message(Command("pauseoff"))
async def admin(message: Message, session: AsyncSession):
    config.settings.spot = 0
    await message.answer("Бот запущен")

@router.message(Command("count"))
async def admin(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    await message.answer(f"Количество пользователей: {await repo.get_count_user()}")


@router.message(Command("addmails"))
async def admin(message: Message, session: AsyncSession):
    repo = UserRepository(session)
    await message.answer(f"Выберите вид почты",reply_markup=keyboards_admin.main_name_keyboard)


@router.callback_query(F.data.in_({"firstmail","notletters"}))
async def admin(call: CallbackQuery, session: AsyncSession,state:FSMContext):
    repo = UserRepository(session)
    await state.update_data(name_mail=call.data)
    await state.set_state(Admin.get_file)
    await call.answer("")
    await call.message.answer(f"Пришлите файл с данными почт {call.data } в виде  login:password"
                              ,reply_markup=keyboards_admin.cancel_keyboard)
    

@router.message(F.document, Admin.get_file)
async def admin(
    message: Message,
    session: AsyncSession,
    state: FSMContext
):
    repo = UserRepository(session)
    data = await state.get_data() 
    name_mails = data.get("name_mail")
    document = message.document

    file = await message.bot.get_file(document.file_id)

    # скачиваем файл в память
    buffer = BytesIO()
    await message.bot.download_file(file.file_path, buffer)

    buffer.seek(0)

    result: list[list[str]] = []

    # читаем построчно
    for line in buffer.read().decode("utf-8").splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue

        login, password = line.split(":", 1)
        result.append([login.strip(), password.strip()])

    if name_mails == "firstmail":
        await repo.set_mails_firstmail(result)
    else:
        await repo.set_mails_notletters(result)
    
    await message.answer(
        f"Готово ✅\nАккаунтов: {len(result)}"
    )
    await state.clear()


@router.callback_query(F.data=="cancel")
async def admin(call: CallbackQuery, session: AsyncSession,state:FSMContext):
    repo = UserRepository(session)
    await state.clear()
    await call.message.answer("Добавление почт отменин")
    
