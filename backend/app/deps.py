from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .database import get_db
from .models import User
from .auth import decode_token

bearer = HTTPBearer(auto_error=False)


def current_user(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if creds is None:
        raise HTTPException(401, "Missing token")
    subject = decode_token(creds.credentials)
    if not subject:
        raise HTTPException(401, "Invalid token")
    user = db.query(User).filter(User.email == subject).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user
