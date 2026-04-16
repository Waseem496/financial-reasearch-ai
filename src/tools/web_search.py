import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()


class WebSearchTool:
    def __init__(self):

        self.api_key = os.getenv("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY")
        self.url = "https://api.tavily.com/search"

    def search(self, query: str) -> str:
        payload = {
            "api_key": self.api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 3
        }

        try:
            response = requests.post(self.url, json=payload)
            data = response.json()

            results = []

            for item in data.get("results", []):
                results.append(item.get("content", ""))

            return "\n".join(results)

        except Exception as e:
            return f"Error during web search: {str(e)}"


if __name__ == "__main__":
    tool = WebSearchTool()

    query = "Indian IT sector growth 2025"
    result = tool.search(query)

    print("Search Results:\n")
    print(result)