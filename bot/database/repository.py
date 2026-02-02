from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Firstmail

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int) -> User:
        user = User(telegram_id=telegram_id)
        self.session.add(user)
        await self.session.commit()
        return user
    
    async def is_mail(self,login:str, password:str):
        query = select(Firstmail).where(
            Firstmail.login == login,
            Firstmail.password == password
        )
        
        # Выполняем запрос
        result = await self.session.execute(query)
        firstmail = result.scalar_one_or_none()
        
        # Если запись найдена и пароль совпадает
        return firstmail is not None