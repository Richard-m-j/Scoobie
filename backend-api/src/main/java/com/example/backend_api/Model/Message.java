package com.example.backendapi.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.Data;
import lombok.NoArgsConstructor;

@Entity
@Data // Lombok: auto-generates getters, setters, toString, etc.
@NoArgsConstructor // Lombok: creates a no-argument constructor
public class Message {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String text;

    public Message(String text) {
        this.text = text;
    }
}