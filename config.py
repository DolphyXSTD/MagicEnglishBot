import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
db_name = os.getenv('DATABASE_NAME')

ENGLISH_LEVELS = ['A1','A2','B1','B2','C1','C2']