from sqladmin import ModelView
from bot.database.models import User, Firstmail # <-- твоя модель

class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.telegram_id]
    column_telegram_id= [User.telegram_id]


class MailFirstmail(ModelView, model=Firstmail):
    # Правильно указываем столбцы для списка
    column_list = [Firstmail.id, Firstmail.login, Firstmail.password]
    
    # Настраиваем поля для поиска
    column_searchable_list = [Firstmail.login]
    
    # Настраиваем сортировку
    column_sortable_list = [Firstmail.id, Firstmail.login]
    
