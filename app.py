import streamlit as st
import google.generativeai as genai

# ✅ Configure API Key
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

def get_ai_response(prompt, fallback_message="⚠️ AI response unavailable. Please try again later."):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if hasattr(response, "text") and response.text.strip() else fallback_message
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\n{fallback_message}"

# ---- AI Generation Functions ----
def generate_case_study():
    return get_ai_response("Create a realistic and complex restaurant management scenario involving staffing, inventory, and customer satisfaction for training purposes.")

def generate_hint(scenario):
    return get_ai_response(f"Provide a brief and practical hint to handle the following restaurant management case study:\n\n{scenario}")

def generate_guidance(scenario):
    return get_ai_response(f"""
    Scenario: {scenario}
    Give a structured manager-level solution including:
    - Key decisions to consider
    - Strategic actions
    - Best practices
    - What to avoid
    """)

def generate_test_question():
    return get_ai_response("Generate a test case scenario for restaurant managers with a clear challenge. Ask the user how they would respond.")

def evaluate_test_response(question, user_answer):
    prompt = f"""
    Test Scenario: {question}
    User's Response: {user_answer}

    As a restaurant management expert, evaluate their answer. Provide:
    - Evaluation summary
    - Strengths in their response
    - Areas for improvement
    - Final performance feedback
    - Score out of 10
    """
    return get_ai_response(prompt)

# ---- Streamlit App UI ----
st.set_page_config(page_title="Manager Upliftment Course", layout="centered")
st.title("🚀 Restaurant Manager Upliftment Course with Generative AI")

if "step" not in st.session_state:
    st.session_state.step = 0
if "case_studies" not in st.session_state:
    st.session_state.case_studies = []
if "test_question" not in st.session_state:
    st.session_state.test_question = ""
if "user_answer" not in st.session_state:
    st.session_state.user_answer = ""

# ---- Step 0: Welcome ----
if st.session_state.step == 0:
    st.header("Welcome to the AI-Powered Manager Upliftment Course")
    st.markdown("""
    This short course uses Generative AI to:
    - 🧠 Challenge your decision-making
    - 📚 Sharpen your strategic thinking
    - ✅ Help you grow as a better restaurant manager
    
    You'll go through **3 real-world scenarios** with AI guidance and complete a final **test** to receive personalized feedback.
    """)
    if st.button("Start Course"):
        st.session_state.step = 1

# ---- Step 1–3: Case Studies ----
elif 1 <= st.session_state.step <= 3:
    case_index = st.session_state.step
    st.header(f"📘 Module {case_index}: AI-Powered Case Study")
    
    if len(st.session_state.case_studies) < case_index:
        scenario = generate_case_study()
        hint = generate_hint(scenario)
        guidance = generate_guidance(scenario)
        st.session_state.case_studies.append((scenario, hint, guidance))
    else:
        scenario, hint, guidance = st.session_state.case_studies[case_index - 1]

    st.subheader("📌 Scenario")
    st.write(scenario)
    
    st.subheader("💡 Hint")
    st.info(hint)
    
    st.subheader("🧭 Strategic Guidance")
    st.write(guidance)

    if st.button("Next Module"):
        st.session_state.step += 1

# ---- Step 4: Final Test ----
elif st.session_state.step == 4:
    st.header("📝 Final Test: Apply Your Skills")
    
    if not st.session_state.test_question:
        st.session_state.test_question = generate_test_question()

    st.subheader("📌 Test Scenario")
    st.write(st.session_state.test_question)

    st.session_state.user_answer = st.text_area("✍️ How would you handle this situation?", st.session_state.user_answer)

    if st.button("Submit Test Response"):
        st.session_state.step += 1

# ---- Step 5: Performance Feedback ----
elif st.session_state.step == 5:
    st.header("📊 Your Performance Feedback")
    with st.spinner("Evaluating your response..."):
        feedback = evaluate_test_response(st.session_state.test_question, st.session_state.user_answer)
    st.write(feedback)

    if st.button("🔄 Restart Course"):
        st.session_state.step = 0
        st.session_state.case_studies = []
        st.session_state.test_question = ""
        st.session_state.user_answer = ""
