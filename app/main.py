import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import uuid
from datetime import datetime

# 🔹 Imports
from src.core.router import QueryRouter
from src.research.planner import ResearchPlanner
from src.research.executor import ResearchExecutor
from src.research.synthesizer import ReportSynthesizer
from src.utils.charts import plot_stock_chart

# 🔹 Initialize components
router = QueryRouter()
planner = ResearchPlanner()
executor = ResearchExecutor()
synthesizer = ReportSynthesizer()

# 🔹 Session state init
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "search_query" not in st.session_state:
    st.session_state.search_query = ""

if "active_menu" not in st.session_state:
    st.session_state.active_menu = None

# 🔹 Page config
st.set_page_config(page_title="Financial AI", layout="wide")

# 🔹 CSS
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: #f5f7fa;
}
.chat-item {
    background: #e9eef3;
    padding: 8px;
    border-radius: 10px;
    margin-bottom: 6px;
}
.chat-active {
    background: #dbeafe;
}
.chat-time {
    font-size: 10px;
    color: gray;
}
h1 { font-size: 24px !important; font-weight: bold; }
h2 { font-size: 22px !important; font-weight: bold; }
p { font-size: 20px !important; }
</style>
""", unsafe_allow_html=True)

# =======================
# 🔹 SIDEBAR
# =======================
with st.sidebar:

    st.markdown("### Chats")

    search = st.text_input("Search chats...", value=st.session_state.search_query)
    st.session_state.search_query = search

    if st.button("New Chat", use_container_width=True):
        st.session_state.current_chat = None
        st.rerun()

    st.markdown("---")

    for chat_id, chat in st.session_state.chats.items():

        if not chat["messages"] and chat.get("status") != "running":
            continue

        if search and search.lower() not in chat["title"].lower():
            continue

        is_active = chat_id == st.session_state.current_chat
        bg_class = "chat-item chat-active" if is_active else "chat-item"

        status = chat.get("status", "done")
        status_text = "⏳ Researching..." if status == "running" else chat["timestamp"]

        col1, col2 = st.columns([0.85, 0.15])

        # 🔹 Chat click
        with col1:
            if st.button(chat["title"][:30], key=f"chat_btn_{chat_id}", use_container_width=True):
                st.session_state.current_chat = chat_id
                st.session_state.active_menu = None
                st.rerun()

            st.markdown(
                f"<div class='{bg_class}'><div class='chat-time'>{status_text}</div></div>",
                unsafe_allow_html=True
            )

        # 🔹 Three dots
        with col2:
            if st.button("⋯", key=f"menu_btn_{chat_id}"):
                if st.session_state.active_menu == chat_id:
                    st.session_state.active_menu = None
                else:
                    st.session_state.active_menu = chat_id

        # 🔽 Dropdown actions
        if st.session_state.active_menu == chat_id:

            st.caption("Actions")

            a1, a2 = st.columns(2)

            with a1:
                if st.button("Edit", key=f"edit_btn_{chat_id}"):
                    st.session_state[f"rename_{chat_id}"] = True
                    st.session_state.active_menu = None

            with a2:
                if st.button("Delete", key=f"delete_btn_{chat_id}"):
                    del st.session_state.chats[chat_id]

                    if st.session_state.current_chat == chat_id:
                        st.session_state.current_chat = None

                    st.session_state.active_menu = None
                    st.rerun()

        # 🔹 Rename
        if st.session_state.get(f"rename_{chat_id}", False):

            new_name = st.text_input("Rename chat", key=f"input_{chat_id}")

            if new_name:
                st.session_state.chats[chat_id]["title"] = new_name
                st.session_state[f"rename_{chat_id}"] = False
                st.rerun()

# =======================
# 🔹 MAIN UI
# =======================

st.title("Financial Research AI")

query = st.chat_input("Ask a financial question...")

# 🔹 Create chat instantly
if query:
    chat_id = str(uuid.uuid4())

    st.session_state.chats[chat_id] = {
        "title": query,
        "messages": [],
        "timestamp": datetime.now().strftime("%d %b %H:%M"),
        "status": "running"   # 🔥 important
    }

    st.session_state.current_chat = chat_id
    st.rerun()

# 🔹 Safety checks
if st.session_state.current_chat is None:
    st.info("Start a new chat to begin")
    st.stop()

if st.session_state.current_chat not in st.session_state.chats:
    st.session_state.current_chat = None
    st.warning("Chat not found")
    st.stop()

chat_data = st.session_state.chats[st.session_state.current_chat]

# =======================
# 🔹 RUN PIPELINE
# =======================

if not chat_data["messages"]:

    user_query = chat_data["title"]

    with st.spinner("Running deep research..."):

        route = router.route(user_query)
        plan = planner.create_plan(user_query, route)
        result = executor.execute(plan)
        report = synthesizer.generate_report(result)

        chat_data["messages"].append({
            "query": user_query,
            "report": report
        })

        chat_data["status"] = "done"

        st.rerun()

# =======================
# 🔹 DISPLAY
# =======================

for msg in chat_data["messages"]:

    st.markdown(msg["report"], unsafe_allow_html=True)

    # 🔹 Example chart
    if "infosys" in msg["query"].lower():
        chart = plot_stock_chart("INFY.NS")

        if chart:
            st.pyplot(chart)
        else:
            st.warning("Stock data not available")

# 🔹 Footer
st.markdown("---")
st.caption("⚠️ This is for educational purposes only. Not financial advice.")