from typing import Dict, List
from src.tools.web_search import WebSearchTool


class ResearchExecutor:
    def __init__(self):
        self.results = []
        self.web_search = WebSearchTool()

    def execute(self, plan: Dict, max_steps: int = 8) -> Dict:
        steps = plan.get("steps", [])

        print("\n🚀 Starting Research Execution...\n")

        # 🔥 Reset results every run
        self.results = []

        for i, step in enumerate(steps[:max_steps], 1):

            print(f"🔍 Step {i}: {step}")

            # 🔥 Refined query
            refined_query = f"{plan.get('query')} {step}"

            # 🔥 Run step
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

    def run_step(self, query: str) -> List[Dict]:
        results = self.web_search.search(query)

        if not results:
            return [{"text": "No data found", "url": ""}]

        insights = []

        for item in results:

            # ✅ Case 1: Proper dict from API
            if isinstance(item, dict):
                content = item.get("content", "").strip()
                url = item.get("url", "")

            # ✅ Case 2: fallback (string)
            else:
                content = str(item).strip()
                url = ""

            if len(content) > 50:
                insights.append({
                    "text": content,
                    "url": url
                })

        return insights[:5]


# 🔹 Standalone test
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
        print(f"\n🔹 {item['step']}")
        for res in item["result"]:
            print(f"- {res['text']}")
            if res["url"]:
                print(f"  Source: {res['url']}")