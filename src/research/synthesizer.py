from typing import Dict
import os


class ReportSynthesizer:
    def generate_report(self, execution_result: Dict) -> str:

        if not execution_result:
            return "⚠️ No execution result found."

        # ✅ Support BOTH formats
        results = (
            execution_result.get("results")
            or execution_result.get("steps")
            or []
        )

        query = execution_result.get("query") or "Financial Analysis"

        if not results:
            return "⚠️ No insights generated from research."

        report = []

        report.append("# 📊 Financial Research Report\n")
        report.append(f"## Query: {query}\n")

        report.append("## 🧾 Executive Summary\n")
        report.append(
            "This report provides a comprehensive analysis based on multi-step research combining web and document insights.\n"
        )

        report.append("## 🔍 Detailed Findings\n")

        for i, item in enumerate(results, 1):

            step_title = item.get("step") or item.get("query") or f"Step {i}"
            report.append(f"### {step_title}\n")

            query_used = item.get("query_used") or item.get("query") or "N/A"
            report.append(f"**Query Used:** {query_used}\n")

            insights = item.get("result") or item.get("insights") or ""

            if isinstance(insights, list):
                insights = "\n".join(f"- {ins}" for ins in insights)

            report.append(f"{insights}\n")

        report.append("## 📈 Conclusion\n")
        report.append(
            "The analysis indicates key growth trends, competitive positioning, and potential risks in the sector/company.\n"
        )

        return "\n".join(report)


    def save_report(self, report: str, filename: str = "report.txt"):
        os.makedirs("output/reports", exist_ok=True)

        file_path = os.path.join("output/reports", filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Report saved at: {file_path}")