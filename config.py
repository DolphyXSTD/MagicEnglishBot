import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')
db_name = os.getenv('DATABASE_NAME')