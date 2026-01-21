package com.stylesense.stylesense.repository;

import com.stylesense.stylesense.model.WardrobeItem;
import com.stylesense.stylesense.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface WardrobeRepository extends JpaRepository<WardrobeItem, Long> {
    List<WardrobeItem> findByUser(User user);
}
