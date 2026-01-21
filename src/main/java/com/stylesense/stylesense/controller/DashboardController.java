package com.stylesense.stylesense.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.ui.Model;
import java.security.Principal;

@Controller
public class DashboardController {

    public DashboardController() {
    }

    @GetMapping("/dashboard")
    public String dashboard(Model model, Principal principal) {
        if (principal == null)
            return "redirect:/login";
        String username = principal.getName();
        model.addAttribute("username", username);
        return "dashboard";
    }
}
