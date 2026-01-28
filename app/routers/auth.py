from fastapi import APIRouter, Depends, Request, Form, status, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..utils import verify_password, get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Dependency to get current user
def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    # Set session
    request.session["user_id"] = user.id
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check if user exists
    if db.query(User).filter((User.username == username) | (User.email == email)).first():
         return templates.TemplateResponse("register.html", {"request": request, "error": "Username or Email already exists"})
    
    new_user = User(username=username, email=email, password_hash=get_password_hash(password))
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
