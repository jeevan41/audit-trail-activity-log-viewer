package com.internship.tool.service;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.repository.AuditLogRepository;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.Map;

@Service
public class AuditLogService {

    private final AuditLogRepository auditLogRepository;
    private final AiServiceClient aiServiceClient;

    public AuditLogService(AuditLogRepository auditLogRepository, AiServiceClient aiServiceClient) {
        this.auditLogRepository = auditLogRepository;
        this.aiServiceClient = aiServiceClient;
    }

    @Transactional
    public AuditLog createAuditLog(String logEntry) {
        AuditLog auditLog = new AuditLog(logEntry);
        auditLog = auditLogRepository.save(auditLog);

        // Call AI processing asynchronously
        processAiAnalysis(auditLog.getId(), logEntry);

        return auditLog;
    }

    @Async
    public void processAiAnalysis(Long auditLogId, String logEntry) {
        try {
            // Call describe
            Map<String, Object> descriptionResult = aiServiceClient.describeLogEntry(logEntry);
            String description = null;
            if (descriptionResult != null && descriptionResult.containsKey("description")) {
                description = (String) descriptionResult.get("description");
            }

            // Call recommend
            Map<String, Object> recommendationResult = aiServiceClient.recommendForLogEntry(logEntry);
            String recommendations = null;
            if (recommendationResult != null && recommendationResult.containsKey("recommendations")) {
                // Convert to string or store as JSON
                recommendations = recommendationResult.get("recommendations").toString();
            }

            // Update the audit log with AI results
            AuditLog auditLog = auditLogRepository.findById(auditLogId).orElse(null);
            if (auditLog != null) {
                auditLog.setAiDescription(description);
                auditLog.setAiRecommendations(recommendations);
                auditLog.setAiProcessedAt(LocalDateTime.now());
                auditLogRepository.save(auditLog);
            }
        } catch (Exception e) {
            // Handle exceptions gracefully, perhaps log them
            System.err.println("Error processing AI analysis: " + e.getMessage());
        }
    }
}