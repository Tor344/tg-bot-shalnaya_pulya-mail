from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger,String,Enum
from enum import Enum as PyEnum

from .session import Base


class MailType(PyEnum):
    FIRSTMAIL = "firstmail"
    NOTLETTERS = "notletters"
    
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

class BlockUser(Base):
    __tablename__ = "blockuser"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)

class Mail(Base):
    __tablename__ = "firstmail" 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name_mail: Mapped[MailType] = mapped_column(
        Enum(MailType),
        nullable=False,
        default=MailType.FIRSTMAIL
    )

    login: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255)) 
