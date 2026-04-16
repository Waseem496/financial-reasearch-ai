import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import uuid
from datetime import datetime

from src.core.router import QueryRouter
from src.research.planner import ResearchPlanner
from src.research.executor import ResearchExecutor
from src.research.synthesizer import ReportSynthesizer
from src.utils.charts import plot_stock_chart

router = QueryRouter()
planner = ResearchPlanner()
executor = ResearchExecutor()
synthesizer = ReportSynthesizer()

st.set_page_config(layout="wide", page_title="AI Research Agent")

# -------------------------
# CSS
# -------------------------
st.markdown("""
<style>
/* Sidebar styling */
[data-testid="stSidebar"] {
    background-color: #f8fafc;
}

/* Chat item row */
.chat-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 6px 4px;
    border-radius: 8px;
}

/* Chat title */
.chat-title {
    font-size: 13px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 140px;
}

/* Timestamp */
.chat-time {
    font-size: 10px;
    color: gray;
}

/* Buttons inline */
.chat-actions {
    display: flex;
    gap: 4px;
}

/* Reduce button size */
button[kind="secondary"] {
    padding: 2px 6px !important;
    font-size: 12px !important;
}
</style>
""", unsafe_allow_html=True)
# -------------------------
# SMALL TALK
# -------------------------
def handle_small_talk(query: str):
    q = query.lower().strip()
    if any(w in q for w in ["hi", "hello", "hey"]):
        return "👋 Hi! How can I assist you with financial research today?"
    if any(w in q for w in ["thanks", "thank you"]):
        return "😊 You're welcome! Let me know if you need any financial insights."
    if any(w in q for w in ["bye", "goodbye"]):
        return "👋 Goodbye! Have a great day."
    return None

# -------------------------
# ENTITY DETECTION
# -------------------------
def extract_company_or_sector(query: str):
    if not query:
        return None
    q = query.lower()
    mapping = {
        "infosys": "INFY.NS",
        "tcs": "TCS.NS",
        "wipro": "WIPRO.NS",
        "reliance": "RELIANCE.NS",
        "hdfc": "HDFCBANK.NS",
        "sun pharma": "SUNPHARMA.NS",
        "dr reddy": "DRREDDY.NS",
        "cipla": "CIPLA.NS",
    }
    for name, ticker in mapping.items():
        if name in q:
            return ticker
    if "pharma" in q:
        return "SUNPHARMA.NS"
    if "it" in q or "software" in q:
        return "INFY.NS"
    return None

# -------------------------
# SESSION INIT
# -------------------------
for key, default in [
    ("chats", {}),
    ("current_chat", None),
    ("search_query", ""),
    ("current_plan", None),
    ("agents", []),
    ("plan_approved", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<h2 style='text-align:center;'>🤖 Financial Deep Research AI</h2>
<p style='text-align:center;color:gray;'>AI-powered financial analysis</p>
""", unsafe_allow_html=True)

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.markdown("## 💬 Chats")
    search = st.text_input("🔍 Search chats", value=st.session_state.search_query)
    st.session_state.search_query = search

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.current_chat = None
        st.rerun()

    st.markdown("---")

    for chat_id, chat in list(st.session_state.chats.items()):

        if not chat["messages"]:
            continue

        if search and search.lower() not in chat["title"].lower():
            continue

        is_active = chat_id == st.session_state.current_chat

        col1, col2 = st.columns([0.75, 0.25])

    # 🔹 Chat Title
        with col1:
            if st.button(
                chat["title"][:30],
                key=f"chat_{chat_id}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_chat = chat_id
                st.rerun()

                st.markdown(f"<div class='chat-time'>{chat['timestamp']}</div>",
            unsafe_allow_html=True
        )

    # 🔹 Actions (Edit + Delete)
        with col2:
            action_col1, action_col2 = st.columns(2)

            with action_col1:
                if st.button("✏️", key=f"rename_{chat_id}"):
                    st.session_state[f"rename_{chat_id}"] = True

            with action_col2:
                if st.button("🗑️", key=f"del_{chat_id}"):
                    del st.session_state.chats[chat_id]
                    if st.session_state.current_chat == chat_id:
                        st.session_state.current_chat = None
                    st.rerun()

    # 🔹 Rename input
        if st.session_state.get(f"rename_{chat_id}", False):
            new_name = st.text_input("Rename", key=f"input_{chat_id}")
            if new_name:
                st.session_state.chats[chat_id]["title"] = new_name
                st.session_state[f"rename_{chat_id}"] = False
                st.rerun()

        
        st.markdown("---")
# -------------------------
# DISPLAY EXISTING MESSAGES
# -------------------------
if st.session_state.current_chat:
    for msg in st.session_state.chats[st.session_state.current_chat]["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -------------------------
# CHAT INPUT
# -------------------------
query = st.chat_input("Ask a financial question...")

if query:
    # Small talk shortcut
    small_talk_response = handle_small_talk(query)
    if small_talk_response:
        if st.session_state.current_chat is None:
            chat_id = str(uuid.uuid4())
            st.session_state.current_chat = chat_id
            st.session_state.chats[chat_id] = {
                "title": query[:40],
                "messages": [],
                "timestamp": datetime.now().strftime("%d %b %H:%M"),
            }
        chat_data = st.session_state.chats[st.session_state.current_chat]
        chat_data["messages"].append({"role": "user", "content": query})
        with st.chat_message("assistant"):
            st.markdown(small_talk_response)
        chat_data["messages"].append({"role": "assistant", "content": small_talk_response})
        st.stop()

    # Minimum length guard
    if len(query.split()) < 3:
        st.info("💡 Try something like: 'Analyze Infosys financial performance 2024'")
        st.stop()

    # Create new chat if needed
    if st.session_state.current_chat is None:
        chat_id = str(uuid.uuid4())
        st.session_state.current_chat = chat_id
        st.session_state.chats[chat_id] = {
            "title": query[:40],
            "messages": [],
            "timestamp": datetime.now().strftime("%d %b %H:%M"),
        }

    chat_data = st.session_state.chats[st.session_state.current_chat]
    chat_data["messages"].append({"role": "user", "content": query})

    # Route and plan — store in session state
    routing = router.route(query)
    agents = routing["agents"]
    plan = planner.create_plan(query, routing, agents[0])

    st.session_state.current_plan = plan
    st.session_state.agents = agents
    st.session_state.plan_approved = False

# -------------------------
# PLAN APPROVAL
# -------------------------
if st.session_state.current_plan and not st.session_state.plan_approved:
    with st.chat_message("assistant"):
        st.markdown("## 🧠 Research Plan")
        for i, step in enumerate(st.session_state.current_plan["steps"], 1):
            st.markdown(f"**{i}.** {step}")
        st.markdown("---")
        st.markdown("👉 Approve to start deep research")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve & Run"):
                st.session_state.plan_approved = True
                st.rerun()
        with col2:
            if st.button("✏️ Modify Query"):
                st.session_state.current_plan = None
                st.session_state.plan_approved = False
                st.info("Modify your query and try again")

# -------------------------
# EXECUTION — runs exactly once
# -------------------------
# -------------------------
# EXECUTION — CLEAN UI
# -------------------------
if st.session_state.current_plan and st.session_state.plan_approved:

    plan = st.session_state.current_plan
    agents = st.session_state.agents

    if not agents:
        st.error("⚠️ No agent found. Please try again.")
        st.session_state.current_plan = None
        st.session_state.plan_approved = False
        st.stop()

    chat_data = st.session_state.chats[st.session_state.current_chat]

    last_user_query = next(
        (m["content"] for m in reversed(chat_data["messages"]) if m["role"] == "user"),
        None,
    )

    # 🔥 AI message (ONLY status)
    with st.chat_message("assistant"):
        st.markdown("🚀 Running deep research... please wait")

    progress = st.progress(0)
    status = st.empty()

    try:
        result = executor.execute(plan)
    except Exception as e:
        st.error("❌ Research failed")
        st.code(str(e))
        st.session_state.current_plan = None
        st.session_state.plan_approved = False
        st.session_state.agents = []
        st.stop()

    steps = result.get("steps", [])
    total_steps = max(len(steps), 1)

    # -------------------------
    # 🔍 Research Steps (SEPARATE SECTION)
    # -------------------------
    st.markdown("## 🔍 Research Steps")

    for i, step in enumerate(steps):
        progress.progress((i + 1) / total_steps)
        status.markdown(f"🔄 Step {i + 1}: {step.get('query')}")

        with st.expander(f"Step {i + 1} Details"):
            st.write("**Query:**", step.get("query"))

            insights = step.get("insights", [])
            if isinstance(insights, str):
                insights = [insights]

            for ins in insights:
                st.markdown(f"- {ins}")

    status.markdown("✅ Research completed")

    # -------------------------
    # 📄 FINAL OUTPUT (TABS OUTSIDE CHAT)
    # -------------------------
    report = synthesizer.generate_report(result)

    st.markdown("## 📊 Final Output")

    tab1, tab2 = st.tabs(["📄 Report", "📊 Charts"])

    with tab1:
        if report:
            st.markdown(report)
        else:
            st.warning("⚠️ Report not generated")

    with tab2:
        ticker = extract_company_or_sector(last_user_query)

        if ticker:
            st.markdown(f"### 📊 Stock Analysis: {ticker}")

            chart = plot_stock_chart(ticker)
            if chart:
                st.pyplot(chart)
            else:
                st.warning("No data found for this ticker.")
        else:
            st.info("Try asking about companies like Infosys, Sun Pharma, TCS, etc.")

    # -------------------------
    # SAVE RESPONSE
    # -------------------------
    chat_data["messages"].append({
        "role": "assistant",
        "content": report
    })

    st.session_state.current_plan = None
    st.session_state.plan_approved = False
    st.session_state.agents = []