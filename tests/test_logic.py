import pytest
from app.utils import get_color_category, calculate_compatibility_score, NEUTRALS, COMPLEMENTARY, ANALOGOUS
import collections

# --- Color Categorization Tests ---
def test_grayscale_detection():
    # H, S, L
    assert get_color_category(0, 0, 0) == "Black"
    assert get_color_category(0, 0, 100) == "White"
    assert get_color_category(0, 0, 50) == "Gray"
    assert get_color_category(0, 10, 96) == "White" # High lightness override

def test_navy_detection():
    # Navy: Hue ~200-240 (Blue), Low Lightness (<40)
    assert get_color_category(220, 50, 20) == "Navy"
    
def test_blue_vs_light_blue():
    # Blue: L=50, Light Blue: L=80
    assert get_color_category(220, 100, 50) == "Blue"
    assert get_color_category(220, 100, 80) == "Light Blue"

def test_beige_detection():
    # Beige: Hue ~30 (Orange/Yellow), High Lightness, Low-Mid Saturation
    assert get_color_category(30, 20, 85) == "Beige"

# --- Scoring Logic Tests ---

def test_monochrome_score():
    # Score 3
    assert calculate_compatibility_score("Blue", "Blue", "Blue") >= 3
    assert calculate_compatibility_score("Dark Blue", "Light Blue", "Blue") >= 3

def test_complementary_score():
    # Score 3 (Weighted match)
    # Blue <-> Orange
    score = calculate_compatibility_score("Blue", "Orange", "White")
    # Blue-Orange = 3 (Comp)
    # Shoe(White) - Pant(Orange) = 1 (Neutral)
    # Total should be at least 3
    assert score >= 3

def test_neutral_score():
    # Score 2
    # Gray + White
    score = calculate_compatibility_score("Gray", "White", "White")
    assert score >= 2

def test_analogous_score():
    # Score 2
    # Red + Pink
    score = calculate_compatibility_score("Red", "Pink", "Red")
    # Red-Pink = 2 (Analogous)
    assert score >= 2

def test_navy_black_clash():
    # Penalty check
    score = calculate_compatibility_score("Navy", "Black", "White")
    # Navy-Black: Both neutral (+1), but penalty (-2)? 
    # Let's check logic:
    # Match: Navy(Neutral) + Black(Neutral) = +1 (Neutral match) 
    # Penalty: -2 
    # Net: -1
    # Plus shoes: White vs Black = +1
    # Total roughly 1 now (2+2-3=1). Should be < 2.
    assert score < 2

# --- Generator / Variety Logic Simulation ---
def test_variety_distribution():
    # Simulate the weighted random choice logic
    import random
    
    # Mock outfits with scores
    mock_outfits = [
        {"id": "perfect", "score": 5},
        {"id": "good", "score": 3},
        {"id": "okay", "score": 2},
        {"id": "bad", "score": 1}
    ]
    
    results = collections.Counter()
    
    # Run 1000 times
    for _ in range(1000):
        # Logic from generator.py
        weights = [o['score']**2 for o in mock_outfits]
        choice = random.choices(mock_outfits, weights=weights, k=1)[0]
        results[choice["id"]] += 1
        
    # Assert distribution properties
    # Perfect should be most common
    assert results["perfect"] > results["good"]
    # Good should be > Okay
    assert results["good"] > results["okay"]
    # But Okay should NOT be zero (variety exists)
    assert results["okay"] > 0
    print(f"\nDistribution (N=1000): {results}")
