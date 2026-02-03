import aiohttp
import asyncio
import re
from typing import Optional, List

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from bot.database.repository import UserRepository
from bot.database.session import *

async def request_humaniml(login: str, password: str) -> Optional[List[str]]:
    try:
        async with SessionMaker() as session:
            repo = UserRepository(session)

            API_KEY = '8jhmLxCs28q-g4Zxx-e5xgz0kvU-RLL3sf2S6wAMGAzQhhM317HOT5ouTsNUYaQP'
            
            headers = {
                "X-API-KEY": API_KEY
            }

            json_data = {
                "email": login,
                "password": password,
                "limit": 10,
                "folder": "INBOX"
            }
            
            MAIN_URL = "https://firstmail.ltd/api/v1/"
            url = MAIN_URL + "email/messages"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=json_data) as response:
                    response_text = await response.text()
                    print(response_text)
                    
                    if response.status != 200:
                        print(f"Status code: {response.status}")
                        return None
                    
                    request_json = await response.json()
                    messages = request_json.get("data", {}).get("messages", [])
                    
                    result = []
                    pattern = re.compile(r'\b\d{4,8}\b')
                    
                    for message in messages:
                        text = message.get("body_text", "")
                        match = pattern.search(text)
                        
                        if match:
                            code = match.group()
                            result.append(code)
                            
                    return result if result else None
        
    except aiohttp.ClientError as e:
        print(f"HTTP client error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


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
                    
                    return result if result else None
                    
    except aiohttp.ClientError as e:
        print(f"HTTP client error: {e}")
        return None
    except KeyError as e:
        print(f"Missing key in response data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
if __name__ == "__main__":
    result = asyncio.run(request_notletters("burrell16516@tiebreakermail.ru", 'JEimH2oSLVhx'))
    print(result)
        # harrietroth2006@parietosplml.ru:rjzqzfovS!6749
        #burrell16516@tiebreakermail.ru:JEimH2oSLVhx