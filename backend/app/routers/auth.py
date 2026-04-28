"""CraftWoodAIVision Backend — Auth Router"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import LoginRequest, LoginResponse, UserOut
from app.security import verify_password, create_access_token, decode_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
bearer = HTTPBearer()


def get_username_from_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return payload.get("sub")


@router.post("/login", response_model=LoginResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账户已停用")

    token = create_access_token(data={"sub": user.username, "role": user.role})
    return LoginResponse(
        token=token,
        user=UserOut(
            id=user.id,
            username=user.username,
            name=user.name,
            role=user.role,
            avatar=user.avatar,
        )
    )


@router.get("/me", response_model=UserOut)
def get_me(
    db: Session = Depends(get_db),
    username: str = Depends(get_username_from_token),
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
