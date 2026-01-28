from fastapi import APIRouter, Depends, Request, UploadFile, File, Form, status
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Item, User
from .auth import get_current_user
from ..utils import detect_dominant_color
import shutil
import os
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads"
# Ensure simple check, though mkdir command should handle it
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.get("/wardrobe", response_class=HTMLResponse)
def get_wardrobe(request: Request, category: str = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    
    query = db.query(Item).filter(Item.user_id == current_user.id)
    if category and category != "All":
        query = query.filter(Item.category == category)
    
    items = query.all()
    
    return templates.TemplateResponse("wardrobe.html", {
        "request": request,
        "items": items,
        "user": current_user,
        "current_category": category or "All"
    })

@router.get("/wardrobe/upload", response_class=HTMLResponse)
def upload_page(request: Request, category: str = None, current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("upload.html", {"request": request, "user": current_user, "prefilled_category": category})

from typing import List

@router.post("/wardrobe/upload")
async def upload_item(
    request: Request,
    files: List[UploadFile] = File(...),
    category: str = Form(...),
    occasion: str = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login")
    
    for file in files:
        # Generate unique filename
        file_extension = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        file_location = f"{UPLOAD_DIR}/{filename}"
        
        # Save file
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Process Background (Remove it)
        try:
            from ..bg_remover import process_image_background
            # Create a temp output path or overwrite
            # We will overwrite for simplicity but usually safer to create new
            # Let's overwrite to save space and keep filename simple
            if process_image_background(file_location, file_location):
                print(f"Background removed for {filename}")
        except Exception as e:
            print(f"Background removal failed (or module not ready): {e}")

            
        # Detect Color
        color = detect_dominant_color(file_location)
        
        # Save to DB
        new_item = Item(
            user_id=current_user.id,
            image_filename=filename,
            category=category,
            color=color,
            occasion=occasion
        )
        db.add(new_item)
    
    db.commit()
    
    return RedirectResponse(url="/wardrobe", status_code=status.HTTP_302_FOUND)


@router.post("/wardrobe/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    
    item = db.query(Item).filter(Item.id == item_id, Item.user_id == current_user.id).first()
    if item:
        # Delete file
        file_path = f"{UPLOAD_DIR}/{item.image_filename}"
        if os.path.exists(file_path):
            os.remove(file_path)
            
        db.delete(item)
        db.commit()
        
    return RedirectResponse(url="/wardrobe", status_code=status.HTTP_302_FOUND)
