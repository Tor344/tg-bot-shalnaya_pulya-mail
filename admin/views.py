from sqladmin import ModelView
from bot.database.models import User, Mail,MailType # <-- твоя модель

    
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.telegram_id]
    column_telegram_id= [User.telegram_id]


class MailAdmin(ModelView, model=Mail):
    column_list = [Mail.id, Mail.name_mail, Mail.login, Mail.password]
    column_searchable_list = [Mail.login]
    column_sortable_list = [Mail.id, Mail.login]
    
    # Форматируем Enum для красивого отображения
    column_formatters = {
        Mail.name_mail: lambda m, a: m.name_mail.value
    }
    
    column_formatters_detail = {
        Mail.name_mail: lambda m, a: m.name_mail.value
    }
    
    # Для удобства в форме можно добавить описание
    form_choices = {
        'name_mail': [
            (MailType.FIRSTMAIL.value, 'First Mail Service'),
            (MailType.NOTLETTERS.value, 'Not Letters Service')
        ]
    }
    
