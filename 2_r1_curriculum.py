# pages/2_r1_curriculum.py
import os
import pandas as pd
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import openai
from PIL import Image, UnidentifiedImageError

# --- Config ---
st.set_page_config(page_title="R1 Curriculum", layout="wide")
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# --- Load Case Data ---
def load_data():
    df = pd.read_csv("data/fluoro_ct_matches_with_unmatched.csv")
    if "R_level" not in df.columns:
        st.error("❌ 'R_level' column not found in the CSV. Available columns: " + ", ".join(df.columns))
        st.stop()
    df["label"] = df["image_filename"]
    return df[df["R_level"] == "R1"]

df = load_data()
fluoro_root = Path("1950 rad films")
ct_root = Path("fluoro_CT images")

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filters & Search")
query = st.sidebar.text_input("Search cases")
if query:
    df = df[df.apply(lambda row: query.lower() in str(row).lower(), axis=1)]

# --- Case Selection ---
st.title("📊 R1 Curriculum")
if len(df) == 0:
    st.warning("No cases match your filter/search.")
    st.stop()

label = st.selectbox("Select a case", df["label"])
row = df[df["label"] == label].iloc[0]

# --- Quiz Mode ---
st.subheader("🧪 Quiz Yourself")
if st.checkbox("Activate Quiz Mode"):
    st.markdown(f"**📋 Presentation:** {row.get('Presentation', 'N/A')}")
    guess = st.text_input("🤔 What's your diagnosis?")
    if guess:
        st.success(f"✅ Correct answer: {row.get('matched_ct_diagnosis', 'Unknown')}")
else:
    st.info("Toggle Quiz Mode to test yourself on this case.")

# --- Image Viewer ---
st.subheader("🖼️ Side-by-Side PACS-style Viewer")
fluoro_path = fluoro_root / row["image_filename"]
ct_path = ct_root / row["image_filename"]

col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🔎 Fluoroscopy")
    try:
        if fluoro_path.exists():
            st.image(str(fluoro_path), caption=row["image_filename"], use_container_width=True)
        else:
            st.info("No fluoro image found.")
    except UnidentifiedImageError:
        st.error(f"⚠️ Could not read fluoro image: {fluoro_path.name}")

with col2:
    st.markdown("### 🧠 CT")
    try:
        if ct_path.exists():
            st.image(str(ct_path), caption=row["image_filename"], use_container_width=True)
        else:
            st.info("No CT image found.")
    except UnidentifiedImageError:
        st.error(f"⚠️ Could not read CT image: {ct_path.name}")

# --- Educational Summary ---
with st.expander("📚 Educational Summary"):
    st.markdown(f"- **Teaching Point:** {row.get('Teaching_Pearls', 'N/A')}")
    st.markdown(f"- [🔗 Radiopaedia Fluoro Link]({row.get('url', '')})")
    st.markdown(f"- [🔗 Radiopaedia CT Link]({row.get('url_ct', '')})")

# --- AI Tutor Chat ---
mode = st.selectbox("Tutor Mode", ["Teaching", "Quiz Me", "Explain Findings", "Clinical Pearls"])
prompt_map = {
    "Teaching": "You are a tutor. Explain the fluoroscopy and CT findings step-by-step.",
    "Quiz Me": "You are a quiz master. Ask me questions based on this case.",
    "Explain Findings": "List the key radiologic signs in CT and Fluoroscopy for this case.",
    "Clinical Pearls": "Give 3 clinical pearls about this diagnosis and modality use."
}

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": prompt_map[mode]}]

st.subheader("💬 AI Tutor Chat")
question = st.text_input("Ask a question about this case...")
if st.button("Ask"):
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-4",
                messages=st.session_state.messages,
            )
            reply = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.markdown(f"**AI Response:** {reply}")
        except Exception as e:
            st.error(f"API Error: {e}")