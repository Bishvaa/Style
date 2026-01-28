from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Item
from .auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    
    # Stats
    total_items = db.query(Item).filter(Item.user_id == current_user.id).count()
    # For now, outfits generated is 0 as we don't store them yet
    outfits_generated = 0 
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": current_user,
        "total_items": total_items,
        "outfits_generated": outfits_generated
    })
