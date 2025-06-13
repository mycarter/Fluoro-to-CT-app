import streamlit as st

# ✅ Must be the first Streamlit command
st.set_page_config(page_title="Fluoro Bootcamp", layout="wide")

# Sidebar navigation
st.sidebar.title("🧠 Fluoro Bootcamp")
page = st.sidebar.radio("Navigate", [
    "🏠 Home",
    "📘 About Fluoroscopy",
    "📊 R1 Curriculum",
    "📊 R2 Curriculum",
    "📊 R3 Curriculum",
    "📚 Case Library",
    "✅ Progress Tracker",
    "🎓 Faculty Dashboard"
])

# Page routing
if page == "🏠 Home":
    st.title("🩻 Welcome to Learning Fluoroscopy")
    st.markdown("""
    This curriculum is designed to help radiology residents build confidence in reading fluoroscopic studies
    with CT correlation and interactive AI tools.
    
    ### 🔍 What You’ll Learn:
    - Fluoro study types: Esophagram, Upper GI, Barium Enema, etc.
    - How to recognize key pathology patterns
    - How CT correlates with fluoroscopy findings
    - Dictation practice and AI feedback
    """)
elif page == "📘 About Fluoroscopy":
    st.header("About Fluoroscopy")
    st.write("This is where you’ll learn what fluoroscopy is, its clinical value, and basics for residents.")

elif page == "📊 R1 Curriculum":
    st.header("R1 Curriculum")
    st.write("Classic pathology exposure, paired with CT. Focused on early recognition and confidence.")

# You can add other elif blocks here for the rest of the pages
