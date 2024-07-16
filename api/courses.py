from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.db_setup import get_db
from pydantic_schemas.course import Course, CourseCreate
from api.utils.courses import get_course, get_courses, create_course

router = APIRouter()


@router.get('/course', response_model=List[Course])
async def read_courses(db: Session = Depends(get_db)):
    courses = get_courses(db)
    return courses


@router.post('/courses', response_model=Course)
async def create_new_course(course: CourseCreate, db: Session = Depends(get_db)):
    return create_course(db, course)


@router.get('/courses/{id}')
async def read_course(id: int, db: Session = Depends(get_db)):
    db_course = get_course(db=db, id=id)
    if db_course is None:
        raise HTTPException(status_code=404, detail='Course not found')
    return db_course


@router.patch('/courses/{id}')
async def update_course():
    return {
        'courses': []
    }


@router.delete('/courses/{id}')
async def delete_course():
    return {
        'course': []
    }
