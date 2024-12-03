from fastapi import FastAPI, HTTPException, status, APIRouter

from app.database.database import SessionDep
from app.database.models import User
from app.database.security.jwt_users import create_access_token
from app.schema.users import UserIn, Token, Login, UserOut
from app.services.user import UserService
from app.database.security.users import get_user_by_username, get_password_hash, validate_password, verify_password
app = FastAPI()
userService = UserService()
router = APIRouter(
    tags=["Users"],
)


@router.post("/register/")
async def user_register(user_in: UserIn, session: SessionDep)->UserOut:
    error_message = None
    if not await validate_password(password=user_in.password, confirm_password=user_in.password):
        error_message = "Password don not match"
    elif await get_user_by_username(username=user_in.username, session=session):
        error_message = "Username already exists"

    if error_message:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message)

    user_dict = user_in.dict()
    user_dict.pop('confirm_password')
    user_dict["password"] = await  get_password_hash(user_in.password)
    user = User(**user_dict)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.post("/login/")
async def user_login(data: Login,  session: SessionDep):
    user = await get_user_by_username(username=data.username, session=session)
    if not user or not verify_password(plain_password=data.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password incorrect"
        )
    access_token = await create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


