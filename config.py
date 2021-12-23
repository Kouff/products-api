import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY: str = os.environ.get('SECRET')

DB_CONNECT: str = os.environ.get('DB_CONNECT')
DB_USER: str = os.environ.get('DB_USER')
DB_PASSWORD: str = os.environ.get('DB_PASSWORD')
DB_ADDRESS: str = os.environ.get('DB_ADDRESS')
DB_PORT: str = os.environ.get('DB_PORT')
DB_NAME: str = os.environ.get('DB_NAME')

DB_URL: str = f'{DB_CONNECT}://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'

DEFAULT_UPLOAD_FOLDER: str = os.path.join(BASE_DIR, 'media')
UPLOAD_FOLDER: str = os.environ.get('UPLOAD_FOLDER') or DEFAULT_UPLOAD_FOLDER

ALLOWED_IMAGE_EXTENSIONS = ('png', 'jpg', 'jpeg')
