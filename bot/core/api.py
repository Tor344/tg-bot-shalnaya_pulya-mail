import json
import re

import requests


def  request_humaniml(login:str, password:str) -> list|None:
    try:
        API_KEY = '8jhmLxCs28q-g4Zxx-e5xgz0kvU-RLL3sf2S6wAMGAzQhhM317HOT5ouTsNUYaQP'
        
        headers = {
            "X-API-KEY": API_KEY
        }

        json ={
            "email": login,
            "password": password,
            "limit": 10,
        
            "folder": "INBOX"
            }
        MAIN_URL = "https://firstmail.ltd/api/v1/"
        request = requests.post(url=MAIN_URL + "email/messages/latest",headers=headers, json=json)
        print(request.text)

        result = []
        if request.status_code != 200:
            print(request.status_code)
            return None
        
        request_json = request.json()
        messages = request_json.get("data").get("messages")
        
        pattern = r":\s*\d{4,6}\s*"
        
        for message in messages:
            text = message.get("body_text")
            # print(text)
            match = re.search(r'\b\d{4,8}\b', text)

            if match:
                code = match.group()
                result.append(code)
        return result
    
    except BaseException as e:
        return None


def request_notletters(login:str, password:str) -> list|None: 
    try:
        API_KEY = "jSroFXlfpeqCflxKjGVVb4dYZmjzdhRx"

        headers = {
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        }

        json = {
            "email": login,
            "password": password,
            }
        
        MAIN_URL = "https://api.notletters.com/v1/"

        request = requests.post(url=MAIN_URL + "letters",headers=headers, json=json)
        print(request.status_code)
        request_json = request.json()
        
        result = []
        letters = request_json.get("data").get("letters") 
        pattern = r":\s*\d{4,6}\s*"
        for letter in letters:
            text = letter.get("letter").get("text")
            
            match = re.search(r'\b\d{4,8}\b', text)

            if match:
                code = match.group()
                result.append(code)
        return result
    except BaseException as e:
        return None

if __name__ == "__main__":
    print(request_notletters("burrell16516@tiebreakermail.ru", 'JEimH2oSLVhx'))
        # harrietroth2006@parietosplml.ru:rjzqzfovS!6749
        #burrell16516@tiebreakermail.ru:JEimH2oSLVhx