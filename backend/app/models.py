from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем базовый класс для моделей
Base = declarative_base()

# Определяем модель User
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)

# Строка подключения к базе данных (для PostgreSQL, замените на вашу СУБД)
DATABASE_URL = "postgresql://username:password@localhost/dbname"

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создаем сессию для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Автоматическое создание таблиц, если они еще не существуют
Base.metadata.create_all(bind=engine)

# Пример использования сессии для работы с данными
def create_user(db_session, username, email, full_name, hashed_password):
    db_user = User(username=username, email=email, full_name=full_name, hashed_password=hashed_password)
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

# Пример работы с базой данных
if __name__ == "__main__":
    # Открываем сессию
    db = SessionLocal()

    # Создаем пользователя
    create_user(db, username="tuiweyr", email="tyuy@ghjh.py", full_name="jlkj", hashed_password="hashed_password_example")

    # Закрываем сессию
    db.close()
