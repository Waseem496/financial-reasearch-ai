from typing import Dict, List
from unittest import result
from src.tools.web_search import WebSearchTool


class ResearchExecutor:
    def __init__(self):
        self.results = []
        self.web_search = WebSearchTool()  


    def execute(self, plan: Dict, max_steps: int = 8) -> Dict:
        steps = plan.get("steps", [])

        print("\n🚀 Starting Research Execution...\n")

    # 🔥 RESET results every run
        self.results = []

        for i, step in enumerate(steps[:max_steps], 1):

            print(f"🔍 Step {i}: {step}")

        # 🔥 Create better query
            refined_query = f"{plan.get('query')} {step}"

        # 🔥 Call web search
            result = self.run_step(refined_query)

            self.results.append({
            "step": step,
            "query": refined_query,
            "result": result
        })

            print(f"✅ Result: {result}\n")

        return {
        "query": plan.get("query"),
        "results": self.results
    }

    def run_step(self, query: str) -> list:
        raw_data = self.web_search.search(query)

        if not raw_data:
            return ["No data found"]

    # 🔥 Clean + extract insights
        lines = raw_data.split("\n")

        insights = []
        for line in lines:
            clean = line.strip()

        # remove junk + short lines
            if len(clean) > 50:
                insights.append(clean)

    # limit output
        return insights[:5]
    

if __name__ == "__main__":
    from src.core.router import QueryRouter
    from src.research.planner import ResearchPlanner

    router = QueryRouter()
    planner = ResearchPlanner()
    executor = ResearchExecutor()

    query = "Analyze IT sector in India"

    routing = router.route(query)
    plan = planner.create_plan(query, routing)

    execution_result = executor.execute(plan)

    print("\n📊 FINAL RESULTS:")
    for item in execution_result["results"]:
        print(f"- {item['step']}: {item['result']}")