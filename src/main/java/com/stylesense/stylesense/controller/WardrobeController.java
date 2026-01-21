package com.stylesense.stylesense.controller;

import com.stylesense.stylesense.model.User;
import com.stylesense.stylesense.model.WardrobeItem;
import com.stylesense.stylesense.repository.UserRepository;
import com.stylesense.stylesense.service.WardrobeService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.security.Principal;
import java.util.List;

@Controller
public class WardrobeController {

    private final WardrobeService wardrobeService;
    private final UserRepository userRepository;

    public WardrobeController(WardrobeService wardrobeService, UserRepository userRepository) {
        this.wardrobeService = wardrobeService;
        this.userRepository = userRepository;
    }

    private User getAuthenticatedUser(Principal principal) {
        if (principal == null)
            return null;
        return userRepository.findByUsername(principal.getName()).orElse(null);
    }

    @GetMapping("/wardrobe")
    public String wardrobeHub(Model model, Principal principal) {
        if (getAuthenticatedUser(principal) == null)
            return "redirect:/logout";
        return "wardrobe";
    }

    @GetMapping("/wardrobe/{category}")
    public String viewCategory(@org.springframework.web.bind.annotation.PathVariable String category, Model model,
            Principal principal) {
        User user = getAuthenticatedUser(principal);
        if (user == null)
            return "redirect:/logout";

        List<WardrobeItem> allItems = wardrobeService.getItemsByUser(user);

        // Normalize category name for filtering (capitalized)
        String filterCategory = category.substring(0, 1).toUpperCase() + category.substring(1).toLowerCase();

        List<WardrobeItem> categoryItems = allItems.stream()
                .filter(i -> filterCategory.equalsIgnoreCase(i.getCategory()))
                .toList();

        model.addAttribute("category", filterCategory);
        model.addAttribute("items", categoryItems);

        return "wardrobe-category";
    }

    @PostMapping("/wardrobe/upload")
    public String uploadItem(@RequestParam("file") List<MultipartFile> files,
            @RequestParam("category") String category,
            @RequestParam(value = "occasion", required = false) String occasion,
            Principal principal) throws IOException {
        User user = getAuthenticatedUser(principal);
        if (user == null)
            return "redirect:/logout";

        for (MultipartFile file : files) {
            if (!file.isEmpty()) {
                wardrobeService.uploadItem(file, category, occasion, user);
            }
        }
        return "redirect:/wardrobe/" + category;
    }

    @PostMapping("/wardrobe/delete/{id}")
    public String deleteItem(@org.springframework.web.bind.annotation.PathVariable Long id, Principal principal) {
        User user = getAuthenticatedUser(principal);
        if (user == null)
            return "redirect:/logout";

        WardrobeItem item = wardrobeService.getItemById(id);
        String category = item.getCategory();

        wardrobeService.deleteItem(id, user);
        return "redirect:/wardrobe/" + category;
    }
}
