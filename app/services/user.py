from app.database.models import User, Base
from app.database.database import engine, get_db

class UserService:
    # Baza yaratish (agar mavjud bo'lmasa)
    Base.metadata.create_all(bind=engine)
    db = next(get_db())  # Sessiya yaratish


    # Foydalanuvchi qo'shish
    def create_user(self, username: str, password: str):
        newUser = User(username=username, password=password)
        self.db.add(newUser)
        self.db.commit()
        self.db.refresh(newUser)
        return newUser


    # Foydalanuvchi olish
    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()


    # Foydalanuvchilar ro'yxatini olish
    def get_users(self, page: int = 1, limit: int = 10):
        skip = (page - 1) * limit

        return self.db.query(User).offset(skip).limit(limit).all()

     # Foydalanuvchi ma'lumotlarini yangilash
    def update_user(self, user_id: int, username: str = None):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None  # Foydalanuvchi topilmadi

        if username:
            user.username = username
        self.db.commit()
        self.db.refresh(user)
        return user


    # Foydalanuvchini o'chirish
    def delete_user(self, user_id: int):
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return None  # Foydalanuvchi topilmadi

        self.db.delete(user)
        self.db.commit()
        return user