from passlib.context import CryptContext

from app.database.database import SessionDep
from app.database.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password):
    return pwd_context.hash(password)

async def validate_password(password: str, confirm_password: str)-> bool:
    if password != confirm_password:
        return False
    return True


async def get_user_by_username(username: str, session: SessionDep)-> None | User:
    return session.query(User).filter(User.username == username).first()