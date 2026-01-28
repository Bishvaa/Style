from passlib.hash import pbkdf2_sha256
from PIL import Image
import colorsys
from collections import Counter

# Password Hashing
# using direct pbkdf2_sha256 to avoid CryptContext loading broken bcrypt backend
def verify_password(plain_password, hashed_password):
    return pbkdf2_sha256.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pbkdf2_sha256.hash(password)


# Color Detection Logic
def get_color_category(h, s, l):
    # h is 0-360, s is 0-100, l is 0-100
    
    # Grayscale Check
    if s < 15:
        if l < 15: return "Black"
        elif l < 35: return "Dark Gray"
        elif l < 65: return "Gray"
        elif l < 85: return "Silver"
        else: return "White"
    
    # Hue Mapping
    # Lightness checks first
    if l < 15: return "Black"
    if l > 93: return "White"
    
    # Ranges
    if 0 <= h < 15:
        return "Red" if l >= 30 else "Maroon"
    elif 15 <= h < 45:
        if l < 40: return "Brown"
        elif l > 75: return "Beige"
        else: return "Orange"
    elif 45 <= h < 70:
        return "Yellow"
    elif 70 <= h < 150:
        return "Green"
    elif 150 <= h < 190:
        return "Teal"
    elif 190 <= h < 260:
        if l < 40: return "Navy"
        elif l > 70: return "Light Blue"
        else: return "Blue"
    elif 260 <= h < 300:
        return "Purple"
    elif 300 <= h < 340:
        return "Pink"
    elif 340 <= h <= 360:
        return "Red"
    
    return "Gray" # Fallback

def detect_dominant_color(image_path_or_file):
    try:
        with Image.open(image_path_or_file) as img:
            img = img.convert("RGBA")
            
            # Resize for performance (slightly larger for better accuracy)
            img = img.resize((150, 150))
            
            pixels = list(img.getdata())
            color_counts = Counter()
            
            for r, g, b, a in pixels:
                # Skip transparent pixels (strict alpha check)
                if a < 10:
                    continue
                    
                # Convert RGB (0-255) to HSL
                h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
                
                # Convert to degrees/percent
                h_deg = h * 360
                s_per = s * 100
                l_per = l * 100
                
                # --- Refined Color Categories ---
                
                # 1. Grayscale (Low Saturation)
                if s_per < 20: # Increased threshold for "gray-ish" items
                    if l_per < 20: category = "Black"
                    elif l_per < 40: category = "Dark Gray"
                    elif l_per < 70: category = "Gray"
                    elif l_per < 90: category = "Silver"
                    else: category = "White"
                
                # 2. Specific Lightness Checks (Overrides Hue)
                elif l_per < 15: category = "Black" # Very dark colors are black
                elif l_per > 95: category = "White" # Very bright colors are white
                
                # 3. Hue Mapping
                elif 0 <= h_deg < 15:
                    category = "Red" if l_per >= 30 else "Maroon"
                elif 15 <= h_deg < 45:
                    if l_per < 40: category = "Brown"
                    elif l_per > 80: category = "Beige" # Strict Beige
                    else: category = "Orange"
                elif 45 <= h_deg < 70:
                    # Olive handling
                    category = "Yellow" if l_per > 40 else "Olive" # Dark yellow is Olive
                elif 70 <= h_deg < 150:
                    if l_per < 30: category = "Dark Green"
                    else: category = "Green"
                elif 150 <= h_deg < 190:
                    category = "Teal" if l_per < 60 else "Cyan"
                elif 190 <= h_deg < 260:
                    if l_per < 35: category = "Navy" # Strict Navy
                    elif l_per > 75: category = "Light Blue"
                    else: category = "Blue"
                elif 260 <= h_deg < 300:
                    if l_per < 30: category = "Dark Purple"
                    else: category = "Purple"
                elif 300 <= h_deg < 340:
                    if l_per > 80: category = "Light Pink"
                    else: category = "Pink"
                else: # 340-360
                    category = "Red"

                color_counts[category] += 1

            
            if not color_counts:
                # If image was fully transparent or empty
                return "Unknown"
                
            # Return most frequent
            return color_counts.most_common(1)[0][0]
            
    except Exception as e:
        print(f"Error detecting color: {e}")
        return "Unknown"

# Outfit Scoring Logic
NEUTRALS = {"Black", "White", "Gray", "Silver", "Beige", "Cream", "Tan"}

COMPLEMENTARY = {
    "Red": {"Green", "Blue", "Black", "White", "Navy"},
    "Blue": {"Orange", "Brown", "White", "Khaki", "Beige", "Gray"},
    "Green": {"Brown", "Yellow", "Black", "White", "Beige"},
    "Yellow": {"Purple", "Navy", "Black", "White", "Gray", "Blue"},
    "Pink": {"Gray", "White", "Navy", "Teal", "Blue", "Black"},
    "Purple": {"Yellow", "White", "Silver", "Gray", "Black"},
    "Orange": {"Blue", "White", "Black", "Gray", "Navy"},
    "Brown": {"Blue", "Green", "White", "Beige"},
    "Navy": {"Khaki", "Beige", "White", "Gray", "Yellow", "Pink", "Red", "Orange"},
    "Maroon": {"Gray", "White", "Beige", "Black", "Navy"},
    "Teal": {"Coral", "Pink", "White", "Black", "Gray", "Navy"},
    "Olive": {"Beige", "Brown", "Navy", "White", "Black"}
}

ANALOGOUS = {
    "Red": {"Pink", "Orange", "Maroon"},
    "Orange": {"Red", "Yellow", "Beige", "Brown"},
    "Yellow": {"Orange", "Green", "Beige", "Cream"},
    "Green": {"Yellow", "Teal", "Olive"},
    "Teal": {"Green", "Blue"},
    "Blue": {"Teal", "Purple", "Navy"},
    "Navy": {"Blue", "Purple", "Black"}, # Navy is dark blue, sits near Black/Purple
    "Purple": {"Blue", "Pink", "Maroon", "Navy"},
    "Pink": {"Red", "Purple", "Maroon"},
    "Brown": {"Beige", "Tan", "Orange", "Olive"},
    "Beige": {"Brown", "Tan", "Cream", "White"},
    "Maroon": {"Red", "Purple", "Brown"}
}

def calculate_compatibility_score(shirt_color, pant_color, shoe_color):
    score = 0
    
    # Weighted Scoring Helper
    def get_match_score(c1, c2):
        # 1. Monochrome (Highest - Elegant & Slimming)
        if c1 == c2 or c1 in c2 or c2 in c1:
             return 3
             
        # 2. Neutrals (Safe & Proper)
        if c1 in NEUTRALS or c2 in NEUTRALS:
            return 2
            
        # 3. Analogous (Harmonious - Next to each other on wheel)
        if (c1 in ANALOGOUS and c2 in ANALOGOUS[c1]) or \
           (c2 in ANALOGOUS and c1 in ANALOGOUS[c2]):
            return 2
            
        # 4. Complementary (Bold - Good contrast but risky)
        if (c1 in COMPLEMENTARY and c2 in COMPLEMENTARY[c1]) or \
           (c2 in COMPLEMENTARY and c1 in COMPLEMENTARY[c2]):
            return 1 
            
        return 0

    # Score: Top vs Bottom
    score += get_match_score(shirt_color, pant_color)
    
    # Score: Shoes vs (Top OR Bottom)
    shoe_match_pant = get_match_score(shoe_color, pant_color)
    shoe_match_shirt = get_match_score(shoe_color, shirt_color)
    score += max(shoe_match_pant, shoe_match_shirt)
    
    # Rule: Sandwich Rule Bonus (Shoe == Top specifically)
    if shoe_color == shirt_color:
        score += 1
        
    # Penalty: Black and Navy interaction (often indistinguishable/clash)
    if ("Black" in (shirt_color, pant_color) and "Navy" in (shirt_color, pant_color)):
        score -= 3 # Punish this specifically to make it very low priority
        
    return score

def generate_style_explanation(shirt_color, pant_color, shoe_color):
    explanations = []
    
    # 1. Neutrals
    if shirt_color in NEUTRALS and pant_color in NEUTRALS:
        explanations.append("A clean, minimal look using neutral tones.")
    elif shirt_color in NEUTRALS or pant_color in NEUTRALS:
        explanations.append(f"The neutral {shirt_color if shirt_color in NEUTRALS else pant_color} balances the {pant_color if shirt_color in NEUTRALS else shirt_color} perfectly.")
        
    # 2. Monochrome
    if shirt_color in pant_color or pant_color in shirt_color:
        explanations.append("A stylish monochromatic combination that elongates the silhouette.")
        
    # 3. Complementary
    if (shirt_color in COMPLEMENTARY and pant_color in COMPLEMENTARY[shirt_color]) or \
       (pant_color in COMPLEMENTARY and shirt_color in COMPLEMENTARY[pant_color]):
        explanations.append(f"High contrast! {shirt_color} and {pant_color} are complementary colors that make each other pop.")
        
    # 4. Sandwich Rule
    if shoe_color == shirt_color:
        explanations.append("The 'Sandwich Rule' is applied here: matching shoes and top creates a cohesive, balanced frame.")
    elif shoe_color in NEUTRALS:
        explanations.append(f"{shoe_color} shoes provide a solid, versatile foundation.")
        
    if not explanations:
        return "A bold, experimental color combination."
        
    return " ".join(explanations)
