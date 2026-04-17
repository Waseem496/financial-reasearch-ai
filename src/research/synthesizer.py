from typing import Dict
import os

from src.schemas import report


class ReportSynthesizer:
    def generate_report(self, execution_result: Dict) -> str:

        if not execution_result:
            return "No execution result found."

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

            insights = item.get("result") or item.get("insights") or []

        # 🔥 HANDLE LIST OF DICTS (WITH LINKS)
            if isinstance(insights, list):

                for ins in insights:

                # Case 1: dict with link
                    if isinstance(ins, dict):
                        text = ins.get("text", "")
                        url = ins.get("url", "")

                        report.append(f"- {text}")

                        if url:
                            report.append(f"<a href='{url}' target='_blank'>Read more →</a>\n")

                # Case 2: plain string
                        else:
                            report.append(f"- {ins}\n")

                    else:
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