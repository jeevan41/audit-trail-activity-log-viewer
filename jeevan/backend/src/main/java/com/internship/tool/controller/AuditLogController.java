package com.internship.tool.controller;

import com.internship.tool.entity.AuditLog;
import com.internship.tool.service.AuditLogService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/audit-logs")
public class AuditLogController {

    private final AuditLogService auditLogService;

    public AuditLogController(AuditLogService auditLogService) {
        this.auditLogService = auditLogService;
    }

    @PostMapping
    public ResponseEntity<AuditLog> createAuditLog(@RequestBody Map<String, String> request) {
        String logEntry = request.get("logEntry");
        if (logEntry == null || logEntry.trim().isEmpty()) {
            return ResponseEntity.badRequest().build();
        }

        AuditLog auditLog = auditLogService.createAuditLog(logEntry);
        return ResponseEntity.ok(auditLog);
    }
}