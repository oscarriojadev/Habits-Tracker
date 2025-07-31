# quiz.py
import streamlit as st

# -------------------- dummy data so you can test immediately -----------------
if "questions" not in st.session_state:
    st.session_state.questions = [
        {
            "Topic": "Python",
            "Question": "What does `len()` return for `[1, 2, 3]`?",
            "Answer A": "3",
            "Answer B": "2",
            "Answer C": "Error",
            "Answer D": "None",
            "Correct Answer": "3",
        },
        {
            "Topic": "Streamlit",
            "Question": "Which widget shows balloons?",
            "Answer A": "st.balloons()",
            "Answer B": "st.party()",
            "Answer C": "st.celebrate()",
            "Answer D": "st.fireworks()",
            "Correct Answer": "st.balloons()",
        }
    ]
# -----------------------------------------------------------------------------

# initialise session-state variables
for key, default in {"idx": 0, "score": 0, "answered": False}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# -------------------- UI ------------------------------------------------------
idx = st.session_state.idx
q   = st.session_state.questions[idx]

st.markdown(f"**{q['Topic']}**")
st.write(f"Question {idx + 1} / {len(st.session_state.questions)}")
st.write(q["Question"])

choices = [q["Answer A"], q["Answer B"], q["Answer C"], q["Answer D"]]

# stable key so Streamlit can remember the selection
selected = st.radio(
    "Select an answer:",
    choices,
    key="current_choice",
    index=None,                    # no pre-selection
    disabled=st.session_state.answered
)

col1, col2, _ = st.columns([1, 1, 1])

with col1:
    submitted = st.button(
        "Submit",
        disabled=st.session_state.answered,
        key=f"submit_{idx}"        # unique key prevents duplicate-widget error
    )

with col2:
    next_btn = st.button(
        "Next",
        disabled=not st.session_state.answered,
        key=f"next_{idx}"
    )

# -------------------- Submit logic -------------------------------------------
if submitted:
    choice = st.session_state.get("current_choice")
    if choice is None:
        st.warning("Please choose an answer.")
        st.stop()

    st.session_state.answered = True
    if choice == q["Correct Answer"]:
        st.session_state.score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect")
    st.info(f"**Correct answer:** {q['Correct Answer']}")

# -------------------- Next / Finish logic ------------------------------------
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
