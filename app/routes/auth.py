import httpx
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError

router = APIRouter()
templates = Jinja2Templates(directory="templates")

SECRET_KEY = "supersecretkey"  # API ile aynı olmalı
ALGORITHM = "HS256"

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
    print(f"Login attempt: {username}, {user_type}")
    """Process login form"""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "http://localhost:8000/api/auth",
            json={"username": username, "password": password, "account_type": user_type}
        )
        
        if resp.status_code == 200:
            token = resp.json()["token"]
            account = resp.json().get("account", {})
            request.session["token"] = token
            request.session["account"] = account
            # Token'dan kullanıcı bilgilerini al
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                request.session["user"] = {
                    "username": payload.get("username"),
                    "user_type": payload.get("account_type")
                }
            except JWTError:
                request.session["user"] = None
            return RedirectResponse("/", status_code=302)
        else:
            return templates.TemplateResponse(
                "login.html", 
                {"request": request, "error": "Invalid credentials"}
            )


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