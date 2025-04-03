import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import re

# ✅ Configure API Key securely
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

leaderboard_file = "leaderboard.csv"

# ✅ Ensure the leaderboard file exists
if not os.path.exists(leaderboard_file):
    df_init = pd.DataFrame(columns=["Player", "Score"])
    df_init.to_csv(leaderboard_file, index=False)

def get_ai_response(prompt, fallback_message="⚠️ AI response unavailable. Please try again later."):
    """Generates AI response using Gemini 1.5 Pro."""
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if hasattr(response, "text") and response.text.strip() else fallback_message
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\n{fallback_message}"

def generate_ai_scenario():
    return get_ai_response("Create a realistic restaurant management scenario that requires decision-making.")

def get_ai_suggestions(scenario):
    prompt = f"""
    Scenario: {scenario}
    Generate 4 multiple-choice response options labeled A, B, C, and D.
    Ensure the options are realistic and applicable to restaurant management.
    """
    return get_ai_response(prompt)

def get_ai_feedback(scenario, user_choice):
    prompt = f"""
    Scenario: {scenario}
    User's Response: {user_choice}

    Provide:
    - A brief evaluation of the response
    - Pros and cons of the choice
    - A better alternative if applicable
    - A motivational message if they get it right!
    - Assign a score from 0 to 10 based on correctness (Ensure you return only one score at the end as 'Score: X').
    """
    feedback = get_ai_response(prompt)
    score = extract_score(feedback)
    return feedback, score

def get_ai_hint(scenario):
    prompt = f"Give a short hint for handling this restaurant scenario wisely: {scenario}"
    return get_ai_response(prompt)

def extract_score(feedback):
    match = re.search(r'Score:\s*(\d+)', feedback)
    return int(match.group(1)) if match else 0

def update_leaderboard(player, score):
    df = pd.read_csv(leaderboard_file)
    if player in df["Player"].values:
        df.loc[df["Player"] == player, "Score"] += score
    else:
        df = pd.concat([df, pd.DataFrame({"Player": [player], "Score": [score]})], ignore_index=True)
    df.to_csv(leaderboard_file, index=False)

def display_leaderboard():
    df = pd.read_csv(leaderboard_file).sort_values(by="Score", ascending=False)
    st.subheader("🏆 Leaderboard 🏆")
    st.dataframe(df)

# ✅ Streamlit UI
st.title("🍽️ AI-Powered Restaurant Challenge 🍽️")
player_name = st.text_input("🎮 Enter your name:")

if player_name:
    if "scenario" not in st.session_state:
        st.session_state.scenario = generate_ai_scenario()

    st.subheader("📌 AI-Generated Scenario:")
    st.write(st.session_state.scenario)

    hint = get_ai_hint(st.session_state.scenario)
    st.info(f"💡 AI Hint: {hint}")

    ai_suggestions = get_ai_suggestions(st.session_state.scenario)
    st.subheader("🤖 AI-Suggested Responses:")
    st.write(ai_suggestions)

    user_choice = st.radio("Select your choice:", ["A", "B", "C", "D"], key="user_choice")

    if st.button("Submit Choice"):
        ai_feedback, score = get_ai_feedback(st.session_state.scenario, user_choice)
        st.subheader("🤖 AI Feedback:")
        st.write(ai_feedback)
        st.success(f"🏅 Score Assigned by AI: {score} Points")

        update_leaderboard(player_name, score)
        display_leaderboard()

        # Generate new scenario and trigger re-run
        st.session_state.scenario = generate_ai_scenario()
        st.session_state.rerun = True #add this line.

    if "rerun" in st.session_state: # add this if condition.
        del st.session_state.rerun #delete the rerun key.
        st.rerun() #use st.rerun()
