import httpx
import json
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def administrator_dashboard(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    stats = {"students": 0, "teachers": 0, "departments": 0, "lectures": 0}
    async with httpx.AsyncClient() as client:
        resp_students = await client.get("http://localhost:8000/api/students", headers=headers)
        resp_teachers = await client.get("http://localhost:8000/api/teachers", headers=headers)
        resp_departments = await client.get("http://localhost:8000/api/departments", headers=headers)
        resp_lectures = await client.get("http://localhost:8000/api/lectures", headers=headers)
        if resp_students.status_code == 200:
            stats["students"] = len(resp_students.json().get("model", []))
        if resp_teachers.status_code == 200:
            stats["teachers"] = len(resp_teachers.json().get("model", []))
        if resp_departments.status_code == 200:
            stats["departments"] = len(resp_departments.json().get("model", []))
        if resp_lectures.status_code == 200:
            stats["lectures"] = len(resp_lectures.json().get("model", []))
    return templates.TemplateResponse("administrator/dashboard.html", {"request": request, "user": user, "stats": stats})



@router.get("/students", response_class=HTMLResponse)
async def administrator_students(request: Request, user=Depends(get_current_user)):
    """Manage students"""
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    account = request.session.get("account")
    
    students = []
    departments = []
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://localhost:8000/api/students", headers=headers)
        if resp.status_code == 200:
            students = resp.json().get("model", [])
    
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://localhost:8000/api/departments", headers=headers)
        if resp.status_code == 200:
            departments = resp.json().get("model", [])
    
    return templates.TemplateResponse(
        "administrator/students.html",
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
    student_id: str = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    department_id: int = Form(...)
):
    user = request.session.get("account")
    token = request.session.get("token")
    
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = {
        "student_id": student_id, 
        "username": username,
        "password": password,
        "department_id": department_id
    }
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:8000/api/student", headers=headers, json=data)
    return RedirectResponse("/administrator/students", status_code=302)


@router.get("/teachers", response_class=HTMLResponse)
async def administrator_teachers(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    teachers = []
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/api/teachers", headers=headers)
        if resp.status_code == 200:
            teachers = resp.json().get("model", [])
    return templates.TemplateResponse(
        "administrator/teachers.html",
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
    user = request.session.get("account")
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = {
        "username": username,
        "password": password,
        "office_hour": office_hour,
        "office_no": office_no
    }
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:8000/api/teacher", headers=headers, json=data)
    return RedirectResponse("/administrator/teachers", status_code=302)



@router.get("/departments", response_class=HTMLResponse)
async def administrator_departments(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    departments = []
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/api/departments", headers=headers)
        if resp.status_code == 200:
            departments = resp.json().get("model", [])
    return templates.TemplateResponse(
        "administrator/departments.html",
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
    user = request.session.get("account")
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    data = {"dept_name": department_name}
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:8000/api/department", headers=headers, json=data)
    return RedirectResponse("/administrator/departments", status_code=302)




@router.post("/departments/delete/{department_id}")
async def delete_department_route(
    request: Request,
    department_id: int
):
    user = request.session.get("account")
    token = request.session.get("token")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    } if token else {}

    data = {"department_id": department_id}

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method="DELETE",
            url="http://localhost:8000/api/department",
            headers=headers,
            json=data 
        )

    if response.status_code == 200:
        return RedirectResponse("/administrator/departments", status_code=302)
    else:
        return RedirectResponse("/error", status_code=302)