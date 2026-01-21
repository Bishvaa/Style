package com.stylesense.stylesense.util;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public class ColorUtils {

    public static String getDominantColorName(InputStream imageStream) {
        try {
            BufferedImage image = ImageIO.read(imageStream);
            if (image == null)
                return "Unknown";

            Map<String, Integer> colorCounts = new HashMap<>();
            int width = image.getWidth();
            int height = image.getHeight();

            // HEURISTIC: Focus on the center 50% of the image to avoid background noise.
            // Clothes are usually centered.
            int startX = width / 4;
            int endX = startX + (width / 2);
            int startY = height / 4;
            int endY = startY + (height / 2);

            // Sample step for performance
            int step = 5;

            for (int x = startX; x < endX; x += step) {
                for (int y = startY; y < endY; y += step) {
                    // Safe bounds check
                    if (x >= width || y >= height)
                        continue;

                    int rgb = image.getRGB(x, y);

                    // Ignore strictly transparent pixels
                    if (((rgb >> 24) & 0xFF) == 0)
                        continue;

                    int r = (rgb >> 16) & 0xFF;
                    int g = (rgb >> 8) & 0xFF;
                    int b = (rgb) & 0xFF;

                    String colorName = getColorNameFromHSL(r, g, b);
                    colorCounts.put(colorName, colorCounts.getOrDefault(colorName, 0) + 1);
                }
            }

            return colorCounts.entrySet().stream()
                    .max(Map.Entry.comparingByValue())
                    .map(Map.Entry::getKey)
                    .orElse("Unknown");

        } catch (IOException e) {
            e.printStackTrace();
            return "Unknown";
        }
    }

    private static String getColorNameFromHSL(int r, int g, int b) {
        float[] hsl = rgbToHsl(r, g, b);
        float h = hsl[0]; // 0-360
        float s = hsl[1]; // 0-100
        float l = hsl[2]; // 0-100

        // 1. Grayscale Check (Low Saturation)
        // If saturation is very low, it's a shade of gray/white/black
        if (s < 15) {
            if (l < 15)
                return "Black";
            if (l < 35)
                return "Dark Gray";
            if (l < 65)
                return "Gray";
            if (l < 85)
                return "Silver";
            return "White";
        }

        // 2. Color by Hue
        // Extreme Lightness overrides Hue
        if (l < 15)
            return "Black"; // Very dark colors are black
        if (l > 93)
            return "White"; // Very bright colors are white

        // Hue Ranges
        if (h >= 0 && h < 15)
            return (l > 30) ? "Red" : "Maroon";
        if (h >= 15 && h < 45)
            return (l > 75) ? "Beige" : (l < 40 ? "Brown" : "Orange");
        if (h >= 45 && h < 70)
            return "Yellow";
        if (h >= 70 && h < 150)
            return "Green";
        if (h >= 150 && h < 190)
            return "Teal";
        if (h >= 190 && h < 260) {
            if (l > 70)
                return "Light Blue";
            return (l < 40) ? "Navy" : "Blue";
        }
        if (h >= 260 && h < 300)
            return "Purple";
        if (h >= 300 && h < 340)
            return "Pink";
        // Wrap around for Red
        if (h >= 340 && h <= 360)
            return (l > 30) ? "Red" : "Maroon";

        return "Gray"; // Fallback
    }

    private static float[] rgbToHsl(int r, int g, int b) {
        float fr = r / 255f;
        float fg = g / 255f;
        float fb = b / 255f;

        float max = Math.max(fr, Math.max(fg, fb));
        float min = Math.min(fr, Math.min(fg, fb));

        float h = 0, s = 0, l = (max + min) / 2;

        if (max != min) {
            float d = max - min;
            s = l > 0.5 ? d / (2 - max - min) : d / (max + min);

            if (max == fr)
                h = (fg - fb) / d + (fg < fb ? 6 : 0);
            else if (max == fg)
                h = (fb - fr) / d + 2;
            else if (max == fb)
                h = (fr - fg) / d + 4;

            h *= 60;
        }

        return new float[] { h, s * 100, l * 100 };
    }
}
