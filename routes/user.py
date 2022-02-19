from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import schemas
from config import engine, Base
from config.db import SessionLocal
from utils.user import crud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
user_routes = APIRouter()




# Dependency
def get_db():
    print("SessionLocal : ",SessionLocal)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@user_routes.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {'access_token': form_data.username + 'token'}


@user_routes.get("/user/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)) -> schemas.User:
    return crud.get_user_by_id(user_id=user_id,db=db)

@user_routes.get("/user")
def get_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)


@user_routes.post("/user")
def add_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@user_routes.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    db_user = crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User Not Found for the given User Id")
    return crud.delete_user(db=db, user_id=user_id)
