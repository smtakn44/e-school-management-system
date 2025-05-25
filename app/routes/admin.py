from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import (
    get_all_students, get_all_teachers, get_all_departments, get_all_lectures,
    add_student, add_teacher, add_department, delete_department
)
from .auth import require_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard"""
    user = require_auth(request, 'admin')
    
    students_count = len(get_all_students())
    teachers_count = len(get_all_teachers())
    departments_count = len(get_all_departments())
    lectures_count = len(get_all_lectures())
    
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "user": user,
            "stats": {
                "students": students_count,
                "teachers": teachers_count,
                "departments": departments_count,
                "lectures": lectures_count
            }
        }
    )

@router.get("/students", response_class=HTMLResponse)
async def admin_students(request: Request):
    """Manage students"""
    user = require_auth(request, 'admin')
    
    students = get_all_students()
    departments = get_all_departments()
    
    return templates.TemplateResponse(
        "admin/students.html",
        {
            "request": request,
            "user": user,
            "students": students,
            "departments": departments
        }
    )

@router.post("/students/add")
async def add_student_route(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    department_id: int = Form(...)
):
    """Add new student"""
    user = require_auth(request, 'admin')
    
    success = add_student(username, password, department_id)
    return RedirectResponse("/admin/students", status_code=302)

@router.get("/teachers", response_class=HTMLResponse)
async def admin_teachers(request: Request):
    """Manage teachers"""
    user = require_auth(request, 'admin')
    
    teachers = get_all_teachers()
    
    return templates.TemplateResponse(
        "admin/teachers.html",
        {
            "request": request,
            "user": user,
            "teachers": teachers
        }
    )

@router.post("/teachers/add")
async def add_teacher_route(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    office_hour: str = Form(...),
    office_no: str = Form(...)
):
    """Add new teacher"""
    user = require_auth(request, 'admin')
    
    success = add_teacher(username, password, office_hour, office_no)
    return RedirectResponse("/admin/teachers", status_code=302)

@router.get("/departments", response_class=HTMLResponse)
async def admin_departments(request: Request):
    """Manage departments"""
    user = require_auth(request, 'admin')
    
    departments = get_all_departments()
    
    return templates.TemplateResponse(
        "admin/departments.html",
        {
            "request": request,
            "user": user,
            "departments": departments
        }
    )

@router.post("/departments/add")
async def add_department_route(
    request: Request,
    department_name: str = Form(...)
):
    """Add new department"""
    user = require_auth(request, 'admin')
    success = add_department(department_name)
    return RedirectResponse("/admin/departments", status_code=302)

@router.post("/departments/delete/{department_id}")
async def delete_department_route(
    request: Request,
    department_id: int
):
    user = require_auth(request, 'admin')
    delete_department(department_id)
    return RedirectResponse("/admin/departments", status_code=302)