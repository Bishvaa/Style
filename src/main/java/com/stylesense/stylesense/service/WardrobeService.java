package com.stylesense.stylesense.service;

import com.stylesense.stylesense.model.User;
import com.stylesense.stylesense.model.WardrobeItem;
import com.stylesense.stylesense.repository.WardrobeRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;
import java.util.UUID;

@Service
public class WardrobeService {

    private final WardrobeRepository wardrobeRepository;
    private final Path uploadPath = Paths.get("uploads");

    public WardrobeService(WardrobeRepository wardrobeRepository) {
        this.wardrobeRepository = wardrobeRepository;
        try {
            Files.createDirectories(uploadPath);
        } catch (IOException e) {
            throw new RuntimeException("Could not create upload directory", e);
        }
    }

    public List<WardrobeItem> getItemsByUser(User user) {
        return wardrobeRepository.findByUser(user);
    }

    public void uploadItem(MultipartFile file, String category, String occasion, User user) throws IOException {
        String filename = UUID.randomUUID().toString() + "_" + file.getOriginalFilename();
        Path filePath = uploadPath.resolve(filename);
        Files.copy(file.getInputStream(), filePath);

        // Detect Color - safely
        String color = "Unknown";
        try (java.io.InputStream is = Files.newInputStream(filePath)) {
            color = com.stylesense.stylesense.util.ColorUtils.getDominantColorName(is);
        } catch (Throwable t) {
            System.err.println("WARNING: Color detection failed: " + t.getMessage());
            // We do NOT rethrow, so the item is still saved with "Unknown" color
        }

        String imageUrl = "/uploads/" + filename;
        WardrobeItem item = new WardrobeItem(imageUrl, category, color, occasion, user);
        wardrobeRepository.save(item);
    }

    public WardrobeItem getItemById(Long id) {
        return wardrobeRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Item not found"));
    }

    public void deleteItem(Long itemId, User user) {
        WardrobeItem item = wardrobeRepository.findById(itemId)
                .orElseThrow(() -> new RuntimeException("Item not found"));

        if (!item.getUser().getId().equals(user.getId())) {
            throw new RuntimeException("Unauthorized");
        }

        // Optional: Delete file from disk
        // Path filePath = uploadPath.resolve(item.getImageUrl().replace("/uploads/",
        // ""));
        // try { Files.deleteIfExists(filePath); } catch (IOException ignored) {}

        wardrobeRepository.delete(item);
    }
}
