import os
import json
import math
import urllib.parse
from typing import Dict, List, Any, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots

# ------------------------------------------------------------
# Config / Flags
# ------------------------------------------------------------
st.set_page_config(
    page_title="Azure Solution Architect Pro",
    layout="wide",
    page_icon="☁️",
    initial_sidebar_state="expanded",
)

IS_ADMIN = os.getenv("AZ_SOL_ARCH_ADMIN", "false").lower() == "true"

# ------------------------------------------------------------
# Data Sources
# ------------------------------------------------------------
@st.cache_data(ttl=3600)
def get_comprehensive_azure_services() -> List[Dict[str, Any]]:
    return [
        {"name": "Azure Synapse Analytics", "category": "Analytics & BI", "subcategory": "Data Warehousing", "cost_tier": "high",
         "use_cases": ["data_warehouse", "analytics", "big_data", "etl", "reporting"], "integrates_with": ["Power BI", "Azure Data Lake", "Azure ML", "Data Factory"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Enterprise data warehouse that unites data integration, warehousing, and analytics",
         "data_role": "Central analytics hub for processing and analyzing large datasets", "architectural_importance": "critical",
         "pricing_model": "Pay-per-use + Reserved capacity", "docs": "https://learn.microsoft.com/azure/synapse-analytics/",
         "pricing": "https://azure.microsoft.com/pricing/details/synapse-analytics/"},
        {"name": "Power BI", "category": "Analytics & BI", "subcategory": "Visualization", "cost_tier": "medium",
         "use_cases": ["visualization", "dashboards", "reporting", "business_intelligence"], "integrates_with": ["Synapse", "Data Factory", "Office 365", "Dynamics"],
         "compliance": ["SOC", "ISO"], "description": "Business analytics platform for creating interactive dashboards and reports",
         "data_role": "Visualizes insights from data sources and presents to stakeholders", "architectural_importance": "high",
         "pricing_model": "Per-user subscription", "docs": "https://learn.microsoft.com/power-bi/", "pricing": "https://powerbi.microsoft.com/pricing/"},
        {"name": "Azure Data Factory", "category": "Analytics & BI", "subcategory": "Data Integration", "cost_tier": "medium",
         "use_cases": ["etl", "data_integration", "pipeline", "orchestration"], "integrates_with": ["Synapse", "Data Lake", "SQL Database", "Cosmos DB"],
         "compliance": ["SOC", "HIPAA", "ISO"], "description": "Cloud-based data integration service for creating ETL/ELT pipelines",
         "data_role": "Orchestrates data movement and transformation between sources", "architectural_importance": "high",
         "pricing_model": "Pay-per-execution", "docs": "https://learn.microsoft.com/azure/data-factory/", "pricing": "https://azure.microsoft.com/pricing/details/data-factory/"},
        {"name": "Azure Databricks", "category": "Analytics & BI", "subcategory": "Advanced Analytics", "cost_tier": "high",
         "use_cases": ["machine_learning", "big_data", "spark", "analytics"], "integrates_with": ["Azure ML", "Data Lake", "Synapse", "Power BI"],
         "compliance": ["SOC", "HIPAA", "ISO"], "description": "Apache Spark-based analytics platform for big data and machine learning",
         "data_role": "Processes large datasets and builds ML models collaboratively", "architectural_importance": "high",
         "pricing_model": "Compute + DBU charges", "docs": "https://learn.microsoft.com/azure/databricks/", "pricing": "https://azure.microsoft.com/pricing/details/databricks/"},
        {"name": "Azure OpenAI Service", "category": "AI & Machine Learning", "subcategory": "Generative AI", "cost_tier": "high",
         "use_cases": ["generative_ai", "chatbot", "content_generation", "language_models"], "integrates_with": ["Cognitive Services", "Bot Service", "Functions", "Logic Apps"],
         "compliance": ["SOC", "ISO"], "description": "Access to OpenAI's powerful language models including GPT-4",
         "data_role": "Generates content, answers questions, and processes natural language", "architectural_importance": "high",
         "pricing_model": "Token-based usage", "docs": "https://learn.microsoft.com/azure/ai-services/openai/",
         "pricing": "https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/"},
        {"name": "Azure Machine Learning", "category": "AI & Machine Learning", "subcategory": "ML Platform", "cost_tier": "high",
         "use_cases": ["machine_learning", "model_training", "mlops", "deployment"], "integrates_with": ["Databricks", "Synapse", "Container Registry", "Functions"],
         "compliance": ["SOC", "HIPAA", "ISO"], "description": "End-to-end machine learning lifecycle management platform",
         "data_role": "Trains, deploys, and manages machine learning models at scale", "architectural_importance": "high",
         "pricing_model": "Compute + Storage", "docs": "https://learn.microsoft.com/azure/machine-learning/", "pricing": "https://azure.microsoft.com/pricing/details/machine-learning/"},
        {"name": "Azure Cognitive Services", "category": "AI & Machine Learning", "subcategory": "Pre-built AI", "cost_tier": "medium",
         "use_cases": ["computer_vision", "speech", "language", "decision_apis"], "integrates_with": ["Bot Service", "Functions", "Logic Apps", "Power Platform"],
         "compliance": ["SOC", "ISO"], "description": "Pre-built AI services for vision, speech, language, and decision making",
         "data_role": "Adds AI capabilities to applications without custom model development", "architectural_importance": "medium",
         "pricing_model": "Transaction-based", "docs": "https://learn.microsoft.com/azure/cognitive-services/", "pricing": "https://azure.microsoft.com/pricing/details/cognitive-services/"},
        {"name": "Azure Kubernetes Service (AKS)", "category": "Containers", "subcategory": "Orchestration", "cost_tier": "medium",
         "use_cases": ["kubernetes", "microservices", "container_orchestration", "devops"], "integrates_with": ["Container Registry", "Monitor", "Active Directory", "Key Vault"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Managed Kubernetes service for deploying containerized applications",
         "data_role": "Orchestrates containerized applications with high availability", "architectural_importance": "high",
         "pricing_model": "Node pool compute costs", "docs": "https://learn.microsoft.com/azure/aks/", "pricing": "https://azure.microsoft.com/pricing/details/kubernetes-service/"},
        {"name": "Azure Container Apps", "category": "Containers", "subcategory": "Serverless Containers", "cost_tier": "low",
         "use_cases": ["serverless_containers", "microservices", "event_driven", "api"], "integrates_with": ["Event Grid", "Service Bus", "Monitor", "Key Vault"],
         "compliance": ["SOC", "ISO"], "description": "Serverless containers with built-in best practices",
         "data_role": "Runs containerized apps without managing infrastructure", "architectural_importance": "medium",
         "pricing_model": "vCPU and memory consumption", "docs": "https://learn.microsoft.com/azure/container-apps/",
         "pricing": "https://azure.microsoft.com/pricing/details/container-apps/"},
        {"name": "Azure API Management", "category": "Integration & Messaging", "subcategory": "API Gateway", "cost_tier": "medium",
         "use_cases": ["api_gateway", "api_management", "developer_portal", "policies"], "integrates_with": ["App Service", "Functions", "Logic Apps", "Active Directory"],
         "compliance": ["SOC", "HIPAA", "ISO"], "description": "Hybrid, multicloud management platform for APIs",
         "data_role": "Manages, secures, and analyzes APIs across environments", "architectural_importance": "high",
         "pricing_model": "Gateway units + calls", "docs": "https://learn.microsoft.com/azure/api-management/",
         "pricing": "https://azure.microsoft.com/pricing/details/api-management/"},
        {"name": "Azure Functions", "category": "Compute", "subcategory": "Serverless", "cost_tier": "low",
         "use_cases": ["serverless", "event_driven", "microservices", "triggers"], "integrates_with": ["Logic Apps", "Event Grid", "Cosmos DB", "Storage"],
         "compliance": ["SOC", "ISO"], "description": "Event-driven serverless compute platform",
         "data_role": "Executes code in response to events without managing infrastructure", "architectural_importance": "high",
         "pricing_model": "Consumption-based", "docs": "https://learn.microsoft.com/azure/azure-functions/",
         "pricing": "https://azure.microsoft.com/pricing/details/functions/"},
        {"name": "Azure Cosmos DB", "category": "Databases", "subcategory": "NoSQL", "cost_tier": "medium",
         "use_cases": ["nosql", "global_distribution", "multi_model", "real_time"], "integrates_with": ["Functions", "Synapse", "Power BI", "Search"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Globally distributed, multi-model NoSQL database",
         "data_role": "Stores unstructured data with global distribution and consistency", "architectural_importance": "high",
         "pricing_model": "Request Units + Storage", "docs": "https://learn.microsoft.com/azure/cosmos-db/",
         "pricing": "https://azure.microsoft.com/pricing/details/cosmos-db/"},
        {"name": "Azure SQL Database", "category": "Databases", "subcategory": "Relational", "cost_tier": "medium",
         "use_cases": ["relational_database", "sql_server", "oltp", "applications"], "integrates_with": ["Power BI", "Data Factory", "Functions", "App Service"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Fully managed relational database with AI-powered features",
         "data_role": "Stores structured data with ACID compliance and relationships", "architectural_importance": "high",
         "pricing_model": "DTU or vCore-based", "docs": "https://learn.microsoft.com/azure/azure-sql/database/",
         "pricing": "https://azure.microsoft.com/pricing/details/azure-sql-database/"},
        {"name": "Azure Blob Storage", "category": "Storage", "subcategory": "Object Storage", "cost_tier": "low",
         "use_cases": ["object_storage", "backup", "archival", "media", "data_lake"], "integrates_with": ["CDN", "Data Factory", "Synapse", "Functions"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Massively scalable object storage for unstructured data",
         "data_role": "Stores files, documents, media, and backup data", "architectural_importance": "high",
         "pricing_model": "Storage + transactions", "docs": "https://learn.microsoft.com/azure/storage/blobs/",
         "pricing": "https://azure.microsoft.com/pricing/details/storage/blobs/"},
        {"name": "Azure Virtual Network", "category": "Networking", "subcategory": "Core Networking", "cost_tier": "low",
         "use_cases": ["network_isolation", "hybrid_connectivity", "security", "subnets"], "integrates_with": ["Virtual Machines", "AKS", "Application Gateway", "Firewall"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Private network in Azure for connecting resources securely",
         "data_role": "Provides network isolation and secure communication paths", "architectural_importance": "critical",
         "pricing_model": "VPN Gateway + bandwidth", "docs": "https://learn.microsoft.com/azure/virtual-network/",
         "pricing": "https://azure.microsoft.com/pricing/details/virtual-network/"},
        {"name": "Azure Application Gateway", "category": "Networking", "subcategory": "Load Balancer", "cost_tier": "medium",
         "use_cases": ["load_balancer", "ssl_termination", "waf", "routing"], "integrates_with": ["Virtual Network", "AKS", "App Service", "Key Vault"],
         "compliance": ["SOC", "ISO"], "description": "Web traffic load balancer with application-level routing",
         "data_role": "Routes and load balances HTTP/HTTPS traffic to applications", "architectural_importance": "high",
         "pricing_model": "Gateway hours + data processing", "docs": "https://learn.microsoft.com/azure/application-gateway/",
         "pricing": "https://azure.microsoft.com/pricing/details/application-gateway/"},
        {"name": "Azure Active Directory", "category": "Security & Identity", "subcategory": "Identity Platform", "cost_tier": "variable",
         "use_cases": ["identity", "authentication", "authorization", "sso"], "integrates_with": ["All Azure Services", "Office 365", "Third-party SaaS"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Cloud-based identity and access management service",
         "data_role": "Manages user identities and access across all services", "architectural_importance": "critical",
         "pricing_model": "Per-user/per-month", "docs": "https://learn.microsoft.com/azure/active-directory/",
         "pricing": "https://azure.microsoft.com/pricing/details/active-directory/"},
        {"name": "Azure Key Vault", "category": "Security & Identity", "subcategory": "Secrets Management", "cost_tier": "low",
         "use_cases": ["secrets", "keys", "certificates", "encryption"], "integrates_with": ["App Service", "Functions", "AKS", "Virtual Machines"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Secure storage for secrets, keys, and certificates",
         "data_role": "Protects and manages cryptographic keys and secrets", "architectural_importance": "critical",
         "pricing_model": "Operations-based", "docs": "https://learn.microsoft.com/azure/key-vault/",
         "pricing": "https://azure.microsoft.com/pricing/details/key-vault/"},
        {"name": "Microsoft Defender for Cloud", "category": "Security & Identity", "subcategory": "Security Posture", "cost_tier": "medium",
         "use_cases": ["security_monitoring", "threat_detection", "compliance", "cspm"], "integrates_with": ["Monitor", "Sentinel", "Logic Apps", "Security Center"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Unified security management and advanced threat protection",
         "data_role": "Monitors and protects cloud resources from threats", "architectural_importance": "high",
         "pricing_model": "Per-resource pricing", "docs": "https://learn.microsoft.com/azure/defender-for-cloud/",
         "pricing": "https://azure.microsoft.com/pricing/details/defender-for-cloud/"},
        {"name": "Microsoft Sentinel", "category": "Security & Identity", "subcategory": "SIEM", "cost_tier": "medium",
         "use_cases": ["siem", "security_analytics", "threat_hunting", "incident_response"], "integrates_with": ["Monitor", "Defender", "Logic Apps", "Threat Intelligence"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Cloud-native SIEM and SOAR solution",
         "data_role": "Collects, analyzes, and responds to security events", "architectural_importance": "high",
         "pricing_model": "Data ingestion + analysis", "docs": "https://learn.microsoft.com/azure/sentinel/",
         "pricing": "https://azure.microsoft.com/pricing/details/microsoft-sentinel/"},
        {"name": "Azure Monitor", "category": "Monitoring & Management", "subcategory": "Observability", "cost_tier": "medium",
         "use_cases": ["monitoring", "logging", "metrics", "alerting", "diagnostics"], "integrates_with": ["All Azure Services", "Application Insights", "Log Analytics"],
         "compliance": ["SOC", "HIPAA", "ISO", "FedRAMP"], "description": "Full-stack monitoring service for applications and infrastructure",
         "data_role": "Collects, analyzes, and acts on telemetry from all environments", "architectural_importance": "critical",
         "pricing_model": "Data ingestion + retention", "docs": "https://learn.microsoft.com/azure/azure-monitor/",
         "pricing": "https://azure.microsoft.com/pricing/details/monitor/"},
        {"name": "Application Insights", "category": "Monitoring & Management", "subcategory": "APM", "cost_tier": "low",
         "use_cases": ["apm", "performance", "diagnostics", "user_analytics"], "integrates_with": ["App Service", "Functions", "AKS", "Monitor"],
         "compliance": ["SOC", "ISO"], "description": "Application performance monitoring and analytics service",
         "data_role": "Tracks application performance and user behavior", "architectural_importance": "high",
         "pricing_model": "Data volume-based", "docs": "https://learn.microsoft.com/azure/azure-monitor/app/app-insights-overview/",
         "pricing": "https://azure.microsoft.com/pricing/details/monitor/"},
    ]
# ------------------------------------------------------------
# Patterns / Compliance / Success Stories
# ------------------------------------------------------------
COMPREHENSIVE_PATTERNS = {
    "modern_data_platform": {
        "name": "Modern Data & Analytics Platform",
        "description": "Complete data platform with warehouse, lake, BI, and ML.",
        "required_services": ["Azure Data Factory", "Azure Blob Storage", "Azure Synapse Analytics", "Power BI"],
        "recommended_services": ["Azure Machine Learning", "Microsoft Purview", "Azure Monitor"],
        "optional_services": ["Azure Databricks", "Azure Stream Analytics", "Azure Cognitive Services"],
        "use_cases": ["data_warehouse", "analytics", "business_intelligence", "machine_learning"],
        "complexity": "high", "estimated_timeline": "3-6 months",
    },
    "intelligent_app_platform": {
        "name": "AI-Powered Application Platform",
        "description": "Modern application platform with integrated AI and APIs.",
        "required_services": ["Azure App Service", "Azure OpenAI Service", "Azure Cognitive Services", "Azure SQL Database"],
        "recommended_services": ["Azure Functions", "Azure API Management", "Application Insights", "Azure Key Vault"],
        "optional_services": ["Azure Bot Service", "Azure AI Search", "Azure Cache for Redis"],
        "use_cases": ["intelligent_apps", "chatbot", "automation", "ai_integration"],
        "complexity": "medium", "estimated_timeline": "2-4 months",
    },
    "cloud_native_microservices": {
        "name": "Cloud-Native Microservices Platform",
        "description": "Microservices with containers, DevOps, and observability.",
        "required_services": ["Azure Kubernetes Service (AKS)", "Azure Container Registry", "Azure Virtual Network", "Azure Monitor"],
        "recommended_services": ["Azure Application Gateway", "Azure Key Vault", "Azure API Management", "Azure Service Bus"],
        "optional_services": ["Azure Container Apps", "Azure Cache for Redis", "Microsoft Defender for Cloud"],
        "use_cases": ["microservices", "containers", "scalability", "devops"],
        "complexity": "high", "estimated_timeline": "4-8 months",
    },
    "serverless_event_driven": {
        "name": "Serverless Event-Driven Architecture",
        "description": "Event-driven, autoscaling, low-ops serverless stack.",
        "required_services": ["Azure Functions", "Azure Event Grid", "Azure Cosmos DB", "Azure Blob Storage"],
        "recommended_services": ["Azure Logic Apps", "Azure API Management", "Application Insights", "Azure Key Vault"],
        "optional_services": ["Azure Service Bus", "Azure Stream Analytics", "Power BI"],
        "use_cases": ["serverless", "event_driven", "auto_scaling", "cost_optimization"],
        "complexity": "medium", "estimated_timeline": "2-3 months",
    },
}

INDUSTRY_COMPLIANCE = {
    "healthcare": {"name": "Healthcare & Life Sciences", "compliance_frameworks": ["HIPAA", "HITECH", "FDA", "GxP"],
                   "required_services": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Monitor", "Azure Private Link"],
                   "data_residency": "required", "encryption": "end_to_end"},
    "financial": {"name": "Financial Services", "compliance_frameworks": ["PCI DSS", "SOX", "GDPR", "Basel III"],
                  "required_services": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Firewall", "Azure Monitor"],
                  "data_residency": "required", "encryption": "end_to_end"},
    "government": {"name": "Government & Public Sector", "compliance_frameworks": ["FedRAMP", "FISMA", "ITAR", "CJIS"],
                   "required_services": ["Azure Key Vault", "Microsoft Defender for Cloud", "Azure Policy", "Azure Monitor"],
                   "data_residency": "government_cloud", "encryption": "fips_140_2"},
    "retail": {"name": "Retail & E-commerce", "compliance_frameworks": ["PCI DSS", "GDPR", "CCPA"],
               "required_services": ["Azure Key Vault", "Azure CDN", "Azure Application Gateway"], "data_residency": "flexible", "encryption": "standard"},
    "technology": {"name": "Technology & Software", "compliance_frameworks": ["SOC 2", "ISO 27001", "GDPR"],
                   "required_services": ["Azure DevOps", "Azure Key Vault", "Azure Monitor"], "data_residency": "flexible", "encryption": "standard"},
}

SUCCESS_STORIES = {
    "healthcare": [{"title": "Provider cuts reporting time with Synapse + Power BI", "outcome": "60% faster insights",
                    "services": ["Synapse", "Power BI"], "link": "https://www.microsoft.com/en-us/customers"}],
    "financial": [{"title": "Bank modernizes apps with AKS + API Management", "outcome": "Reduced downtime 40%",
                   "services": ["AKS", "APIM"], "link": "https://www.microsoft.com/en-us/customers"}],
    "technology": [{"title": "ISV ships AI features with OpenAI + Functions", "outcome": "Launch in 6 weeks",
                    "services": ["Azure OpenAI", "Functions"], "link": "https://www.microsoft.com/en-us/customers"}],
}

# ------------------------------------------------------------
# Scoring & Analysis
# ------------------------------------------------------------
def calculate_comprehensive_score(service: Dict, requirements: Dict, architecture_context: Dict) -> Tuple[int, Dict]:
    score_breakdown = {k: 0 for k in ["functional_alignment", "architectural_fit", "compliance_match",
                                      "integration_synergy", "cost_efficiency", "industry_relevance", "innovation_factor"]}
    use_case_text = requirements.get("use_case", "").lower()
    selected_capabilities = requirements.get("capabilities", {})
    industry = requirements.get("industry", "")
    selected_services = architecture_context.get("selected_services", [])

    # Functional alignment (max 30)
    service_use_cases = [uc.lower() for uc in service.get("use_cases", [])]
    capability_matches = sum(1 for cap, val in selected_capabilities.items() if val and cap.lower().replace(" ", "_") in " ".join(service_use_cases))
    text_matches = sum(3 for uc in service_use_cases if uc in use_case_text)
    score_breakdown["functional_alignment"] = min(30, capability_matches * 5 + text_matches)

    # Architectural fit (max 20)
    importance_scores = {"critical": 20, "high": 15, "medium": 10, "low": 5}
    score_breakdown["architectural_fit"] = importance_scores.get(service.get("architectural_importance", "medium"), 10)

    # Compliance match (max 15)
    if industry in INDUSTRY_COMPLIANCE:
        req = INDUSTRY_COMPLIANCE[industry]
        frameworks = req["compliance_frameworks"]
        compliance_score = sum(3 for f in frameworks if f in service.get("compliance", []))
        if service["name"] in req["required_services"]:
            compliance_score += 6
        score_breakdown["compliance_match"] = min(15, compliance_score)

    # Integration synergy (max 15)
    integration_partners = service.get("integrates_with", [])
    synergy_score = sum(2 for selected in selected_services if any(p in selected for p in integration_partners))
    score_breakdown["integration_synergy"] = min(15, synergy_score)

    # Cost efficiency (max 10)
    cost_scores = {"free": 10, "low": 8, "medium": 6, "high": 3, "variable": 5}
    score_breakdown["cost_efficiency"] = cost_scores.get(service.get("cost_tier", "medium"), 6)

    # Industry relevance (max 5)
    if industry in ["healthcare", "financial", "government"] and service.get("category") in ["Security & Identity", "Monitoring & Management"]:
        score_breakdown["industry_relevance"] = 5
    elif industry in ["technology"] and service.get("category") in ["AI & Machine Learning", "DevOps & Developer Tools"]:
        score_breakdown["industry_relevance"] = 4

    # Innovation factor (max 5)
    innovative_services = ["Azure OpenAI Service", "Microsoft Fabric", "Azure Digital Twins", "Azure Container Apps", "Azure Machine Learning"]
    if service["name"] in innovative_services:
        score_breakdown["innovation_factor"] = 5
    elif service.get("category") == "AI & Machine Learning":
        score_breakdown["innovation_factor"] = 3

    # Normalize to 100
    max_possible = 30 + 20 + 15 + 15 + 10 + 5 + 5
    raw_total = sum(score_breakdown.values())
    normalized_total = round((raw_total / max_possible) * 100)
    return normalized_total, score_breakdown

def detect_architecture_patterns(selected_services: List[str], requirements: Dict) -> List[Dict]:
    patterns = []
    for name, pattern in COMPREHENSIVE_PATTERNS.items():
        reqd = pattern["required_services"]
        rec = pattern["recommended_services"]
        opt = pattern["optional_services"]
        required_coverage = sum(1 for s in reqd if s in selected_services)
        recommended_coverage = sum(1 for s in rec if s in selected_services)
        optional_coverage = sum(1 for s in opt if s in selected_services)
        total_required = len(reqd)
        completeness = "minimal"
        if required_coverage == total_required:
            completeness = "complete" if recommended_coverage >= len(rec) * 0.7 else "core_complete"
        elif required_coverage >= total_required * 0.8:
            completeness = "mostly_complete"
        elif required_coverage >= total_required * 0.5:
            completeness = "partially_complete"

        migration_notes = []
        if requirements.get("source_cloud") in ["AWS", "GCP", "On-prem"]:
            migration_notes.append(f"Plan DMS/migration waves from {requirements['source_cloud']}")
        if requirements.get("source_db"):
            migration_notes.append(f"Migrate DBs: {', '.join(requirements['source_db'])} via DMS/MI")
        if requirements.get("external_solutions"):
            migration_notes.append(f"Integrate external: {requirements['external_solutions']} (APIM/Logic Apps)")

        patterns.append({
            "name": pattern["name"],
            "description": pattern["description"],
            "completeness": completeness,
            "required_coverage": f"{required_coverage}/{total_required}",
            "recommended_coverage": f"{recommended_coverage}/{len(rec)}",
            "optional_coverage": optional_coverage,
            "missing_required": [s for s in reqd if s not in selected_services],
            "missing_recommended": [s for s in rec if s not in selected_services],
            "pattern_score": required_coverage * 3 + recommended_coverage * 2 + optional_coverage,
            "complexity": pattern["complexity"],
            "timeline": pattern["estimated_timeline"],
            "migration_notes": migration_notes,
        })
    patterns.sort(key=lambda x: x["pattern_score"], reverse=True)
    return patterns

def generate_cost_analysis(selected_services: List[Dict], requirements: Dict) -> Dict:
    base_costs = {"free": 0, "low": 75, "medium": 350, "high": 1200, "variable": 200}
    team_size = requirements.get("team_size", 10)
    data_volume = requirements.get("data_volume_gb", 500)
    expected_users = requirements.get("expected_users", 1000)
    cost = {"services": {}, "category_totals": {}, "total_monthly": 0, "total_annual": 0}
    total_monthly = 0
    category_costs = {}
    for svc in selected_services:
        cost_tier = svc.get("cost_tier", "medium")
        category = svc["category"]
        base = base_costs[cost_tier]
        if "Analytics" in category or "AI" in category:
            factor = max(1, data_volume / 100)
        elif "Compute" in category or "Container" in category:
            factor = max(1, expected_users / 500)
        elif "Database" in category:
            factor = max(1, (data_volume / 200) * (expected_users / 1000))
        else:
            factor = max(1, expected_users / 1000)
        monthly = base * factor
        annual = monthly * 12 * 0.85
        cost["services"][svc["name"]] = {"monthly_estimate": round(monthly, 2), "annual_estimate": round(annual, 2),
                                         "cost_tier": cost_tier, "scaling_factor": round(factor, 2), "category": category}
        total_monthly += monthly
        category_costs[category] = category_costs.get(category, 0) + monthly
    cost["total_monthly"] = round(total_monthly, 2)
    cost["total_annual"] = round(total_monthly * 12 * 0.85, 2)
    cost["category_totals"] = {k: round(v, 2) for k, v in category_costs.items()}
    return cost

def validate_architecture(selected_services: List[Dict], requirements: Dict) -> Tuple[List[str], List[str], List[str]]:
    names = [s["name"] for s in selected_services]
    cats = [s["category"] for s in selected_services]
    industry = requirements.get("industry", "")
    critical, warnings, recs = [], [], []
    if "Security & Identity" not in cats:
        critical.append("❌ Add identity/security (Azure AD, Key Vault).")
    if "Monitoring & Management" not in cats:
        critical.append("❌ Add monitoring (Azure Monitor, App Insights).")
    if any(c in ["Compute", "Containers"] for c in cats) and "Networking" not in cats:
        warnings.append("⚠️ Add Virtual Network for isolation.")
    if industry in INDUSTRY_COMPLIANCE:
        miss = [s for s in INDUSTRY_COMPLIANCE[industry]["required_services"] if s not in names]
        if miss:
            critical.append(f"❌ Missing required {industry} services: {', '.join(miss)}")
    return critical, warnings, recs

def calculate_business_value(selected_services: List[Dict], requirements: Dict) -> Dict:
    ai = len([s for s in selected_services if "AI" in s.get("category", "")])
    analytics = len([s for s in selected_services if "Analytics" in s.get("category", "")])
    devops = len([s for s in selected_services if "DevOps" in s.get("category", "")])
    security = len([s for s in selected_services if "Security" in s.get("category", "")])
    return {
        "cost_savings": {"infrastructure_reduction": min(0.4, 0.1 + len(selected_services) * 0.02),
                         "operational_efficiency": min(0.3, 0.1 + devops * 0.05),
                         "license_optimization": min(0.25, 0.1 + len(selected_services) * 0.01)},
        "productivity": {"developer_productivity": min(0.5, 0.2 + devops * 0.1),
                         "deployment_speed": min(0.7, 0.3 + devops * 0.15),
                         "time_to_market": min(0.5, 0.2 + ai * 0.1)},
        "innovation": {"ai_ml_capabilities": ai, "analytics_maturity": analytics, "security_posture": security},
    }

def get_success_stories(industry: str, selected_services: List[str]) -> List[Dict]:
    return SUCCESS_STORIES.get(industry, [])

# ------------------------------------------------------------
# Draw.io generation and viewer
# ------------------------------------------------------------
def generate_drawio_xml(selected_services: List[Dict]) -> str:
    cat_groups = {}
    for svc in selected_services:
        cat_groups.setdefault(svc["category"], []).append(svc["name"])
    cells, x, y, cell_id = [], 40, 40, 1
    for cat, items in cat_groups.items():
        cells.append(f'<mxCell id="{cell_id}" value="{cat}" style="swimlane;fontStyle=1;horizontal=1;" vertex="1"><mxGeometry x="{x}" y="{y}" width="260" height="{120+30*len(items)}" as="geometry"/></mxCell>')
        parent = cell_id
        cell_id += 1
        yy = y + 40
        for item in items:
            cells.append(f'<mxCell id="{cell_id}" value="{item}" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc" vertex="1" parent="{parent}"><mxGeometry x="20" y="{yy - y}" width="200" height="30" as="geometry"/></mxCell>')
            cell_id += 1
            yy += 40
        y += 180
    xml = f'<mxfile host="app.diagrams.net"><diagram name="Azure Architecture"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>'
    return xml

def drawio_viewer_url(xml: str) -> str:
    encoded = urllib.parse.quote(xml)
    return f"https://viewer.diagrams.net/?lightbox=1&edit=_blank&layers=1&nav=1&title=azure-architecture.drawio#R{encoded}"

# ------------------------------------------------------------
# Utility UI helpers
# ------------------------------------------------------------
def score_help_row(label: str, text: str, value: int):
    st.markdown(f"**{label}** ℹ️", help=text)
    st.write(f"{value}")

def record_event(event: Dict[str, Any]):
    st.session_state.setdefault("telemetry", []).append(event)
# ------------------------------------------------------------
# Main App
# ------------------------------------------------------------
def main():
    st.title("🏗️ Azure Solution Architect Pro")
    st.caption("Comprehensive Azure architecture recommendations with scoring, cost, patterns, diagrams, and business value.")

    # Sidebar inputs
    with st.sidebar:
        st.header("📋 Requirements")
        use_case = st.text_area("Use case / goals", placeholder="e.g., Real-time analytics with AI features...", height=120)
        industry = st.selectbox("Industry", [""] + list(INDUSTRY_COMPLIANCE.keys()),
                                format_func=lambda x: INDUSTRY_COMPLIANCE[x]["name"] if x else "Select industry")
        st.subheader("📊 Scale")
        team_size = st.slider("Team size", 1, 100, 10)
        expected_users = st.slider("Expected users", 100, 100000, 1000, step=100)
        data_volume = st.slider("Data volume (GB)", 10, 10000, 500, step=50)

        st.subheader("🎯 Capabilities")
        caps = {}
        for cap in ["Data Warehousing", "Real-time Analytics", "Business Intelligence", "ETL/Data Integration",
                    "Machine Learning", "Generative AI", "APIs", "Microservices", "Serverless", "Monitoring", "Security", "Networking", "IoT"]:
            caps[cap] = st.checkbox(cap, key=f"cap_{cap}")

        st.subheader("🚚 Migration")
        source_cloud = st.selectbox("Source cloud/hosting", ["", "On-prem", "AWS", "GCP", "Other"])
        source_db = st.multiselect("Source databases", ["SQL Server", "Oracle", "MySQL", "PostgreSQL", "MongoDB", "Other"])
        external_solutions = st.text_input("External solutions (SAP, Salesforce, ServiceNow, etc.)")
        migration_cutover = st.select_slider("Cutover preference", ["Big bang", "Phased", "Parallel run"])

        st.divider()
        generate_recommendations = st.button("🚀 Generate Architecture", type="primary", use_container_width=True)

        if IS_ADMIN:
            with st.expander("📈 Telemetry (admin only)", expanded=False):
                st.write("Sessions (local):", len(st.session_state.get("telemetry", [])))
                st.write("Recent industries:", list({e.get("industry") for e in st.session_state.get("telemetry", []) if e.get("industry")}))

    # Main flow
    if generate_recommendations and use_case:
        requirements = {
            "use_case": use_case,
            "industry": industry,
            "capabilities": caps,
            "team_size": team_size,
            "expected_users": expected_users,
            "data_volume_gb": data_volume,
            "source_cloud": source_cloud,
            "source_db": source_db,
            "external_solutions": external_solutions,
            "migration_cutover": migration_cutover,
        }
        record_event({"industry": industry, "caps": sum(caps.values())})

        all_services = get_comprehensive_azure_services()
        scored = []
        context = {"selected_services": []}
        for svc in all_services:
            score, breakdown = calculate_comprehensive_score(svc, requirements, context)
            if score > 20:
                s = svc.copy()
                s["total_score"] = score
                s["score_breakdown"] = breakdown
                scored.append(s)
        scored.sort(key=lambda x: (-x["total_score"], x["name"]))
        top_services = scored[:20]
        context["selected_services"] = [s["name"] for s in top_services]

        patterns = detect_architecture_patterns(context["selected_services"], requirements)
        cost = generate_cost_analysis(top_services, requirements)
        critical, warnings, recs = validate_architecture(top_services, requirements)
        business = calculate_business_value(top_services, requirements)
        stories = get_success_stories(industry, context["selected_services"])
        diagram_xml = generate_drawio_xml(top_services)
        diagram_url = drawio_viewer_url(diagram_xml)

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📋 Recommended Services", "🏗️ Architecture Patterns", "💰 Cost Analysis",
            "🖼️ Architecture Diagram", "✅ Validation & Next Steps", "📈 Business Value"
        ])

        # Tab 1: Recommended Services
        with tab1:
            st.header("🎯 Recommended Azure Services")
            for i, svc in enumerate(top_services, 1):
                with st.expander(f"{i}. {svc['name']} — Score {svc['total_score']}/100", expanded=i <= 5):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Category:** {svc['category']}")
                        st.write(f"**Description:** {svc['description']}")
                        st.write(f"**Role:** {svc['data_role']}")
                        st.write("**Score Breakdown:**")
                        bd = svc["score_breakdown"]
                        score_help_row("Functional Alignment", "Match to use case and selected capabilities.", bd["functional_alignment"])
                        score_help_row("Architectural Fit", "Importance of this service in target architecture.", bd["architectural_fit"])
                        score_help_row("Compliance Match", "Alignment to industry/regulatory frameworks.", bd["compliance_match"])
                        score_help_row("Integration Synergy", "Fit with other selected services.", bd["integration_synergy"])
                        score_help_row("Cost Efficiency", "Relative cost tier vs. scale.", bd["cost_efficiency"])
                        score_help_row("Industry Relevance", "Relevance to the chosen industry.", bd["industry_relevance"])
                        score_help_row("Innovation Factor", "Next-gen/AI-oriented services.", bd["innovation_factor"])
                    with col2:
                        st.metric("Total Score", f"{svc['total_score']}/100")
                        st.write(f"**Cost Tier:** {svc['cost_tier'].title()}")
                        st.write(f"[Pricing]({svc['pricing']})")
                        st.write(f"[Docs]({svc['docs']})")

        # Tab 2: Architecture Patterns
        with tab2:
            st.header("🏗️ Architecture Patterns (with migration hints)")
            for p in patterns[:4]:
                with st.container():
                    st.subheader(p["name"])
                    st.write(p["description"])
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Completeness", p["completeness"].replace("_", " ").title())
                    c2.metric("Complexity", p["complexity"].title())
                    c3.metric("Timeline", p["timeline"])
                    st.write(f"Required coverage: {p['required_coverage']} | Recommended: {p['recommended_coverage']}")
                    if p["missing_required"]:
                        st.error(f"Missing required: {', '.join(p['missing_required'])}")
                    if p["missing_recommended"]:
                        st.info(f"Consider adding: {', '.join(p['missing_recommended'])}")
                    if p["migration_notes"]:
                        st.warning("Migration: " + " | ".join(p["migration_notes"]))
                    st.divider()

        # Tab 3: Cost Analysis
        with tab3:
            st.header("💰 Cost Analysis")
            mode = st.radio("Cost Mode", ["Pay-as-you-go (default)", "MSX / MACC-adjusted"], horizontal=True)
            st.caption("Pay-as-you-go view; connect MSX/MACC to include committed-spend and ACR offsets.")
            col1, col2, col3 = st.columns(3)
            if mode == "Pay-as-you-go (default)":
                col1.metric("Monthly (PAYG)", f"${cost['total_monthly']:,.2f}")
                col2.metric("Annual (PAYG)", f"${cost['total_annual']:,.2f}")
                col3.metric("Annual Savings vs monthly x12", f"${cost['total_monthly']*12 - cost['total_annual']:,.2f}")
            else:
                mac_discount = st.slider("MACC discount (%)", 0, 30, 10)
                acr_offset = st.slider("ACR offset ($/month)", 0, 50000, 5000, step=500)
                monthly_adj = max(0, cost["total_monthly"] * (1 - mac_discount / 100) - acr_offset)
                col1.metric("Monthly (MSX/MACC)", f"${monthly_adj:,.2f}")
                col2.metric("Annual (MSX/MACC)", f"${monthly_adj*12*0.85:,.2f}")
                col3.metric("Applied discounts", f"{mac_discount}% + ACR ${acr_offset:,.0f}")
            st.subheader("📊 Cost Breakdown by Category")
            cost_df = pd.DataFrame([{"Category": k, "Monthly Cost": v} for k, v in cost["category_totals"].items()])
            if not cost_df.empty:
                fig = px.pie(cost_df, values="Monthly Cost", names="Category", title="Monthly Cost Distribution")
                st.plotly_chart(fig, use_container_width=True)
            st.subheader("🏷️ Service Cost Breakdown")
            services_df = pd.DataFrame([
                {"Service": n, "Category": d["category"], "Monthly": d["monthly_estimate"], "Annual": d["annual_estimate"], "Tier": d["cost_tier"]}
                for n, d in cost["services"].items()
            ])
            st.dataframe(services_df, use_container_width=True)

        # Tab 4: Architecture Diagram
        with tab4:
            st.header("🖼️ Architecture Diagram (draw.io embedded)")
            st.caption("Diagram uses draw.io viewer. If it does not load, allow third-party content.")
            st.components.v1.iframe(src=diagram_url, height=600, scrolling=True)

        # Tab 5: Validation & Next Steps
        with tab5:
            st.header("✅ Validation & Next Steps")
            if critical:
                st.error("Critical issues:")
                for c in critical:
                    st.error(c)
            if warnings:
                st.warning("Warnings:")
                for w in warnings:
                    st.warning(w)
            if recs:
                st.info("Recommendations:")
                for r in recs:
                    st.info(r)
            st.subheader("Next Steps")
            for step in [
                "Review recommended services vs. requirements.",
                "Pilot core services (top 5) before broad rollout.",
                "Define landing zone: identity, networking, security, monitoring.",
                "Plan migration waves and cutover strategy.",
                "Set cost governance and budgets (FinOps).",
            ]:
                st.write(f"- {step}")

        # Tab 6: Business Value & Success Stories
        with tab6:
            st.header("📈 Business Value & Success Stories")
            c1, c2, c3 = st.columns(3)
            c1.metric("Infra cost reduction", f"{business['cost_savings']['infrastructure_reduction']:.0%}")
            c2.metric("Operational efficiency", f"{business['cost_savings']['operational_efficiency']:.0%}")
            c3.metric("License optimization", f"{business['cost_savings']['license_optimization']:.0%}")
            c1.metric("Dev productivity", f"{business['productivity']['developer_productivity']:.0%}")
            c2.metric("Deployment speed", f"{business['productivity']['deployment_speed']:.0%}")
            c3.metric("Time to market", f"{business['productivity']['time_to_market']:.0%}")
            c1.metric("AI/ML services", business["innovation"]["ai_ml_capabilities"])
            c2.metric("Analytics services", business["innovation"]["analytics_maturity"])
            c3.metric("Security services", business["innovation"]["security_posture"])

            st.subheader("🏆 Success Stories (industry-matched)")
            if stories:
                for s in stories:
                    st.markdown(f"**{s['title']}** — {s['outcome']}  \nServices: {', '.join(s['services'])}  \n[Read more]({s['link']})")
            else:
                st.info("Add industry to see relevant success stories from microsoft.com/customers.")
    else:
        st.header("Welcome")
        st.write("Describe your use case, select industry, capabilities, migration inputs, then click Generate Architecture.")

if __name__ == "__main__":
    main()
