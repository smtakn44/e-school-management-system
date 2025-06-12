import httpx
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def student_dashboard(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    lectures = []
    student_info = request.session.get("account", {})
    
    async with httpx.AsyncClient() as client:
        resp_lectures = await client.get(f"http://localhost:8000/api/student/{student_info["account_id"]}/lectures", headers=headers)
        if resp_lectures.status_code == 200:
            lectures = resp_lectures.json().get("model", [])
            
    return templates.TemplateResponse(
        "student/dashboard.html",
        {"request": request, "user": user, "lectures": lectures, "student_info": student_info}
    )

@router.get("/lectures", response_class=HTMLResponse)
async def student_lectures(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    lectures = []
    student_info = request.session.get("account", {})
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://localhost:8000/api/student/{student_info["account_id"]}/lectures", headers=headers)
        if resp.status_code == 200:
            lectures = resp.json().get("model", [])
            
    print(lectures)
            
    return templates.TemplateResponse(
        "student/lectures.html",
        {"request": request, "user": user, "lectures": lectures}
    )