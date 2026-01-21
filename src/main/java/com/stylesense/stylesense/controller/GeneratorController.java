package com.stylesense.stylesense.controller;

import com.stylesense.stylesense.model.User;
import com.stylesense.stylesense.model.WardrobeItem;
import com.stylesense.stylesense.repository.UserRepository;
import com.stylesense.stylesense.service.WardrobeService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.security.Principal;
import java.util.List;
import java.util.Random;

@Controller
public class GeneratorController {

    private final WardrobeService wardrobeService;
    private final UserRepository userRepository;
    private final com.stylesense.stylesense.service.OutfitRecommendationService recommendationService;
    private final Random random = new Random();

    public GeneratorController(WardrobeService wardrobeService, UserRepository userRepository,
            com.stylesense.stylesense.service.OutfitRecommendationService recommendationService) {
        this.wardrobeService = wardrobeService;
        this.userRepository = userRepository;
        this.recommendationService = recommendationService;
    }

    @GetMapping("/generator")
    public String generateOutfit(@RequestParam(required = false) String occasion, Model model, Principal principal) {
        if (principal == null)
            return "redirect:/login";
        String username = principal.getName();

        User user = userRepository.findByUsername(username).orElse(null);
        if (user == null)
            return "redirect:/logout";

        List<WardrobeItem> allItems = wardrobeService.getItemsByUser(user);

        // Filter by Occasion if provided
        if (occasion != null && !occasion.isEmpty() && !occasion.equals("All")) {
            allItems = allItems.stream()
                    .filter(i -> recommendationService.isOccasionMatch(i, occasion))
                    .toList();
        }

        // Match categories: Shirt, Pant, Shoe
        List<WardrobeItem> tops = allItems.stream().filter(i -> "Shirt".equalsIgnoreCase(i.getCategory())).toList();
        List<WardrobeItem> bottoms = allItems.stream().filter(i -> "Pant".equalsIgnoreCase(i.getCategory())).toList();
        List<WardrobeItem> shoes = allItems.stream().filter(i -> "Shoe".equalsIgnoreCase(i.getCategory())).toList();

        // Fallback for older items if any (Top/Bottom) - optional, but user is starting
        // fresh effectively.

        if (tops.isEmpty() || bottoms.isEmpty() || shoes.isEmpty()) {
            model.addAttribute("error", "Not enough items" + (occasion != null ? " for this occasion" : "")
                    + " to generate an outfit. Need at least 1 Shirt, 1 Pant, 1 Shoe.");
            return "generator";
        }

        // Smart Generation: Try 20 random combos and pick the best score
        WardrobeItem bestTop = tops.get(0);
        WardrobeItem bestBottom = bottoms.get(0);
        WardrobeItem bestShoes = shoes.get(0);
        int bestScore = -1;

        for (int i = 0; i < 20; i++) {
            WardrobeItem t = tops.get(random.nextInt(tops.size()));
            WardrobeItem b = bottoms.get(random.nextInt(bottoms.size()));
            WardrobeItem s = shoes.get(random.nextInt(shoes.size()));

            int score = recommendationService.scoreOutfit(t, b, s);
            if (score > bestScore) {
                bestScore = score;
                bestTop = t;
                bestBottom = b;
                bestShoes = s;
            }
        }

        model.addAttribute("top", bestTop);
        model.addAttribute("bottom", bestBottom);
        model.addAttribute("shoes", bestShoes);
        model.addAttribute("generated", true);
        model.addAttribute("score", bestScore);
        model.addAttribute("selectedOccasion", occasion);

        return "generator";
    }
}
