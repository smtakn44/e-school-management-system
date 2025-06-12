import httpx
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def schedule_list(request: Request, user=Depends(get_current_user)):
    token = request.session.get("token")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    schedules = []
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8000/api/schedules", headers=headers)
        if resp.status_code == 200:
            schedules = resp.json().get("model", [])
    return templates.TemplateResponse("schedule/list.html", {"request": request, "user": user, "schedules": schedules})
