from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.db.session import get_db
from app.models import User
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "Viewer"

@router.post("/register", status_code=201)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=user_in.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered securely", "user_id": new_user.id}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find user by username (Note: OAuth2 uses 'username' field)
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # 2. Check password
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    
    user_role = user.role.value if hasattr(user.role, 'value') else str(user.role)
    
    access_token = create_access_token(
        data={"sub": user.username, "role": user_role}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}