package com.stylesense.stylesense.model;

import jakarta.persistence.*;

@Entity
public class WardrobeItem {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String imageUrl;
    private String category; // e.g., "Top", "Bottom", "Shoes"
    private String color;
    private String occasion; // "Formal", "College", "Party", "Travel"

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;

    public WardrobeItem() {
    }

    public WardrobeItem(String imageUrl, String category, String color, String occasion, User user) {
        this.imageUrl = imageUrl;
        this.category = category;
        this.color = color;
        this.occasion = occasion;
        this.user = user;
    }

    // ... getters/setters ...

    public String getOccasion() {
        return occasion;
    }

    public void setOccasion(String occasion) {
        this.occasion = occasion;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getImageUrl() {
        return imageUrl;
    }

    public void setImageUrl(String imageUrl) {
        this.imageUrl = imageUrl;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }
}
