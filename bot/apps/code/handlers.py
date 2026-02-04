import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.enums import ParseMode


import bot.core.keyboards as keyboards_core
import bot.core.api as api
from bot.apps.code import keyboards as keyboards_code
from bot.apps.code.state_fms import *

from bot.database.repository import UserRepository

import config.settings  
router = Router()


@router.message(Command("code"))
async def code(message: Message, state: FSMContext, session: AsyncSession):
    if config.settings.spot:
        return
    repo = UserRepository(session)
    if await repo.is_user_block(message.from_user.id):
        await message.answer("Вы заблокированны")
        return
    
    await state.set_state(Code.set_mail_data)
    await message.answer("Отправьте аккаунт в формате login:pass")


@router.message(Code.set_mail_data)
async def code(message: Message, state: FSMContext, session: AsyncSession):
    repo = UserRepository(session)
    try:
        if await repo.is_user_block(message.from_user.id):
            await message.answer("Вы заблокированны")
            return
        text = message.text
        result = text.replace(" ", "")
        login, password = result.split(":")

        if not await repo.is_mail(login=login,password=password):
            await message.answer("Почта не найдена,попорбуйте еще раз ч")
            await state.clear()
            return 
        await message.answer("Ищу код 60 секунд")
        if  await repo.get_type_mail(login=login,password=password) == "firstmail":

            codes,is_time =  api.request_humaniml(login=login,password=password)
            if is_time == False:
                await message.answer("не нашел код, попробуйте отправить снова")
                return
            code = codes[-1]
        
        else:
            for i in range(0, 5):
                codes, is_time = await api.request_notletters(login=login, password=password)
                
                if is_time == True:
                    code = codes[0]
                    break  # Пропускаем остаток итерации, если is_time == True
                
                # Если is_time != True, продолжаем выполнение
                await asyncio.sleep(5)
            else:
                # Этот блок выполнится ТОЛЬКО если цикл завершился НЕ через break
                await message.answer("не нашел код, попробуйте отправить снова")
                return
                    
        if codes == []:
            await message.answer("На почте нет писем")
            return 
        # text = result = ', '.join(str(code) for code in codes)

        await message.answer(f"Ваш код: <code>{code}</code>",parse_mode=ParseMode.HTML)
        await state.clear()
        
        
    except BaseException as e:
        await state.clear()

