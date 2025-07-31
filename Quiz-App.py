# streamlit_app.py
import streamlit as st
import pandas as pd

# ----------------------------------------------------------
# 1.  Session-state helpers
# ----------------------------------------------------------
def init_state():
    if "idx" not in st.session_state:
        st.session_state.idx = 0
        st.session_state.score = 0
        st.session_state.answered = False
        st.session_state.choice = None
        st.session_state.questions = []

# ----------------------------------------------------------
# 2.  Upload CSV
# ----------------------------------------------------------
def load_questions(df: pd.DataFrame):
    required_cols = ["Topic", "Question", "Answer A", "Answer B", "Answer C", "Answer D", "Correct Answer"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        return False
    st.session_state.questions = df[required_cols].to_dict("records")
    return True

# ----------------------------------------------------------
# 3.  Quiz logic
# ----------------------------------------------------------
def show_question():
    q = st.session_state.questions[st.session_state.idx]
    st.markdown(f"**{q['Topic']}**")
    st.write(f"Question {st.session_state.idx + 1} / {len(st.session_state.questions)}")
    st.write(q["Question"])

    choice = st.radio(
        "Select an answer:",
        [q[f"Answer {c}"] for c in "ABCD"],
        key=f"q{st.session_state.idx}",
        index=None if not st.session_state.answered else "ABCD".index(st.session_state.choice)
    )

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        submitted = st.button("Submit", disabled=st.session_state.answered)
    with col2:
        next_btn = st.button("Next", disabled=not st.session_state.answered)

    if submitted and choice is not None:
        st.session_state.answered = True
        st.session_state.choice = choice
        if choice == q["Correct Answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. Correct: **{q['Correct Answer']}**")
        st.rerun()

    if next_btn and st.session_state.answered:
        if st.session_state.idx < len(st.session_state.questions) - 1:
            st.session_state.idx += 1
            st.session_state.answered = False
            st.session_state.choice = None
            st.rerun()
        else:
            st.balloons()
            st.write("### 🎉 Quiz finished!")
            st.write(f"**Your score: {st.session_state.score} / {len(st.session_state.questions)}**")
            if st.button("Restart Quiz"):
                for key in ["idx", "score", "answered", "choice", "questions"]:
                    st.session_state.pop(key, None)
                st.rerun()

# ----------------------------------------------------------
# 4.  Main app
# ----------------------------------------------------------
st.set_page_config(page_title="Quiz-App | CSV Upload", page_icon="📊")
st.title("📊 Upload your own CSV Quiz")

init_state()

if not st.session_state.questions:
    uploaded = st.file_uploader(
        "Choose a CSV file with the columns:\n"
        "**Topic** | **Question** | **Answer A** | **Answer B** | **Answer C** | **Answer D** | **Correct Answer**",
        type=["csv"]
    )
    if uploaded:
        df = pd.read_csv(uploaded)
        if load_questions(df):
            st.success(f"Loaded {len(st.session_state.questions)} questions.")
            st.rerun()
else:
    show_question()
