package com.example.backendapi;

import com.example.backendapi.model.Message;
import com.example.backendapi.repository.MessageRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class BackendApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackendApiApplication.class, args);
    }

    // This bean runs on startup and inserts a sample message into the database.
    @Bean
    CommandLineRunner commandLineRunner(MessageRepository repository) {
        return args -> {
            repository.save(new Message("Hello from the Backend!"));
        };
    }
}