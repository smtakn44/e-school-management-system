import httpx
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def teacher_dashboard(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    lectures = []
    account = request.session.get("account")

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://localhost:8000/api/teacher/{account["account_id"]}/lectures", headers=headers)
        if resp.status_code == 200:
            lectures = resp.json().get("model", [])
            
    return templates.TemplateResponse("teacher/dashboard.html", {"request": request, "user": account, "lectures": lectures})





@router.get("/lectures", response_class=HTMLResponse)
async def teacher_lectures(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    lectures = []
    account = request.session.get("account")
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://localhost:8000/api/teacher/{account["account_id"]}/lectures", headers=headers)
        if resp.status_code == 200:
            lectures = resp.json().get("model", [])
            
    return templates.TemplateResponse("teacher/lectures.html", {"request": request, "user": account, "lectures": lectures})







@router.get("/lecture/{lecture_id}/students", response_class=HTMLResponse)
async def lecture_students(request: Request, lecture_id: int, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    lectures = []
    students = []
    lecture_info = None
    account = request.session.get("account")
    
    
    async with httpx.AsyncClient() as client:
        # Get all lectures for this teacher
        resp_lectures = await client.get(f"http://localhost:8000/api/teacher/{account["account_id"]}/lectures", headers=headers)
        if resp_lectures.status_code == 200:
            lectures = resp_lectures.json().get("model", [])
        # Check if teacher teaches this lecture
        if not any(l.get('lecture_id') == lecture_id for l in lectures):
            return RedirectResponse("/teacher/dashboard")        
        
        # Get students for this lecture
        resp_students = await client.get(f"http://localhost:8000/api/lecture/{lecture_id}/students", headers=headers)
        if resp_students.status_code == 200:
            students = resp_students.json().get("model", [])
        lecture_info = next((l for l in lectures if l.get('lecture_id') == lecture_id), None)
        
        
    return templates.TemplateResponse(
        "teacher/students.html",
        {"request": request, "user": user, "students": students, "lecture_info": lecture_info}
    )






@router.post("/update_grade")
async def update_grade(
        request: Request,
        student_id: int = Form(...),
        lecture_id: int = Form(...),
        grade: float = Form(...),
        user=Depends(get_current_user)
    ):
    
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    account = request.session.get("account")
    lectures = []
    
    # Get all lectures for this teacher
    async with httpx.AsyncClient() as client:
        resp_lectures = await client.get(f"http://localhost:8000/api/teacher/{account["account_id"]}/lectures", headers=headers)
        lectures = resp_lectures.json().get("model", []) if resp_lectures.status_code == 200 else []
        if not any(l.get('lecture_id') == lecture_id for l in lectures):
            return RedirectResponse("/teacher/dashboard")
        # Update grade via API
        await client.put(
            f"http://localhost:8000/api/student/{student_id}/lecture/{lecture_id}/grade",
            headers=headers,
            json={"pass_grade": grade}
        )
        
        
    return RedirectResponse(f"/teacher/lecture/{lecture_id}/students", status_code=302)



