import streamlit as st
import requests

st.title(" A2A Agent Marketplace")

# SELECT TASK TYPE
st.header("Choose Task")

capability = st.selectbox(
    "Select Capability",
    ["math", "summarization", "search"]
)

user_input = st.text_area("Enter your input")

# SEND TASK
if st.button("Submit Task"):

    if not user_input.strip():
        st.warning("Please enter input")
    else:
        payload = {
            "capability": capability,
            "input": {
                "text": user_input
            },
            "context": {}
        }

        try:
            res = requests.post(
                "http://127.0.0.1:8000/api/orchestrate/",
                json=payload
            )

            if res.status_code != 200:
                st.error(f"Server error: {res.status_code}")
            else:
                data = res.json()

                # HANDLE RESPONSE
                if data.get("status") == "error":
                    st.error(data.get("error"))

                else:
                    result = data.get("result")
                    st.subheader("Result")

                    # SEARCH OUTPUT
                    if capability == "search" and isinstance(result, list):
                        for item in result:
                            st.markdown(f"### 🔗 {item.get('title')}")
                            st.write(item.get("snippet"))
                            st.markdown(f"[Open Link]({item.get('link')})")
                            st.write("---")

                    #  MATH OUTPUT
                    elif capability == "math":
                        st.success(result)

                    # SUMMARIZATION OUTPUT
                    elif capability == "summarization":
                        st.info(result)

                    else:
                        st.write(result)

        except Exception as e:
            st.error(f"Request failed: {e}")