from pydantic import BaseModel


class StudentBase(BaseModel):
    first_name: str
    last_name: str
    age: int

    class Config:
        orm_mode = True


class SubjectBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class StudentUpdate(StudentBase):
    id: int

    class Config:
        orm_mode = True


class Student(StudentBase):
    subject: list[int] = []

    class Config:
        orm_mode = True


class Subject(SubjectBase):
    students: list[Student] = []

    class Config:
        orm_mode = True


class SubjectShow(SubjectBase):
    id: int

    class Config:
        orm_mode = True
