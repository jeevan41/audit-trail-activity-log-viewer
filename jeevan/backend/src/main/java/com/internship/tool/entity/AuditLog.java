package com.internship.tool.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.Map;

@Entity
@Table(name = "audit_logs")
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String logEntry;

    @Column(columnDefinition = "TEXT")
    private String aiDescription;

    @Column(columnDefinition = "TEXT")
    private String aiRecommendations;

    @Column
    private LocalDateTime createdAt;

    @Column
    private LocalDateTime aiProcessedAt;

    // Constructors
    public AuditLog() {}

    public AuditLog(String logEntry) {
        this.logEntry = logEntry;
        this.createdAt = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getLogEntry() { return logEntry; }
    public void setLogEntry(String logEntry) { this.logEntry = logEntry; }

    public String getAiDescription() { return aiDescription; }
    public void setAiDescription(String aiDescription) { this.aiDescription = aiDescription; }

    public String getAiRecommendations() { return aiRecommendations; }
    public void setAiRecommendations(String aiRecommendations) { this.aiRecommendations = aiRecommendations; }

    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }

    public LocalDateTime getAiProcessedAt() { return aiProcessedAt; }
    public void setAiProcessedAt(LocalDateTime aiProcessedAt) { this.aiProcessedAt = aiProcessedAt; }
}