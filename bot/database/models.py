from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger,String
from .session import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

class Firstmail(Base):
    __tablename__ = "firstmail" 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255)) 
