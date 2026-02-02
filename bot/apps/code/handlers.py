from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

import bot.core.keyboards as keyboards_core
from bot.apps.code import keyboards as keyboards_code
from bot.apps.code.state_fms import *

from bot.database.repository import UserRepository


router = Router()


@router.message(Command("code"))
async def code(message: Message, state: FSMContext, session: AsyncSession):
    repo = UserRepository(session)
    await state.set_state(Code.set_mail_data)
    await message.answer("Отправьте аккаунт в формате login или login:pass")


@router.message(Code.set_mail_data)
async def code(message: Message, state: FSMContext, session: AsyncSession):
    repo = UserRepository(session)
    login, password = message.text.split(":")
    await message.answer(f"login:{login}, password:{password}")
