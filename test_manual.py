from app.utils import detect_dominant_color, calculate_compatibility_score
import os

def test_logic():
    print("--- Starting Manual Logic Verification ---")
    
    # Paths to demo assets
    red_shirt = "demo_assets/red_shirt.png"
    blue_jeans = "demo_assets/blue_jeans.png"
    white_shoes = "demo_assets/white_shoes.png"
    
    # 1. Test Color Detection
    print("\n[1] Testing Color Detection...")
    
    if os.path.exists(red_shirt):
        c1 = detect_dominant_color(red_shirt)
        print(f"Red Shirt detected as: {c1}")
    else:
        print("Red Shirt file not found!")
        c1 = "Red" # Fallback for scoring test

    if os.path.exists(blue_jeans):
        c2 = detect_dominant_color(blue_jeans)
        print(f"Blue Jeans detected as: {c2}")
    else:
        print("Blue Jeans file not found!")
        c2 = "Blue"

    if os.path.exists(white_shoes):
        c3 = detect_dominant_color(white_shoes)
        print(f"White Shoes detected as: {c3}")
    else:
        print("White Shoes file not found!")
        c3 = "White"
        
    # 2. Test Scoring
    print("\n[2] Testing Compatibility Score...")
    print(f"Combination: Top({c1}) + Bottom({c2}) + Shoe({c3})")
    
    score = calculate_compatibility_score(c1, c2, c3)
    print(f"Calculated Score: {score}/3")
    
    print("\n--- Verification Complete ---")

if __name__ == "__main__":
    test_logic()
