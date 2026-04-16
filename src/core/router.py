from typing import Dict
from src.agents.sector_agents import ITAgent, PharmaAgent, BaseAgent


class QueryRouter:

    def route(self, query: str) -> Dict:
        q = query.lower()

        # 🔥 COMPANY MAP
        company_map = {
            "infosys": ("IT", "Infosys"),
            "tcs": ("IT", "TCS"),
            "wipro": ("IT", "Wipro"),
            "hcl": ("IT", "HCL"),
            "tech mahindra": ("IT", "Tech Mahindra"),
            "sun pharma": ("PHARMA", "Sun Pharma"),
            "dr reddy": ("PHARMA", "Dr Reddy"),
            "cipla": ("PHARMA", "Cipla")
        }

        sectors = set()
        entities = []

        # 🔥 ENTITY + SECTOR DETECTION
        for key, (sector, name) in company_map.items():
            if key in q:
                sectors.add(sector)
                entities.append(name)

        # 🔥 SECTOR KEYWORDS
        if any(word in q for word in ["it", "software", "tech"]):
            sectors.add("IT")

        if any(word in q for word in ["pharma", "drug", "medicine", "vaccine"]):
            sectors.add("PHARMA")

        if not sectors:
            sectors.add("GENERAL")

        # 🔥 QUERY TYPE (PRIORITY BASED)
        if any(word in q for word in ["compare", "vs", "difference"]):
            query_type = "COMPARISON"

        elif entities:
            query_type = "COMPANY_ANALYSIS"

        elif any(word in q for word in ["trend", "analysis", "analyze", "outlook"]):
            query_type = "SECTOR_ANALYSIS"

        else:
            query_type = "GENERAL"

        # 🔥 AGENTS
        agents = []
        for sector in sectors:
            if sector == "IT":
                agents.append(ITAgent())
            elif sector == "PHARMA":
                agents.append(PharmaAgent())
            else:
                agents.append(BaseAgent())

        return {
            "sectors": list(sectors),
            "query_type": query_type,
            "entities": entities,   # 🔥 NEW (VERY IMPORTANT)
            "agents": agents
        }

# 🔥 TEST
if __name__ == "__main__":
    router = QueryRouter()

    queries = [
        "Analyze IT sector in India",
        "Compare IT and Pharma growth",
        "Infosys revenue analysis",
        "Drug development trends"
    ]

    for q in queries:
        print("\nQuery:", q)
        print("Routing:", router.route(q))