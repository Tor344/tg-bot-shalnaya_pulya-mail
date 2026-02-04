import aiohttp
import asyncio
import re
from typing import Optional, List
import time
import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.repository import UserRepository
from bot.database.session import *
import html  # Добавляем импорт html модуля
from email.header import decode_header
import requests
import html  # Добавляем импорт html модуля
from email.header import decode_header


def decode_mime_header(header):
    """Декодирует MIME-encoded заголовки (например, subject, from)"""
    if header is None:
        return ""
    
    decoded_parts = decode_header(header)
    result = []
    
    for content, encoding in decoded_parts:
        if isinstance(content, bytes):
            if encoding:
                try:
                    content = content.decode(encoding)
                except:
                    content = content.decode('utf-8', errors='ignore')
            else:
                content = content.decode('utf-8', errors='ignore')
        result.append(content)
    
    return ''.join(result)

def decode_html_text(html_text):
    """Декодирует HTML текст с Unicode escape последовательностями"""
    if not html_text:
        return ""
    
    # Сначала пробуем декодировать Unicode escape (\u0417 и т.д.)
    try:
        decoded = html_text.encode('utf-8').decode('unicode_escape')
    except:
        decoded = html_text
    
    # Если есть MIME encoded части (quoted-printable)
    if '=?utf-8?q?' in decoded or '=?UTF-8?Q?' in decoded or '=?utf-8?b?' in decoded or '=?UTF-8?B?' in decoded:
        try:
            # Декодируем MIME части
            decoded = decode_mime_header(decoded)
        except:
            pass
    
    return decoded

def extract_text_from_html(html_text):
    """Извлекает текст из HTML, убирая теги"""
    if not html_text:
        return ""
    
    # Упрощенное удаление HTML тегов
    text = re.sub(r'<[^>]+>', ' ', html_text)
    # Заменяем множественные пробелы на один
    text = re.sub(r'\s+', ' ', text)
    # Декодируем HTML entities
    text = html.unescape(text)
    return text.strip()


def  request_humaniml(login,password):
    API_KEY = '8jhmLxCs28q-g4Zxx-e5xgz0kvU-RLL3sf2S6wAMGAzQhhM317HOT5ouTsNUYaQP'
    headers = {
        "X-API-KEY": API_KEY,
    }
    # rodneyanderson1976@tracheobronmail.ru:yhanxqowY!1919
    json ={
        "email": login,
        "password": password,
        "folder": "INBOX"
        }
        
    MAIN_URL = "https://firstmail.ltd/api/v1/"
    request = requests.post(url=MAIN_URL + "email/messages/latest",headers=headers, json=json)
    print(request.content.decode('windows-1251', errors='ignore'))

    request_json = request.json()
    print(request.text)
    messages = request_json.get("data").get("messages")
    pattern = r":\s*\d{4,6}\s*"
    result = []
    
    for message in messages:
        text = message.get("body_text", "")
        if not text:
            text = message.get("body_html", "")
        if text:
            # Декодируем текст
            decoded_text = decode_html_text(text)
            
            # Если это HTML, извлекаем текст
            if "<html>" in decoded_text.lower() or "<!doctype" in decoded_text.lower():
                clean_text = extract_text_from_html(decoded_text) 
                # Ищем код в очищенном тексте
                match = re.search(r'\b\d{4,8}\b', clean_text)
            else:
                print(f"\nText content:\n{decoded_text[:1000]}...")
                match = re.search(r'\b\d{4,8}\b', decoded_text)
            
            if match:
                code = match.group()
                print(f"\n✅ Found code: {code}")
                result.append(code)

            else:
                print("\n❌ No code found")
        else:
            print("\nNo text content found")



        # match = re.search(r'\b\d{4,8}\b', s)

        if match:
            code = match.group()
            print(code)
    
    # print(is_time_close(messages[-1].get("date")))
    return result, True#is_time_close(messages[-1].get("date"))

from datetime import datetime, timedelta, timezone

def is_time_close(date_str):
    target_utc = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")

    # переводим в московское время (+4 часа)
    moscow_tz = timezone(timedelta(hours=4))
    target_moscow = target_utc.astimezone(moscow_tz)

    # текущее время в Москве
    now_moscow = datetime.now(moscow_tz)

    # разница в секундах
    diff_seconds = abs((now_moscow - target_moscow).total_seconds())

    return diff_seconds < 60


# # пример использования
# if is_time_close():
#     print("Время совпадает (меньше 60 секунд)")
# else:
#     print("Разница больше минуты")

    

async def request_notletters(login: str, password: str,) :
    try:
        async with SessionMaker() as session:
            repo = UserRepository(session)

            API_KEY = await repo.get_api("notletters")#"jSroFXlfpeqCflxKjGVVb4dYZmjzdhRx"

            headers = {
                'Authorization': f'Bearer {API_KEY}',
                'Content-Type': 'application/json'
            }

            json_data = {
                "email": login,
                "password": password,
            }
            
            MAIN_URL = "https://api.notletters.com/v1/"
            url = MAIN_URL + "letters"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=json_data) as response:
                    print(f"Status code: {response.status}")
                    if response.status != 200:
                        print(f"Request failed with status: {response.status}")
                        return None
                    
                    request_json = await response.json()

                    # Безопасное извлечение данных с проверками
                    data = request_json.get("data")
                    if not data:
                        print("No 'data' field in response")
                        return None
                        
                    letters = data.get("letters")
                    if not letters:
                        print("No letters found in response")
                        return None
                    
                    result = []
                    pattern = re.compile(r'\b\d{4,8}\b')  # Компилируем паттерн для производительности
                    
                    for letter in letters:
                        letter_data = letter.get("letter")
                        if not letter_data:
                            continue
                        
                        text = letter_data.get("text", "")
                        
                        match = pattern.search(text)
                        if match:
                            code = match.group()
                            result.append(code)
                    # timestamp = data['data']['letters'][0]['date']
                    print(is_within_60_seconds(request_json))
                    return result , is_within_60_seconds(request_json)
                    
    except aiohttp.ClientError as e:
        print(f"HTTP client error: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in response data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    





def is_within_60_seconds(timestamp_data):
    """
    Проверяет, прошло ли менее 60 секунд с момента получения времени.
    
    Args:
        timestamp_data: Словарь с данными письма, содержащий timestamp в поле 'date'
        
    Returns:
        bool: True если разница менее 60 секунд, иначе False
    """
    try:
        # Получаем текущее время в формате Unix timestamp
        current_time = time.time()
        
        # Извлекаем timestamp из данных
        # В вашем случае timestamp находится по пути: data -> letters -> [0] -> date
        letter_timestamp = timestamp_data['data']['letters'][0]['date']
        
        # Вычисляем разницу в секундах
        time_difference = abs(current_time - letter_timestamp)
        
        # Проверяем, меньше ли разница 60 секунд
        return time_difference < 180
        
    except (KeyError, IndexError, TypeError) as e:
        print(f"Ошибка при обработке данных: {e}")
        return False


# print(is_recent_letter(json_data))

# if __name__ == "__main__":
#     result = asyncio.run(request_notletters("burrell16516@tiebreakermail.ru", 'JEimH2oSLVhx'))
#     print(result)
#         # harrietroth2006@parietosplml.ru:rjzqzfovS!6749
