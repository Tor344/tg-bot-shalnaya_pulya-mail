import asyncio
import re

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

import bot.core.keyboards as keyboards_core
from bot.apps.start import keyboards as keyboards_satart
from bot.apps.start.state_fms import *

from bot.database.repository import UserRepository
import bot.core.api as api
import config.settings 


router = Router()


@router.message(Command("start"))
async def start(message: Message, session: AsyncSession):
    if config.settings.spot:
        await message.answer("Бот на паузе, попробуйте позже")
        return

    repo = UserRepository(session)
    if await repo.is_user_block(message.from_user.id):
        await message.answer("Вы заблокированны")
        return
    
    user = await repo.get_by_telegram_id(message.from_user.id)
    if not user:
        await repo.create(message.from_user.id)
        print(config.settings.admin_ids)
        print("Как дела ")
        
        for admin in config.settings.admin_ids:
            print(admin)
            await message.bot.send_message(chat_id=admin,text=f"Новый пользователь: @{message.from_user.username}({message.from_user.id})")
    if config.settings.status_mail == 0:
            
        await message.answer("""Привет! Я выдаю коды от YA

Команды:
    /code - получить код""")
    else:
            await message.answer("""Привет! Я выдаю коды от YA
Отправьте почту в формате login:password или login""")


@router.message()
async def code(message: Message, state: FSMContext, session: AsyncSession):
    if config.settings.spot:
        await message.answer("Бот на паузе, попробуйте позже")
        return
    if config.settings.status_mail == 0:
        await message.answer("К сожалению я не смог распознать Вашу команду. Воспользуйтесь /code или отправьте /start")
        return
    
    repo = UserRepository(session)
    await state.clear()
    try:
        if await repo.is_user_block(message.from_user.id):
            await message.answer("Вы заблокированны")
            return
        text = message.text
        
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
        # Находим все совпадения
        login = re.findall(email_pattern, text)
        if login == []:
            await message.answer("Неверный формат аккаунта. Попробуйте еще раз через /code")
            await state.clear()
        if len(re.findall(email_pattern, text)) > 1:
            await message.answer("Ошибка, отправьте 1 аккаунт еще раз через /code")
            return
        
        login = re.findall(email_pattern, text)[0]
        if not await repo.is_mail(login=login):
            await message.answer("Почта не найдена,попорбуйте еще раз через /code")
            await state.clear()
            return 
        password = await repo.get_password_by_login(login=login)
        print(password)
        await message.answer("Ищу код 60 секунд")
        if  await repo.get_type_mail(login=login,password=password) == "firstmail":
            for i in range(0, 12):
                codes,is_time =  api.request_humaniml(login=login,password=password)
                print(codes, is_time)
                if codes == None and is_time ==None:
                    await message.answer("Проблема с сервисом")
                    await state.clear()
                    return
                if is_time == True:
                    code = codes[-1]
                    break  # Пропускаем остаток итерации, если is_time == True
                await asyncio.sleep(5)
                
            else:
                # Этот блок выполнится ТОЛЬКО если цикл завершился НЕ через break
                await message.answer("не нашел код, попробуйте отправить снова")
                return
            
        else:
            for i in range(0, 12):

                codes, is_time = await api.request_notletters(login=login, password=password)
                if is_time == True:
                    code = codes[0]
                    break  # Пропускаем остаток итерации, если is_time == True
                
                # Если is_time != True, продолжаем выполнение
                await asyncio.sleep(5)
            else:
                # Этот блок выполнится ТОЛЬКО если цикл завершился НЕ через break
                await message.answer("не нашел код, попробуйте отправить снова")
                await state.clear()
                return
                    
        if codes == []:
            await message.answer("На почте нет писем")
            return 
        # text = result = ', '.join(str(code) for code in codes)

        await message.answer(f"Ваш код: <code>{code}</code>",parse_mode=ParseMode.HTML)
        await state.clear()
        
        
    except BaseException as e:
        await state.clear()
    
    finally:
        await state.clear()