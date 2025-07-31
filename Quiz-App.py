# quiz.py
import streamlit as st

# ------------- dummy data so you can test immediately ----------------
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
        },
    ]
# ---------------------------------------------------------------------

# initialise session-state variables
for k, v in {"idx": 0, "score": 0, "answered": False}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -------------------- UI ---------------------------------------------------
idx = st.session_state.idx
q   = st.session_state.questions[idx]

st.markdown(f"**{q['Topic']}**")
st.write(f"Question {idx + 1} / {len(st.session_state.questions)}")
st.write(q["Question"])

choices = [q["Answer A"], q["Answer B"], q["Answer C"], q["Answer D"]]

# radio always enabled so its value is always available
choice = st.radio(
    "Select an answer:",
    choices,
    key=f"radio_{idx}",        # unique key per question
    index=None                 # no pre-selection
)

col1, col2, _ = st.columns([1, 1, 1])

with col1:
    submitted = st.button("Submit", disabled=st.session_state.answered)

with col2:
    next_btn = st.button("Next", disabled=not st.session_state.answered)

# -------------------- Submit logic -----------------------------------------
if submitted and choice is not None:
    st.session_state.answered = True
    if choice == q["Correct Answer"]:
        st.session_state.score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect")
    st.info(f"**Correct answer:** {q['Correct Answer']}")

# -------------------- Next / Finish logic ----------------------------------
if next_btn:
    if idx < len(st.session_state.questions) - 1:
        st.session_state.idx += 1
        st.session_state.answered = False
        st.rerun()
    else:
        st.balloons()
        st.write("### 🎉 Quiz finished!")
        st.write(f"**Your score: {st.session_state.score} / {len(st.session_state.questions)}**")
        if st.button("Restart Quiz"):
            for k in ("idx", "score", "answered", "questions"):
                st.session_state.pop(k, None)
            st.rerun()
