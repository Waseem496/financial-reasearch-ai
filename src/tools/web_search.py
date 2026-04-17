import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


class WebSearchTool:
    def __init__(self):
        # 🔹 Load API key (local + Streamlit cloud)
        self.api_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")
        self.url = "https://api.tavily.com/search"

    def search(self, query: str):
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 3
        }

        try:
            response = requests.post(self.url, json=payload)

            # 🔴 Handle API failure
            if response.status_code != 200:
                return [{
                    "content": f"API Error: {response.status_code}",
                    "url": ""
                }]

            data = response.json()

            results = []

            for item in data.get("results", []):
                results.append({
                    "content": item.get("content", "").strip(),
                    "url": item.get("url", "")
                })

            # 🔴 If no results
            if not results:
                return [{
                    "content": "No results found",
                    "url": ""
                }]

            return results

        except Exception as e:
            return [{
                "content": f"Error during web search: {str(e)}",
                "url": ""
            }]


# 🔹 Standalone test
if __name__ == "__main__":
    tool = WebSearchTool()

    query = "Indian IT sector growth 2025"
    results = tool.search(query)

    print("\n🔍 Search Results:\n")

    for item in results:
        print(f"- {item['content']}")
        if item["url"]:
            print(f"  Source: {item['url']}")