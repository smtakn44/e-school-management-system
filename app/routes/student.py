from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from ..database import get_student_lectures, get_student_info
from .auth import require_auth

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request):
    """Student dashboard"""
    user = require_auth(request, 'student')
    
    student_info = get_student_info(user['user_id'])
    lectures = get_student_lectures(user['user_id'])
    
    return templates.TemplateResponse(
        "student/dashboard.html",
        {
            "request": request,
            "user": user,
            "student_info": student_info,
            "lectures": lectures
        }
    )

@router.get("/lectures", response_class=HTMLResponse)
async def student_lectures(request: Request):
    """Student lectures page"""
    user = require_auth(request, 'student')
    lectures = get_student_lectures(user['user_id'])
    return templates.TemplateResponse(
        "student/lectures.html",
        {
            "request": request,
            "user": user,
            "lectures": lectures
        }
    )