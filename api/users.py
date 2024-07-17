from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from api.utils.users import get_user, get_user_by_email, create_user, get_users, get_user_async
from db.db_setup import get_db
from db.async_db_setup import async_get_db
from pydantic_schemas.user import UserCreate, User
from pydantic_schemas.course import Course
from api.utils.courses import get_user_courses

router = APIRouter()


@router.get('/users', response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get('/users/async/{id}', response_model=User)
async def read_user_async(id: int, db: AsyncSession = Depends(async_get_db)):
    db_user = await get_user_async(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post('/users', response_model=User, status_code=201)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")

    return create_user(db=db, user=user)


@router.get('/users/{id}/courses', response_model=List[Course])
async def read_user_coureses(id: int, db: Session = Depends(get_db)):
    courses = get_user_courses(db=db, user_id=id)
    return courses


@router.get('/users/{id}/courses', response_model=List[Course])
async def read_user_courses(id: int, db: Session = Depends(get_db)):
    courses = get_user_courses(db=db, user_id=id)
    return courses
