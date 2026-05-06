import chromadb
import numpy as np
import os

class DummyEmbeddingFunction:
    def __call__(self, input):
        # Return dummy embeddings (all zeros for simplicity)
        return [np.zeros(384).tolist() for _ in input]
    
    def name(self):
        return "dummy"

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection with dummy embedding function
collection = client.get_or_create_collection(
    name="audit_knowledge",
    embedding_function=DummyEmbeddingFunction()
)

# Domain knowledge documents
documents = [
    {
        "content": "Audit trails are chronological records of system activities that provide evidence of actions performed within an information system. They are essential for security monitoring, compliance, and forensic analysis.",
        "metadata": {"category": "basics", "importance": "high"}
    },
    {
        "content": "Common audit log entry types include: user authentication events, file access attempts, system configuration changes, network connections, and privilege escalations.",
        "metadata": {"category": "log_types", "importance": "high"}
    },
    {
        "content": "Security implications of audit logs: Failed login attempts may indicate brute force attacks, unusual file access patterns could signal data exfiltration, and privilege escalation events require immediate investigation.",
        "metadata": {"category": "security", "importance": "critical"}
    },
    {
        "content": "Compliance requirements: SOX requires audit trails for financial systems, HIPAA mandates healthcare audit logs, PCI DSS requires payment system logging, and GDPR demands data access logging.",
        "metadata": {"category": "compliance", "importance": "high"}
    },
    {
        "content": "Log analysis best practices: Regular review of logs, correlation of events across systems, automated alerting for suspicious patterns, and retention of logs for required periods.",
        "metadata": {"category": "best_practices", "importance": "medium"}
    },
    {
        "content": "Common attack patterns in logs: Multiple failed authentications from same IP, unusual time-based access, privilege escalation chains, and data export activities outside normal hours.",
        "metadata": {"category": "threats", "importance": "high"}
    },
    {
        "content": "Log integrity: Ensure logs cannot be tampered with through write-once media, cryptographic hashing, or secure logging mechanisms to maintain evidentiary value.",
        "metadata": {"category": "integrity", "importance": "medium"}
    },
    {
        "content": "Performance monitoring via logs: Track system performance metrics, identify bottlenecks, monitor resource utilization, and detect anomalies that may indicate security issues.",
        "metadata": {"category": "performance", "importance": "low"}
    },
    {
        "content": "User behavior analytics: Establish baseline user behavior patterns, detect deviations that may indicate compromised accounts or insider threats.",
        "metadata": {"category": "analytics", "importance": "medium"}
    },
    {
        "content": "Incident response using audit logs: Logs provide timeline of events, help identify attack vectors, support root cause analysis, and aid in regulatory reporting.",
        "metadata": {"category": "incident_response", "importance": "high"}
    }
]

# Add documents to collection
ids = [f"doc_{i+1}" for i in range(len(documents))]
contents = [doc["content"] for doc in documents]
metadatas = [doc["metadata"] for doc in documents]

collection.add(
    documents=contents,
    metadatas=metadatas,
    ids=ids
)

print(f"Successfully seeded ChromaDB with {len(documents)} domain knowledge documents.")
print("Collection info:", collection.count())