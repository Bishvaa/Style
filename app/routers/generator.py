from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Item, User
from .auth import get_current_user
from ..utils import calculate_compatibility_score, generate_style_explanation
import random

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/generator", response_class=HTMLResponse)
def generator_page(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("generator.html", {"request": request, "user": current_user})

@router.post("/generator", response_class=HTMLResponse)
def generate_outfit(
    request: Request, 
    occasion: str = Form("Any"),
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login")
    
    # Get all items (fallback) and filtered items
    all_items = db.query(Item).filter(Item.user_id == current_user.id).all()
    
    # Filter by occasion if not "Any"
    filtered_items = []
    if occasion and occasion != "Any":
        filtered_items = [i for i in all_items if occasion.lower() in (i.occasion or "").lower()]
    else:
        filtered_items = all_items
        
    # Helper to get items by category with fallback
    def get_items_by_category(category, preferred_list, fallback_list):
        preferred = [i for i in preferred_list if i.category == category]
        if preferred:
            return preferred
        return [i for i in fallback_list if i.category == category]
    
    shirts = get_items_by_category("Shirt", filtered_items, all_items)
    pants = get_items_by_category("Pant", filtered_items, all_items)
    shoes = get_items_by_category("Shoe", filtered_items, all_items)
    
    if not shirts or not pants or not shoes:
        return templates.TemplateResponse("generator.html", {
            "request": request, 
            "user": current_user,
            "error": f"Not enough items found for occasion '{occasion}'! Need at least 1 Shirt, 1 Pant, and 1 Shoe.",
            "occasion_input": occasion
        })
    
    # Collect ALL valid outfits (score > 0)
    valid_outfits = []
    
    # Try 100 combinations
    for _ in range(100):
        shirt = random.choice(shirts)
        pant = random.choice(pants)
        shoe = random.choice(shoes)
        
        score = calculate_compatibility_score(shirt.color, pant.color, shoe.color)
        
        # Only accept "decent" matches (Score >= 1)
        if score > 0:
            valid_outfits.append({
                "shirt": shirt,
                "pant": pant,
                "shoe": shoe,
                "score": score
            })
            
    # Weighted Random Selection
    # High score = Higher chance of being picked, but not guaranteed
    # This ensures "Good" outfits (Score 2) get shown sometimes even if a "Perfect" (Score 5) exists.
    if valid_outfits:
        # Sort by score desc for better weighing logic if needed, but random.choices handles it
        # Weights = Score (Score 5 is 5x more likely than Score 1)
        # Using exponential weight (score^2) to strongly prefer good ones but still allow variety
        weights = [o['score']**2 for o in valid_outfits]
        best_outfit = random.choices(valid_outfits, weights=weights, k=1)[0]
    else:
        best_outfit = None
        
    best_explanation = "" # Explanation removed from UI logic anyway
            
    return templates.TemplateResponse("generator.html", {
        "request": request,
        "user": current_user,
        "outfit": best_outfit,
        "explanation": best_explanation,
        "occasion_input": occasion
    })
