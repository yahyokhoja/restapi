# init_db.py

from database import Base, engine
from models import User, Post

def init_database():
    confirm = input("⚠️ Это удалит ВСЕ таблицы и данные в базе. Продолжить? (yes/no): ")
    if confirm.lower() != "yes":
        print("Операция отменена.")
        return

    print("Удаление существующих таблиц...")
    Base.metadata.drop_all(bind=engine)
    print("Создание новых таблиц...")
    Base.metadata.create_all(bind=engine)
    print("✅ База данных успешно инициализирована.")

if __name__ == "__main__":
    init_database()
