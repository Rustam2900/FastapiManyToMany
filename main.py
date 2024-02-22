import time
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

import local_log
from database import SessionLocal
from middieware import RateLimitingMiddleware
from schemes import SubjectBase, StudentUpdate, Student
from services import _subject_create, _student_create
from models import Student as StudentModel


app = FastAPI(title="FastapiManyToMany")

app.add_middleware(RateLimitingMiddleware)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    print(request.scope)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    local_log.local_logger.info(f'Time: {process_time}')
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.get("/students/")
async def students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


@app.post('/student-create/')
def student_create(student: Student, db: Session = Depends(get_db)):
    print(student)
    student = _student_create(student, db)
    return student


@app.post('/subject-create/')
def student_create(subject: SubjectBase, db: Session = Depends(get_db)):
    subject = _subject_create(subject, db)
    return subject


@app.put("/student-update/{student_id}")
def update_student(student: StudentUpdate, student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter_by(id=student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    student_data = student.model_dump(exclude_unset=True)
    for key, value in student_data.items():
        setattr(db_student, key, value)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.delete("/student-delete/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}
