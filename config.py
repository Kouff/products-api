import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.environ.get('SECRET')

DB_CONNECT: str = os.environ.get('DB_CONNECT')
DB_USER: str = os.environ.get('DB_USER')
DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
DB_ADDRESS: str = os.environ.get('DB_ADDRESS')
DB_PORT: str = os.environ.get('DB_PORT')
DB_NAME: str = os.environ.get('DB_NAME')

DB_URL: str = f'{DB_CONNECT}://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'
