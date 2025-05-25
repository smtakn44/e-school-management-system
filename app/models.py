from pydantic import BaseModel
from typing import Optional
from datetime import date

class LoginForm(BaseModel):
    username: str
    password: str
    user_type: str

class StudentCreate(BaseModel):
    username: str
    password: str
    department_id: int

class TeacherCreate(BaseModel):
    username: str
    password: str
    office_hour: str
    office_no: str

class DepartmentCreate(BaseModel):
    dept_name: str

class GradeUpdate(BaseModel):
    student_id: int
    lecture_id: int
    grade: float

class WarningCreate(BaseModel):
    warning_text: str
    date: Optional[date] = None

class ScheduleCreate(BaseModel):
    schedule_text: str
    date: Optional[date] = None