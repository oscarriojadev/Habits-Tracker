# quiz.py
import streamlit as st

# ----------  dummy data so the script can run stand-alone  ----------
if "questions" not in st.session_state:
    st.session_state.questions = [
        {
            "Topic": "Python",
            "Question": "What does `len()` return?",
            "Answer A": "Length",
            "Answer B": "Error",
            "Answer C": "None",
            "Answer D": "Zero",
            "Correct Answer": "Length",
        },
        {
            "Topic": "Streamlit",
            "Question": "Which widget shows balloons?",
            "Answer A": "st.balloons()",
            "Answer B": "st.party()",
            "Answer C": "st.celebrate()",
            "Answer D": "st.fireworks()",
            "Correct Answer": "st.balloons()",
        },
    ]
# --------------------------------------------------------------------

# initialise session state
for k, v in {"idx": 0, "score": 0, "answered": False}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ----------  show the question  ----------
idx = st.session_state.idx
q   = st.session_state.questions[idx]

st.markdown(f"**{q['Topic']}**")
st.write(f"Question {idx + 1} / {len(st.session_state.questions)}")
st.write(q["Question"])

choices = [q["Answer A"], q["Answer B"], q["Answer C"], q["Answer D"]]

# use a *stable* key so Streamlit can remember the radio selection
selected = st.radio(
    "Select an answer:",
    choices,
    key="current_choice",
    index=None,                         # no pre-selection
    disabled=st.session_state.answered
)

col1, col2, _ = st.columns([1, 1, 1])

with col1:
    submitted = st.button("Submit", disabled=st.session_state.answered)

with col2:
    next_btn = st.button("Next", disabled=not st.session_state.answered)

# ----------  Submit logic  ----------
if submitted and selected is not None:
    st.session_state.answered = True
    st.session_state.choice = selected

    if selected == q["Correct Answer"]:
        st.session_state.score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect.")
    st.info(f"**Correct answer:** {q['Correct Answer']}")
    #  ↓↓↓  DON’T call st.rerun() here

# ----------  Next / Finish logic  ----------
if next_btn:
    if idx < len(st.session_state.questions) - 1:
        st.session_state.idx += 1
        st.session_state.answered = False
        st.session_state.pop("current_choice", None)
        st.rerun()
    else:
        st.balloons()
        st.write("### 🎉 Quiz finished!")
        st.write(f"**Your score: {st.session_state.score} / {len(st.session_state.questions)}**")
        if st.button("Restart Quiz"):
            for k in ("idx", "score", "answered", "current_choice", "questions"):
                st.session_state.pop(k, None)
            st.rerun()
