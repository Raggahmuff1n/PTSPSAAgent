import os
import json
import math
import urllib.parse
from typing import Dict, List, Any, Tuple

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Azure Solution Architect Pro",
    layout="wide",
    page_icon="☁️",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Flags
# ------------------------------------------------------------------
IS_ADMIN = os.getenv("AZ_SOL_ARCH_ADMIN", "false").lower() == "true"

# ------------------------------------------------------------------
# Data Sources (catalog; keep as-is or swap in your longer original list)
# ------------------------------------------------------------------
@st.cache_data(ttl=3600)
def get_comprehensive_azure_services() -> List[Dict[str, Any]]:
    return [
        # --- Analytics & BI ---
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
        {"name": "Azure Stream Analytics", "category": "Analytics & BI", "subcategory": "Real-time Analytics", "cost_tier": "medium",
         "use_cases": ["real_time", "streaming", "iot", "event_processing"], "integrates_with": ["Event Hubs", "IoT Hub", "Power BI", "Functions"],
         "compliance": ["SOC", "ISO"], "description": "Real-time analytics service for streaming data",
         "data_role": "Processes streaming data in real-time for immediate insights", "architectural_importance": "medium",
         "pricing_model": "Streaming Units per hour", "docs": "https://learn.microsoft.com/azure/stream-analytics/", "pricing": "https://azure.microsoft.com/pricing/details/stream-analytics/"},
        {"name": "Microsoft Fabric", "category": "Analytics & BI", "subcategory": "Unified Analytics", "cost_tier": "high",
         "use_cases": ["unified_analytics", "data_lakehouse", "governance", "collaboration"], "integrates_with": ["Power BI", "Synapse", "Data Factory", "Purview"],
         "compliance": ["SOC", "HIPAA", "ISO"], "description": "All-in-one analytics solution that covers everything from data movement to data science",
         "data_role": "Unified platform for end-to-end analytics and data science workflows", "architectural_importance": "critical",
         "pricing_model": "Capacity-based", "docs": "https://learn.microsoft.com/fabric/", "pricing": "https://azure.microsoft.com/pricing/details/microsoft-fabric/"},
        {"name": "Microsoft Purview", "category": "Analytics & BI", "subcategory": "Data Governance", "cost_tier": "medium",
         "use_cases": ["data_governance", "compliance", "data_discovery", "lineage"], "integrates_with": ["Synapse", "Data Factory", "SQL Database", "Fabric"],
         "compliance": ["SOC", "HIPAA", "ISO", "GDPR"], "description": "Unified data governance service for managing and governing data estate",
         "data_role": "Provides data discovery, classification, lineage, and governance", "architectural_importance": "high",
         "pricing_model": "Data map size + scans", "docs": "https://learn.microsoft.com/purview/", "pricing": "https://azure.microsoft.com/pricing/details/purview/"},
        # (Continue with the rest of your catalog items here; keep or paste your full list)
    ]

# ------------------------------------------------------------------
# Patterns (includes migration/external cues)
# ------------------------------------------------------------------
COMPREHENSIVE_PATTERNS = {
    "modern_data_platform": {
        "name": "Modern Data & Analytics Platform",
        "description": "Complete data platform with warehouse, lake, BI, and ML.",
        "required_services": ["Azure Data Factory", "Azure Data Lake Storage", "Azure Synapse Analytics", "Power BI"],
        "recommended_services": ["Microsoft Fabric", "Azure Machine Learning", "Microsoft Purview", "Azure Monitor"],
        "optional_services": ["Azure Databricks", "Azure Stream Analytics", "Azure Cognitive Services"],
        "use_cases": ["data_warehouse", "analytics", "business_intelligence", "machine_learning", "reporting"],
        "industries": ["financial", "healthcare", "retail", "manufacturing"],
        "complexity": "high", "estimated_timeline": "3-6 months",
    },
    "intelligent_app_platform": {
        "name": "AI-Powered Application Platform",
        "description": "Modern application platform with integrated AI and automation.",
        "required_services": ["Azure App Service", "Azure OpenAI Service", "Azure Cognitive Services", "Azure SQL Database"],
        "recommended_services": ["Azure Functions", "Azure API Management", "Application Insights", "Azure Key Vault"],
        "optional_services": ["Azure Bot Service", "Azure AI Search", "Azure Cache for Redis"],
        "use_cases": ["intelligent_apps", "chatbot", "automation", "ai_integration"],
        "industries": ["technology", "healthcare", "financial", "retail"],
        "complexity": "medium", "estimated_timeline": "2-4 months",
    },
    "cloud_native_microservices": {
        "name": "Cloud-Native Microservices Platform",
        "description": "Microservices with containers, DevOps, and observability.",
        "required_services": ["Azure Kubernetes Service (AKS)", "Azure Container Registry", "Azure Virtual Network", "Azure Monitor"],
        "recommended_services": ["Azure Application Gateway", "Azure Key Vault", "Azure API Management", "Azure Service Bus"],
        "optional_services": ["Azure Container Apps", "Azure Cache for Redis", "Microsoft Defender for Cloud"],
        "use_cases": ["microservices", "containers", "scalability", "devops"],
        "industries": ["technology", "financial", "retail", "gaming"],
        "complexity": "high", "estimated_timeline": "4-8 months",
    },
    "serverless_event_driven": {
        "name": "Serverless Event-Driven Architecture",
        "description": "Event-driven, autoscaling, low-ops serverless stack.",
        "required_services": ["Azure Functions", "Azure Event Grid", "Azure Cosmos DB", "Azure Blob Storage"],
        "recommended_services": ["Azure Logic Apps", "Azure API Management", "Application Insights", "Azure Key Vault"],
        "optional_services": ["Azure Service Bus", "Azure Stream Analytics", "Power BI"],
        "use_cases": ["serverless", "event_driven", "auto_scaling", "cost_optimization"],
        "industries": ["startup", "media", "iot", "retail"],
        "complexity": "medium", "estimated_timeline": "2-3 months",
    },
}

# ------------------------------------------------------------------
# Industry Compliance
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# Success Stories (static samples; source: microsoft.com/customers)
# ------------------------------------------------------------------
SUCCESS_STORIES = {
    "healthcare": [
        {"title": "Provider cuts reporting time with Synapse + Power BI", "outcome": "60% faster insights",
         "services": ["Synapse", "Power BI"], "link": "https://www.microsoft.com/en-us/customers"}
    ],
    "financial": [
        {"title": "Bank modernizes apps with AKS + API Management", "outcome": "Reduced downtime 40%",
         "services": ["AKS", "API Management"], "link": "https://www.microsoft.com/en-us/customers"}
    ],
    "technology": [
        {"title": "ISV ships AI features with OpenAI + Functions", "outcome": "Launch in 6 weeks",
         "services": ["Azure OpenAI", "Functions"], "link": "https://www.microsoft.com/en-us/customers"}
    ],
}

# ------------------------------------------------------------------
# Scoring (boosted/normalized and tooltipped)
# ------------------------------------------------------------------
def score_help_row(label: str, text: str, value: int):
    st.markdown(f"**{label}** ℹ️", help=text)
    st.write(f"{value}")

def calculate_comprehensive_score(service: Dict, requirements: Dict, architecture_context: Dict) -> Tuple[int, Dict]:
    score_breakdown = {k: 0 for k in [
        "functional_alignment", "architectural_fit", "compliance_match",
        "integration_synergy", "cost_efficiency", "industry_relevance", "innovation_factor"
    ]}
    use_case_text = requirements.get("use_case", "").lower()
    selected_capabilities = requirements.get("capabilities", {})
    industry = requirements.get("industry", "")
    selected_services = architecture_context.get("selected_services", [])

    caps = {
        "functional_alignment": 35,
        "architectural_fit": 20,
        "compliance_match": 15,
        "integration_synergy": 15,
        "cost_efficiency": 10,
        "industry_relevance": 5,
        "innovation_factor": 5,
    }

    service_use_cases = [uc.lower() for uc in service.get("use_cases", [])]
    capability_matches = sum(
        1 for cap, val in selected_capabilities.items()
        if val and cap.lower().replace(" ", "_") in " ".join(service_use_cases)
    )
    text_matches = sum(4 for uc in service_use_cases if uc in use_case_text)
    score_breakdown["functional_alignment"] = min(caps["functional_alignment"], capability_matches * 5 + text_matches)

    importance_scores = {"critical": 20, "high": 16, "medium": 11, "low": 6}
    score_breakdown["architectural_fit"] = importance_scores.get(service.get("architectural_importance", "medium"), 11)

    if industry in INDUSTRY_COMPLIANCE:
        req = INDUSTRY_COMPLIANCE[industry]
        frameworks = req["compliance_frameworks"]
        compliance_score = sum(3 for f in frameworks if f in service.get("compliance", []))
        if service["name"] in req["required_services"]:
            compliance_score += 6
        score_breakdown["compliance_match"] = min(caps["compliance_match"], compliance_score)

    integration_partners = service.get("integrates_with", [])
    synergy_score = sum(2 for selected in selected_services if any(p in selected for p in integration_partners))
    score_breakdown["integration_synergy"] = min(caps["integration_synergy"], synergy_score)

    cost_scores = {"free": 10, "low": 8, "medium": 6, "high": 4, "variable": 5}
    score_breakdown["cost_efficiency"] = cost_scores.get(service.get("cost_tier", "medium"), 6)

    if industry in ["healthcare", "financial", "government"] and service.get("category") in ["Security & Identity", "Monitoring & Management"]:
        score_breakdown["industry_relevance"] = 5
    elif industry in ["technology", "startup"] and service.get("category") in ["AI & Machine Learning", "DevOps & Developer Tools"]:
        score_breakdown["industry_relevance"] = 4
    elif industry == "manufacturing" and service.get("category") in ["IoT & Edge", "Analytics & BI"]:
        score_breakdown["industry_relevance"] = 4

    innovative_services = ["Azure OpenAI Service", "Microsoft Fabric", "Azure Digital Twins", "Azure Container Apps", "Azure Machine Learning"]
    if service["name"] in innovative_services:
        score_breakdown["innovation_factor"] = 5
    elif service.get("category") == "AI & Machine Learning":
        score_breakdown["innovation_factor"] = 3

    raw = sum(score_breakdown.values())
    max_possible = sum(caps.values())
    normalized = round((raw / max_possible) * 100)
    return normalized, score_breakdown

# ------------------------------------------------------------------
# Patterns with migration/external cues
# ------------------------------------------------------------------
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
            migration_notes.append(f"Plan DMS/ASR waves from {requirements['source_cloud']}")
        if requirements.get("source_db"):
            migration_notes.append(f"Migrate DBs: {', '.join(requirements['source_db'])} via DMS/MI")
        if requirements.get("external_solutions"):
            migration_notes.append(f"Integrate external: {requirements['external_solutions']} (APIM/Logic Apps)")

        pattern_use_cases = pattern["use_cases"]
        use_case_text = requirements.get("use_case", "").lower()
        capabilities = requirements.get("capabilities", {})
        use_case_alignment = sum(1 for uc in pattern_use_cases
                                 if uc in use_case_text or
                                 any(uc in cap.lower() for cap, selected in capabilities.items() if selected))

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
            "use_case_alignment": use_case_alignment,
        })
    patterns.sort(key=lambda x: x["pattern_score"], reverse=True)
    return patterns

# ------------------------------------------------------------------
# Cost Analysis with PAYG and MSX/MACC toggle
# ------------------------------------------------------------------
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

# ------------------------------------------------------------------
# Validation
# ------------------------------------------------------------------
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

    # Guardrail: too many or too few services
    if len(names) < 6:
        warnings.append("⚠️ Very few services selected; ensure baseline identity, monitoring, network, compute, storage.")
    if len(names) > 25:
        warnings.append("⚠️ Many services selected; review for scope creep and cost.")

    return critical, warnings, recs

# ------------------------------------------------------------------
# Business Value + Success Stories
# ------------------------------------------------------------------
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
    stories = SUCCESS_STORIES.get(industry, [])
    prioritized = []
    for s in stories:
        if any(key.lower() in " ".join(selected_services).lower() for key in s["services"]):
            prioritized.append(s)
    if prioritized:
        return prioritized
    return stories

# ------------------------------------------------------------------
# draw.io generation (simple swimlanes; azure-ish fills)
# ------------------------------------------------------------------
def generate_drawio_xml(selected_services: List[Dict]) -> str:
    cat_groups = {}
    for svc in selected_services:
        cat_groups.setdefault(svc["category"], []).append(svc["name"])
    cells, x, y, cid = [], 40, 40, 1
    for cat, items in cat_groups.items():
        height = 120 + 30 * len(items)
        cells.append(f'<mxCell id="{cid}" value="{cat}" style="swimlane;fontStyle=1;horizontal=1;" vertex="1"><mxGeometry x="{x}" y="{y}" width="320" height="{height}" as="geometry"/></mxCell>')
        parent = cid
        cid += 1
        yy = y + 40
        color = "#DAE8FC" if "Compute" in cat or "Container" in cat else "#E1D5E7" if "AI" in cat else "#D5E8D4"
        for item in items:
            cells.append(f'<mxCell id="{cid}" value="{item}" style="rounded=1;whiteSpace=wrap;html=1;fillColor={color}" vertex="1" parent="{parent}"><mxGeometry x="20" y="{yy - y}" width="260" height="28" as="geometry"/></mxCell>')
            cid += 1
            yy += 34
        y += height + 20
    xml = f'<mxfile host="app.diagrams.net"><diagram name="Azure Architecture"><mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>{"".join(cells)}</root></mxGraphModel></diagram></mxfile>'
    return xml

def drawio_viewer_url(xml: str) -> str:
    encoded = urllib.parse.quote(xml, safe="")
    return f"https://viewer.diagrams.net/?lightbox=1&edit=_blank&layers=1&nav=1&title=azure-architecture.drawio#R{encoded}"

# ------------------------------------------------------------------
# Telemetry (admin-only)
# ------------------------------------------------------------------
def record_event(event: Dict[str, Any]):
    st.session_state.setdefault("telemetry", []).append(event)

# ------------------------------------------------------------------
# Main App
# ------------------------------------------------------------------
def main():
    st.title("🏗️ Azure Solution Architect Pro")
    st.caption("Comprehensive Azure architecture recommendations with scoring, cost, patterns, diagrams, migration cues, and business value.")

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
        for cap in [
            "Data Warehousing", "Real-time Analytics", "Business Intelligence", "ETL/Data Integration",
            "Machine Learning", "Generative AI", "APIs", "Microservices", "Serverless",
            "Monitoring", "Security", "Networking", "IoT"
        ]:
            caps[cap] = st.checkbox(cap, key=f"cap_{cap}")

        st.subheader("🚚 Migration & External")
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

    # Guardrail / wizard hint
    st.info("Wizard guardrail: ensure at least identity, monitoring, networking, compute, and one data store are selected. Avoid selecting more than ~25 services for a first pass.")

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
                        score_help_row("Functional Alignment", "Match to use case and capabilities.", bd["functional_alignment"])
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
            st.header("🏗️ Architecture Patterns (with migration & external cues)")
            for p in patterns[:4]:
                st.subheader(p["name"])
                st.write(p["description"])
                c1, c2, c3 = st.columns(3)
                c1.metric("Completeness", p["completeness"].replace("_", " ").title())
                c2.metric("Complexity", p["complexity"].title())
                c3.metric("Timeline", p["timeline"])
                st.write(f"Required: {p['required_coverage']} | Recommended: {p['recommended_coverage']} | Optional hits: {p['optional_coverage']}")
                if p.get("migration_notes"):
                    st.warning("Migration / External: " + " | ".join(p["migration_notes"]))
                if p["missing_required"]:
                    st.error(f"Missing required: {', '.join(p['missing_required'])}")
                if p["missing_recommended"]:
                    st.info(f"Consider adding: {', '.join(p['missing_recommended'])}")
                st.divider()

        # Tab 3: Cost Analysis
        with tab3:
            st.header("💰 Cost Analysis")
            st.caption("This section is a PAYG estimator. Toggle MSX/MACC to apply discounts/ACR offsets.")
            mode = st.radio("Cost Mode", ["Pay-as-you-go (default)", "MSX / MACC-adjusted"], horizontal=True)

            if mode == "Pay-as-you-go (default)":
                col1, col2, col3 = st.columns(3)
                col1.metric("Monthly (PAYG)", f"${cost['total_monthly']:,.2f}")
                col2.metric("Annual (PAYG)", f"${cost['total_annual']:,.2f}")
                col3.metric("Annual Savings vs monthly x12", f"${cost['total_monthly']*12 - cost['total_annual']:,.2f}")
            else:
                mac_discount = st.slider("MACC discount (%)", 0, 30, 10)
                acr_offset = st.slider("ACR offset ($/month)", 0, 50000, 5000, step=500)
                monthly_adj = max(0, cost["total_monthly"] * (1 - mac_discount / 100) - acr_offset)
                col1, col2, col3 = st.columns(3)
                col1.metric("Monthly (MSX/MACC)", f"${monthly_adj:,.2f}")
                col2.metric("Annual (MSX/MACC)", f"${monthly_adj*12*0.85:,.2f}")
                col3.metric("Applied discounts", f"{mac_discount}% + ACR ${acr_offset:,.0f}")

            st.subheader("📊 Cost Breakdown by Category")
            cost_df = pd.DataFrame([{"Category": k, "Monthly Cost": v} for k, v in cost["category_totals"].items()])
            if cost_df.empty:
                st.info("No cost data available for the current selection.")
            else:
                fig = px.pie(cost_df, values="Monthly Cost", names="Category", title="Monthly Cost Distribution")
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("🏷️ Service Cost Breakdown")
            services_df = pd.DataFrame([
                {"Service": n, "Category": d["category"], "Monthly": d["monthly_estimate"], "Annual": d["annual_estimate"], "Tier": d["cost_tier"]}
                for n, d in cost["services"].items()
            ])
            st.dataframe(services_df, use_container_width=True)

        # Tab 4: Architecture Diagram (draw.io)
        with tab4:
            st.header("🖼️ Architecture Diagram (draw.io embedded)")
            st.caption("Uses draw.io viewer. If blocked, click below to open in a new tab or allow third-party content.")
            st.components.v1.iframe(src=diagram_url, height=720, scrolling=True)
            st.markdown(f"[Open in draw.io viewer]({diagram_url})")

        # Tab 5: Validation & Next Steps
        with tab5:
            st.header("✅ Validation & Next Steps")
            if critical:
                st.error("🚨 Critical Issues")
                for c in critical:
                    st.error(f"• {c}")
            if warnings:
                st.warning("⚠️ Recommendations")
                for w in warnings:
                    st.warning(f"• {w}")
            if recs:
                st.info("💡 Architecture Improvements")
                for r in recs:
                    st.info(f"• {r}")

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

            st.subheader("Cost Savings")
            c1, c2, c3 = st.columns(3)
            c1.metric("Infra cost reduction", f"{business['cost_savings']['infrastructure_reduction']:.0%}")
            c1.caption("Estimate from consolidation + cloud elasticity.")
            c2.metric("Operational efficiency", f"{business['cost_savings']['operational_efficiency']:.0%}")
            c2.caption("Efficiency from automation/DevOps practices.")
            c3.metric("License optimization", f"{business['cost_savings']['license_optimization']:.0%}")
            c3.caption("Savings via right-sizing and platform services.")

            st.subheader("Productivity")
            c1, c2, c3 = st.columns(3)
            c1.metric("Dev productivity", f"{business['productivity']['developer_productivity']:.0%}")
            c1.caption("Faster delivery from CI/CD & platform services.")
            c2.metric("Deployment speed", f"{business['productivity']['deployment_speed']:.0%}")
            c2.caption("Reduced cycle time from build → prod.")
            c3.metric("Time to market", f"{business['productivity']['time_to_market']:.0%}")
            c3.caption("New features faster via managed/AI services.")

            st.subheader("Innovation & Security")
            c1, c2, c3 = st.columns(3)
            c1.metric("AI/ML services", business["innovation"]["ai_ml_capabilities"])
            c1.caption("Count of AI/ML services selected.")
            c2.metric("Analytics services", business["innovation"]["analytics_maturity"])
            c2.caption("Analytics building blocks included.")
            c3.metric("Security services", business["innovation"]["security_posture"])
            c3.caption("Security/identity/monitoring components included.")

            st.subheader("🏆 Success Stories (industry-matched)")
            if stories:
                for s in stories:
                    st.markdown(f"**{s['title']}** — {s['outcome']}  \nServices: {', '.join(s['services'])}  \n[Read more]({s['link']})")
            else:
                st.info("Add industry to see relevant success stories from microsoft.com/customers.")
    else:
        # Welcome screen
        st.header("🏗️ Welcome to Azure Solution Architect Pro")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            ### 🎯 What This Tool Does:
            - **Comprehensive Service Recommendations** across Azure
            - **Architecture Pattern Detection** with completeness analysis
            - **Detailed Cost Analysis** (PAYG + MSX/MACC toggle)
            - **Architecture Validation** with guardrails
            - **Architecture Diagrams** (draw.io)
            - **Business Value & Success Stories**
            """)
        with col2:
            st.markdown("""
            ### 🚀 Perfect For:
            - Solution Architects
            - Technical Consultants
            - Dev Teams planning cloud migrations
            - Business Stakeholders
            - Partners creating proposals
            """)
        st.markdown("""
        ### 📋 Get Started:
        1. Describe your use case in the sidebar
        2. Select your industry (for compliance)
        3. Choose capabilities
        4. Set scale (team size, users, data)
        5. Generate recommendations
        """)
        st.subheader("💡 Sample Use Cases")
        sample_cases = {
            "Modern Data Platform": "Build a comprehensive data platform for real-time analytics, ML, BI, with governance and security.",
            "AI-Powered Application": "Create intelligent applications with generative AI, automated workflows, seamless UX.",
            "Cloud-Native Microservices": "Design a scalable microservices architecture with containers, DevOps, and monitoring.",
            "IoT Analytics Platform": "End-to-end IoT for device management, real-time processing, predictive analytics.",
            "Secure Enterprise Platform": "Zero-trust security, compliance, and governance for the enterprise.",
            "Hybrid Cloud Strategy": "Unified hybrid cloud platform connecting on-prem and Azure with centralized management."
        }
        for title, description in sample_cases.items():
            with st.expander(title):
                st.write(description)

if __name__ == "__main__":
    main()
