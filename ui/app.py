import streamlit as st
import requests

st.title("Agent Marketplace")

# -------------------
# Agent Directory
# -------------------
agents = requests.get("http://localhost:8000/api/agents/list").json()

st.header("Agent Directory")
for agent in agents:
    st.write(f"{agent['name']} → {agent['capabilities']}")

# -------------------
# Send Task
# -------------------
st.header("Send Task")

capability = st.selectbox("Capability", ["math", "summarization", "search"])

user_input = st.text_area("Enter your input")

# Optional params
precision = st.number_input("Precision (math only)", value=2)

if st.button("Send"):

    payload = {
        "capability": capability,
        "input": {
            "text": user_input,
            "params": {
                "precision": precision
            }
        },
        "context": {
            "source": "streamlit_ui"
        }
    }

    res = requests.post(
        "http://localhost:8000/api/orchestrate/",
        json=payload
    )

    st.json(res.json())

# -------------------
# Task History
# -------------------
st.header("Task History")

tasks = requests.get("http://localhost:8000/api/tasks/").json()

for t in tasks:
    st.write(f"Task: {t['task_id']}")
    st.write(f"Input: {t['input']}")
    st.write(f"Result: {t['result']}")
    st.write("---")