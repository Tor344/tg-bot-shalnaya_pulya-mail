import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

admin_ids = [int(id_str.strip()) for id_str in str(ADMIN_ID).split(',') if id_str.strip()]
spot = 0