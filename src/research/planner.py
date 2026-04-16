import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from typing import Dict, List


class ResearchPlanner:
     def create_plan(self, query: str, routing: Dict, agent=None) -> Dict:

        query_type = routing.get("query_type", "GENERAL")
        sectors = routing.get("sectors", ["GENERAL"])

        context = ""
        if agent:
            try:
                context = agent.get_context()
            except:
                context = ""

        query_lower = query.lower()

        steps = []
        plan_explanation = []
        expected_output = ""

        # 🔥 Detect complexity
        is_deep = any(word in query_lower for word in [
            "analyze", "deep dive", "trend", "outlook", "impact"
        ])

        # 🔹 SECTOR ANALYSIS
        if query_type == "SECTOR_ANALYSIS":

            steps = [
                f"Understand {sectors[0]} market size and growth",
                f"Identify major companies in {sectors[0]} sector",
                f"Analyze recent developments and news",
                f"Explore emerging technologies (AI, automation, etc.)",
                f"Evaluate financial performance of key players",
                f"Study regulatory and policy changes",
                f"Identify risks and challenges",
                f"Forecast future outlook and opportunities"
            ]

            if is_deep:
                steps.extend([
                    f"Compare global vs {sectors[0]} market",
                    f"Analyze investment trends and capital flow"
                ])

                plan_explanation = [
                    "Market landscape and growth trends",
                    "Key players and competition",
                    "Technology and innovation trends",
                    "Financial and regulatory analysis",
                    "Future outlook and risks"
                ]

                expected_output = "Comprehensive sector research report with trends, risks, and opportunities"

        # 🔹 COMPANY ANALYSIS
        elif query_type == "COMPANY_ANALYSIS":

            steps = [
                "Company overview and business model",
                "Revenue, profit, and margin analysis",
                "Balance sheet and financial health",
                "Compare with competitors",
                "Recent news and developments",
                "Growth drivers",
                "Risks and weaknesses",
                "Future outlook"
            ]

            if is_deep:
                steps.append("Stock performance and valuation analysis")

                plan_explanation = [
                    "Company fundamentals",
                    "Financial performance",
                    "Competitive positioning",
                    "Growth and risks"
                ]

                expected_output = "Detailed company financial and strategic analysis"

        # 🔹 COMPARISON
        elif query_type == "COMPARISON":

            steps = [
                "Identify companies/entities",
                "Collect financial metrics",
                "Compare revenue, profit, and margins",
                "Analyze growth trends",
                "Compare market position",
                "Evaluate strengths and weaknesses",
                "Summarize differences",
                "Final recommendation"
            ]

            plan_explanation = [
                "Side-by-side comparison",
                "Financial performance differences",
                "Strategic positioning",
                "Final insights"
            ]

            expected_output = "Comparative analysis with clear recommendation"

        # 🔹 GENERAL
        else:
            steps = [
                "Understand query context",
                "Gather financial data",
                "Analyze multiple sources",
                "Extract key insights",
                "Provide summary"
            ]

            plan_explanation = [
                "General financial research",
                "Data collection and synthesis"
            ]

            expected_output = "Structured summary with insights"

        return {
            "query": query,
            "query_type": query_type,
            "sectors": sectors,
            "context": context,
            "steps": steps,
            "plan_explanation": plan_explanation,
            "expected_output": expected_output,
            "total_steps": len(steps)
        }

# 🔥 TEST
if __name__ == "__main__":
    from src.core.router import QueryRouter
    from src.agents.sector_agents import ITAgent

    router = QueryRouter()
    planner = ResearchPlanner()

    query = "Analyze IT sector in India"

    routing = router.route(query)

    # Simulate agent
    agent = ITAgent()

    plan = planner.create_plan(query, routing, agent)

    print("Routing:", routing)
    print("\nResearch Plan:")
    for i, step in enumerate(plan["steps"], 1):
        print(f"{i}. {step}")