package com.example.backendapi.repository;

import com.example.backendapi.model.Message;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MessageRepository extends JpaRepository<Message, Long> {
    // Spring Data JPA will automatically create the methods for us!
}