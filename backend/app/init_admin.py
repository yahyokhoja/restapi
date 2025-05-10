from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils import hash_password

def create_admin():
    db: Session = SessionLocal()
    admin_phone = "9999999999"

    existing_admin = db.query(User).filter(User.phone_number == admin_phone).first()
    if existing_admin:
        print("⚠ Администратор уже существует.")
        return

    admin_user = User(
        name="Admin",
        phone_number=admin_phone,
        password_hash=hash_password("adminpass"),
        is_admin=True
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"✅ Администратор создан: {admin_user.phone_number}")

if __name__ == "__main__":
    create_admin()
