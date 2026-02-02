from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import User, Mail,BlockUser

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
        query = select(Mail).where(
            Mail.login == login,
            Mail.password == password
        )
        
        # Выполняем запрос
        result = await self.session.execute(query)
        mail = result.scalar_one_or_none()
        
        # Если запись найдена и пароль совпадает
        return mail is not None
    
    async def get_type_mail(self,login:str, password:str):
        query = select(Mail.name_mail).where(
        Mail.login == login,
        Mail.password == password
        )
        
        # Выполняем запрос
        result = await self.session.execute(query)
        mail_type = result.scalar_one_or_none()
        
        return mail_type
    
    async def is_user_block(self,id:int) -> bool:
        query = select(BlockUser).where(
        BlockUser.telegram_id == id
    )
    
        # Выполняем запрос
        result = await self.session.execute(query)
        blocked_user = result.scalar_one_or_none()
        
        # Если найдена запись - пользователь заблокирован
        return blocked_user is not None