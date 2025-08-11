# streamlit_app.py

"""
To Run:
1. Activate virtual environment and/or install pip install -r requirements.txt
2. uvicorn score_headlines_api:app --host 0.0.0.0 --port 8017
3. streamlit run streamlit_app.py --server.port 9017
"""

import streamlit as st
import requests

# Set Streamlit page config
st.set_page_config(page_title="Headline Sentiment Scorer", layout="centered")

st.title("📰 Headline Sentiment Scorer")
st.markdown("Enter news headlines below. Click **Score Headlines** to see their sentiment prediction.")

# Initialize session state for headline list
if "headlines" not in st.session_state:
    st.session_state.headlines = [""]

# Editable text boxes for headlines
for i, headline in enumerate(st.session_state.headlines):
    st.session_state.headlines[i] = st.text_input(f"Headline {i+1}", value=headline, key=f"headline_{i}")

# Buttons to add or remove headline input fields
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Add Headline"):
        st.session_state.headlines.append("")
with col2:
    if st.button("Remove Last Headline"):
        if len(st.session_state.headlines) > 1:
            st.session_state.headlines.pop()

st.markdown("---")

# Button to submit headlines for sentiment scoring
if st.button("Score Headlines"):
    # Prepare request
    api_url = "http://localhost:8017/score_headlines"
    headlines_to_send = [h.strip() for h in st.session_state.headlines if h.strip()]

    if not headlines_to_send:
        st.warning("Please enter at least one valid headline.")
    else:
        try:
            response = requests.post(api_url, json={"headlines": headlines_to_send})
            response.raise_for_status()
            result = response.json()
            labels = result.get("labels", [])

            st.success("Sentiment Results:")
            for i, (headline, label) in enumerate(zip(headlines_to_send, labels)):
                color = {
                    "Optimistic": "🟢",
                    "Neutral": "⚪",
                    "Pessimistic": "🔴"
                }.get(label, "❓")
                st.markdown(f"**{headline}** → {color} **{label}**")

        except requests.exceptions.RequestException as e:
            st.error(f"❌ Could not reach API: {e}")
        except Exception as e:
            st.error(f"❌ Error processing response: {e}")