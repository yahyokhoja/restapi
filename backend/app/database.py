from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем строку подключения
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL не задан. Проверь .env файл или переменные окружения.")

# Обработка sslmode только если строка подключения содержит 'render'
connect_args = {"sslmode": "require"} if "render" in SQLALCHEMY_DATABASE_URL else {}

# Создание движка SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Создание сессии
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Генератор для получения сессии
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
