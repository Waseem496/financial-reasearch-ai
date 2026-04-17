# 📊 Financial Research AI Agent

A deep research AI system that performs multi-step financial analysis using real-time web data, financial APIs, and document-based retrieval (RAG).

---

## 🚀 Overview

This application mimics a **financial research analyst**, capable of:

- Understanding user queries  
- Creating structured research plans  
- Performing multi-step analysis  
- Combining multiple data sources  
- Generating a final structured report with references  

---

## 🧠 Architecture
User Query
↓
Router (sector detection)
↓
Planner (research steps)
↓
User Approval
↓
Executor (deep research loop)
├── Web Search (Tavily)
├── RAG (Annual Reports)
├── Financial Data (yfinance)
↓
Synthesizer (final report)
↓
Streamlit UI


---
