import streamlit as st
import google.generativeai as genai

# ✅ Secure API Key Setup
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Add your key to Streamlit Cloud → Settings → Secrets.")
    st.stop()

# 🔁 Utility: AI response handler
def get_ai_response(prompt, fallback="⚠️ AI response unavailable. Try again later."):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if hasattr(response, "text") and response.text.strip() else fallback
    except Exception as e:
        return f"⚠️ Error: {str(e)}\n{fallback}"

# 🔁 Scenario Generators
def generate_case_study(module_topic):
    return get_ai_response(f"Create a detailed restaurant management case study for the topic: {module_topic}. Include realistic operational and decision-making challenges.")

def generate_hint(scenario):
    return get_ai_response(f"Provide a short hint to handle this restaurant scenario:\n\n{scenario}")

def generate_guidance(scenario):
    return get_ai_response(f"""
    Restaurant Management Scenario:
    {scenario}

    You are a seasoned restaurant consultant. Provide:
    - Structured approach to solve this case
    - Key decisions to consider
    - Best practices
    - Pitfalls to avoid
    - A reflective question for managers
    """)

def generate_summary_notes(topic):
    return get_ai_response(f"Summarize the key principles and strategies for restaurant managers under the topic: {topic}. Use bullet points.")

# ✅ Master Course Structure
modules = {
    "Introduction to Smart Restaurant Management": "Overview of responsibilities, goals, and smart tools for restaurant managers.",
    "Staffing & Team Leadership": "Hiring, training, scheduling, motivation, conflict resolution.",
    "Customer Experience & Satisfaction": "Handling complaints, creating loyalty, ambiance design.",
    "Inventory & Supply Chain": "Optimizing ordering, minimizing waste, vendor management.",
    "AI & Technology Integration": "Using AI tools for menus, personalization, analytics, operations.",
    "Financial Planning & Profitability": "Budgeting, pricing, cost control, revenue growth strategies.",
    "Event & Promotion Strategy": "Event planning, marketing campaigns, community engagement.",
    "Sustainability & Waste Reduction": "Eco-friendly practices, waste audits, innovation.",
}

# ✅ UI
st.title("🎓 Restaurant Manager Master Course (AI-Powered)")
st.sidebar.header("🗂️ Course Modules")

selected_module = st.sidebar.selectbox("Select a Module", list(modules.keys()))

st.subheader(f"📘 {selected_module}")
st.markdown(f"_{modules[selected_module]}_")

# ✅ Case Study Generator
if st.button("🔄 Generate Case Study"):
    st.session_state.case_study = generate_case_study(selected_module)

if "case_study" in st.session_state:
    st.markdown("---")
    st.subheader("📌 Case Study")
    st.write(st.session_state.case_study)

    st.subheader("💡 Hint from AI")
    st.info(generate_hint(st.session_state.case_study))

    st.subheader("🧠 AI Expert Strategy")
    st.write(generate_guidance(st.session_state.case_study))

    st.subheader("📝 Reflection Journal")
    user_reflection = st.text_area("What would you do in this situation? How does it relate to your experience?", height=150)

    if user_reflection:
        st.success("Reflection saved locally for now. Export feature coming soon!")

    st.subheader("📒 Summary Notes")
    st.markdown(generate_summary_notes(selected_module))

# 🚀 Coming Soon:
st.sidebar.markdown("---")
st.sidebar.info("Coming Soon:\n- 🧾 Certification Quiz\n- 📥 PDF Export\n- 💬 Peer Discussion")

