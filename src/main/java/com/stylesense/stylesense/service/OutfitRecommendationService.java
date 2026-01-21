package com.stylesense.stylesense.service;

import com.stylesense.stylesense.model.WardrobeItem;
import org.springframework.stereotype.Service;

import java.util.Set;

@Service
public class OutfitRecommendationService {

    // 1. Occasion Logic
    public boolean isOccasionMatch(WardrobeItem item, String desiredOccasion) {
        String itemOccasion = item.getOccasion();
        if (itemOccasion == null || itemOccasion.isEmpty())
            return true; // Flexible if not tagged
        return itemOccasion.equalsIgnoreCase(desiredOccasion);
    }

    // 2. Color Matching Engine
    public boolean areColorsCompatible(String color1, String color2) {
        if (color1 == null || color2 == null)
            return true;

        color1 = color1.toLowerCase();
        color2 = color2.toLowerCase();

        // Rule 1: Neutrals match everything
        if (isNeutral(color1) || isNeutral(color2))
            return true;

        // Rule 2: Monochrome (Same color family)
        if (areSameFamily(color1, color2))
            return true;

        // Rule 3: Complementary / Good Combinations
        return checkComplementary(color1, color2);
    }

    private boolean isNeutral(String color) {
        return Set.of("black", "white", "gray", "silver", "beige", "cream", "tan", "navy").contains(color);
    }

    private boolean areSameFamily(String c1, String c2) {
        // Simple heuristic: if one string contains the other (e.g., "light blue" and
        // "blue")
        return c1.contains(c2) || c2.contains(c1);
    }

    private boolean checkComplementary(String c1, String c2) {
        // Specific pairings
        if (c1.contains("red") && (c2.contains("green") || c2.contains("blue") || c2.contains("black")))
            return true;
        if (c1.contains("blue")
                && (c2.contains("orange") || c2.contains("brown") || c2.contains("white") || c2.contains("khaki")))
            return true;
        if (c1.contains("green") && (c2.contains("brown") || c2.contains("yellow") || c2.contains("black")))
            return true;
        if (c1.contains("yellow")
                && (c2.contains("purple") || c2.contains("navy") || c2.contains("black") || c2.contains("gray")))
            return true;
        if (c1.contains("pink")
                && (c2.contains("gray") || c2.contains("white") || c2.contains("navy") || c2.contains("teal")))
            return true;
        if (c1.contains("purple") && (c2.contains("yellow") || c2.contains("white") || c2.contains("silver")))
            return true;

        return false; // Default: Avoid unknown clashes if not neutral/same family
    }

    // Score an outfit (Top + Bottom + Shoes)
    // 3 points = Perfect, 2 = Good, 1 = Ok, 0 = Bad
    public int scoreOutfit(WardrobeItem top, WardrobeItem bottom, WardrobeItem shoes) {
        String cTop = top.getColor();
        String cBottom = bottom.getColor();
        String cShoes = shoes.getColor();

        // Valid colors?
        if (cTop.equals("Unknown") || cBottom.equals("Unknown"))
            return 1;

        int score = 0;

        // Top + Bottom compatibility
        if (areColorsCompatible(cTop, cBottom))
            score++;

        // Shoes matching Bottom OR Shoes matching Top (Sandwich method)
        if (areColorsCompatible(cShoes, cBottom) || areColorsCompatible(cShoes, cTop))
            score++;

        // Bonus: Shoes match Top exactly (Sandwich Rule) is very stylish
        if (cShoes.equalsIgnoreCase(cTop))
            score++;

        return score;
    }
}
