from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from .models import User, Mail,BlockUser,MailType,Api


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
    

    async def is_mail(self,login:str):
        query = select(Mail).where(
            Mail.login == login
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
        
        if mail_type and isinstance(mail_type, MailType):
            return mail_type.value  # Вернет "firstmail" или "notletters"
    
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
    
    
    async def get_count_user(self):
        query = select(func.count()).select_from(User)
    
        # Выполняем запрос
        result = await self.session.execute(query)
        count = result.scalar_one()
        
        return count
    

    async def set_mails_firstmail(self, mails: list[list[str]]) -> int:
        if not mails:
            return 0

        logins = [login for login, _ in mails]

        query = select(Mail.login).where(Mail.login.in_(logins))
        result = await self.session.execute(query)
        existing_logins = set(result.scalars().all())

        new_mails = [
            Mail(
                login=login,
                password=password,
                name_mail=MailType.FIRSTMAIL
            )
            for login, password in mails
            if login not in existing_logins
        ]

        self.session.add_all(new_mails)
        await self.session.commit()

        return len(new_mails)


    async def set_mails_notletters(self, mails: list[list[str]]) -> int:
        if not mails:
            return 0

        logins = [login for login, _ in mails]

        query = select(Mail.login).where(Mail.login.in_(logins))
        result = await self.session.execute(query)
        existing_logins = set(result.scalars().all())

        new_mails = [
            Mail(
                login=login,
                password=password,
                name_mail=MailType.NOTLETTERS
            )
            for login, password in mails
            if login not in existing_logins
        ]

        self.session.add_all(new_mails)
        await self.session.commit()

        return len(new_mails)
    
    async def get_api(self,id:str):
        query = select(Api.api_token).where(Api.id == id)
        result = await self.session.execute(query)
        token = result.scalar_one_or_none()

        return token
    
    async def get_password_by_login(self, login: str) -> str | None:

        # Запрос для получения пароля по логину
        query = select(Mail.password).where(Mail.login == login)
        result = await self.session.execute(query)
        password = result.scalar_one_or_none()
        return password
