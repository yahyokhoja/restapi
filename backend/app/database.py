from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Строка подключения к базе данных (из .env файла)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Создание объекта базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"sslmode": "require"} if "render" in SQLALCHEMY_DATABASE_URL else {})

# Создаем сессию
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание Base, который используется для создания всех моделей
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
