from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import authenticate_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Display login page"""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    user_type: str = Form(...)
):
    """Process login form"""
    user = authenticate_user(username, password, user_type)
    
    if not user:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid credentials"}
        )
    
    # Store user in session
    request.session['user'] = user
    
    # Redirect based on user type
    if user_type == 'student':
        return RedirectResponse("/student/dashboard", status_code=302)
    elif user_type == 'teacher':
        return RedirectResponse("/teacher/dashboard", status_code=302)
    elif user_type == 'admin':
        return RedirectResponse("/admin/dashboard", status_code=302)

@router.get("/logout")
async def logout(request: Request):
    """Logout user"""
    request.session.clear()
    return RedirectResponse("/", status_code=302)

def get_current_user(request: Request):
    """Get current user from session"""
    return request.session.get('user')

def require_auth(request: Request, required_type: str = None):
    """Require authentication and optionally specific user type"""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if required_type and user.get('user_type') != required_type:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    return user