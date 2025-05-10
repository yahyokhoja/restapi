from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.auth import verify_token
from app.database import get_db

router = APIRouter(tags=["Admin"])

@router.get("/admin")
async def get_admin_data(db: Session = Depends(get_db), token: str = Depends(verify_token)):
    db_user = db.query(User).filter(User.phone_number == token["sub"]).first()
    if not db_user or not db_user.is_admin:
        raise HTTPException(status_code=403, detail="Вы не администратор")
    return {"message": "Добро пожаловать, админ!"}
# Экспортируйте router (или admin_app, если это объект, который вы хотите использовать)
admin_app = router