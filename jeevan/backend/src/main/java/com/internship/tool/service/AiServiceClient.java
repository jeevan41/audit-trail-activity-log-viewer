package com.internship.tool.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;
    private final String aiServiceUrl;

    public AiServiceClient(RestTemplate restTemplate, @Value("${ai.service.url:http://localhost:5000}") String aiServiceUrl) {
        this.restTemplate = restTemplate;
        this.aiServiceUrl = aiServiceUrl;
    }

    public Map<String, Object> describeLogEntry(String logEntry) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, String> requestBody = Map.of("log_entry", logEntry);
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<Map> response = restTemplate.exchange(
                aiServiceUrl + "/describe",
                HttpMethod.POST,
                entity,
                Map.class
            );

            return response.getBody();
        } catch (Exception e) {
            // Handle null gracefully
            return null;
        }
    }

    public Map<String, Object> recommendForLogEntry(String logEntry) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, String> requestBody = Map.of("log_entry", logEntry);
            HttpEntity<Map<String, String>> entity = new HttpEntity<>(requestBody, headers);

            ResponseEntity<Map> response = restTemplate.exchange(
                aiServiceUrl + "/recommend",
                HttpMethod.POST,
                entity,
                Map.class
            );

            return response.getBody();
        } catch (Exception e) {
            // Handle null gracefully
            return null;
        }
    }
}