package com.example.backendapi.controller;

import com.example.backendapi.model.Message;
import com.example.backendapi.repository.MessageRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
public class ApiController {

    @Autowired
    private MessageRepository messageRepository;

    @GetMapping("/messages")
    public List<Message> getMessages() {
        return messageRepository.findAll();
    }
}