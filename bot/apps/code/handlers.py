from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import bot.core.keyboards as keyboards_core
import bot.core.api as api
from bot.apps.code import keyboards as keyboards_code
from bot.apps.code.state_fms import *

from bot.database.repository import UserRepository


router = Router()


@router.message(Command("code"))
async def code(message: Message, state: FSMContext, session: AsyncSession):
    repo = UserRepository(session)
    if await repo.is_user_block(message.from_user.id):
        await message.answer("Вы заблокированны")
        return
    
    await state.set_state(Code.set_mail_data)
    await message.answer("Отправьте аккаунт в формате login или login:pass")


@router.message(Code.set_mail_data)
async def code(message: Message, state: FSMContext, session: AsyncSession):
    repo = UserRepository(session)
    try:
        if await repo.is_user_block(message.from_user.id):
            await message.answer("Вы заблокированны")
            return
        login, password = message.text.split(":")

        if not await repo.is_mail(login=login,password=password):
            await message.answer("Почта не найдена")
            await state.clear()
            return 

        if  await repo.get_type_mail(login=login,password=password) == "firstmail":
            codes = await api.request_humaniml(login=login,password=password)
        else:
            codes = await api.request_notletters(login=login,password=password)

        if codes == None:
            await message.answer("Произошла ошибка")
            await state.clear()
                
        text = result = ', '.join(str(code) for code in codes)

        await message.answer(text)
        await state.clear()
        
    except BaseException as e:
        await message.answer("Неверно введенные данные")

