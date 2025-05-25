from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import get_teacher_lectures, get_lecture_students, update_student_grade
from .auth import require_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def teacher_dashboard(request: Request):
    """Teacher dashboard"""
    user = require_auth(request, 'teacher')
    
    lectures = get_teacher_lectures(user['user_id'])
    
    return templates.TemplateResponse(
        "teacher/dashboard.html",
        {
            "request": request,
            "user": user,
            "lectures": lectures
        }
    )

@router.get("/lectures", response_class=HTMLResponse)
async def teacher_lectures(request: Request):
    """Teacher lectures page"""
    user = require_auth(request, 'teacher')
    
    lectures = get_teacher_lectures(user['user_id'])
    
    return templates.TemplateResponse(
        "teacher/lectures.html",
        {
            "request": request,
            "user": user,
            "lectures": lectures
        }
    )

@router.get("/lecture/{lecture_id}/students", response_class=HTMLResponse)
async def lecture_students(request: Request, lecture_id: int):
    """View students in a lecture"""
    user = require_auth(request, 'teacher')
    
    # Verify teacher teaches this lecture
    teacher_lectures = get_teacher_lectures(user['user_id'])
    if not any(l['lecture_id'] == lecture_id for l in teacher_lectures):
        return RedirectResponse("/teacher/dashboard")
    
    students = get_lecture_students(lecture_id)
    lecture_info = next((l for l in teacher_lectures if l['lecture_id'] == lecture_id), None)
    
    return templates.TemplateResponse(
        "teacher/students.html",
        {
            "request": request,
            "user": user,
            "students": students,
            "lecture_info": lecture_info
        }
    )

@router.post("/update_grade")
async def update_grade(
    request: Request,
    student_id: int = Form(...),
    lecture_id: int = Form(...),
    grade: float = Form(...)
):
    """Update student grade"""
    user = require_auth(request, 'teacher')
    
    # Verify teacher teaches this lecture
    teacher_lectures = get_teacher_lectures(user['user_id'])
    if not any(l['lecture_id'] == lecture_id for l in teacher_lectures):
        return RedirectResponse("/teacher/dashboard")
    
    success = update_student_grade(student_id, lecture_id, grade)
    
    return RedirectResponse(f"/teacher/lecture/{lecture_id}/students", status_code=302)