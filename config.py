from dotenv import load_dotenv
import os

load_dotenv()


group_id = os.getenv('group_id')
token = str(os.getenv('token'))
ip=os.getenv('ip')
PGUSER=os.getenv('PGUSER')
PGPASSWORD=os.getenv('PGPASSWORD')
DATABASEE=os.getenv('DATABASEE')