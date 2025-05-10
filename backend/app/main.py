from fastapi import FastAPI
from app.routers import user, admin, system
from app.routers import user, admin  # Импортируйте из app.routes, если переместили файл
from app import models  # Здесь подключаем модели
from app.database import Base  # Импортируем Base из database.py
from app.database import engine  # Импортируем engine из database.py
# Создаем таблицы (если они еще не существуют)
Base.metadata.create_all(bind=engine)



app = FastAPI()

# Подключаем маршруты
app.include_router(user.router)
app.include_router(admin.router)
app.include_router(system.router)

# Монтируем админку
app.include_router(admin.admin_app)  # Убедитесь, что 'admin_app' существует в admin.py
