# StyleSense 👗👔

**StyleSense** is a smart digital wardrobe assistant built with Spring Boot. It helps you organize your clothes, upload items by category (Shirt, Pant, Shoe, Accessories), and generate AI-powered outfit recommendations for any occasion.

## ✨ Features

-   **Digital Wardrobe Hub**:
    -   Organize your closet into 4 clear sections: **Shirt**, **Pant**, **Shoe**, **Accessories**.
    -   Upload images directly to each category.
    -   View your collection in a beautiful grid layout.
-   **Smart Outfit Generator**:
    -   AI-driven logic combines a Shirt, Pant, and Shoe based on color harmony (Complementary, Analogous, Neutral).
    -   **Occasion Filtering**: Generate outfits specifically for **Formal**, **Casual**, or **Party** events.
-   **User Accounts**: Secure Login and Registration system to keep your wardrobe private.
-   **Dashboard**: Quick access to your style stats (Total Items, Outfits Generated, etc.).

## 🛠️ Tech Stack

-   **Backend**: Java 17, Spring Boot 3
-   **Frontend**: Thymeleaf, HTML5, CSS3, JavaScript
-   **Database**: H2 Database (In-Memory for Dev) / MySQL (Production ready)
-   **Security**: Spring Security

## 🚀 How to Run

1.  **Clone the repo**:
    ```bash
    git clone https://github.com/Bishvaa/StyleSense.git
    cd StyleSense
    ```

2.  **Run with Maven**:
    ```bash
    mvn spring-boot:run
    ```

3.  **Access the App**:
    Open your browser and go to `http://localhost:8080`.

## 📸 Screenshots

| Wardrobe Hub | Outfit Generator |
| :---: | :---: |
| *Manage your collection* | *Get smart recommendations* |

## 🤝 Contributing

1.  Fork the repository.
2.  Create a branch (`git checkout -b feature-name`).
3.  Commit your changes (`git commit -m "Add feature"`).
4.  Push to the branch (`git push origin feature-name`).
5.  Open a Pull Request.

---
*Built with ❤️ by Bishvaa*
