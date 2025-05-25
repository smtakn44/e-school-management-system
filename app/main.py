from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
import os
from typing import Optional

from .database import db
from .routes import auth, student, teacher, admin, general

app = FastAPI(title="E-School Management System")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(student.router, prefix="/student", tags=["student"])
app.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(general.router, tags=["general"])

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown"""
    db.disconnect()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - redirect to login if not authenticated"""
    user = request.session.get('user')
    if user:
        user_type = user.get('user_type')
        if user_type == 'student':
            return RedirectResponse("/student/dashboard")
        elif user_type == 'teacher':
            return RedirectResponse("/teacher/dashboard")
        elif user_type == 'admin':
            return RedirectResponse("/admin/dashboard")
    
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)