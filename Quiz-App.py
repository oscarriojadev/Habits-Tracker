# quiz.py
import streamlit as st
import pandas as pd

# -------------------- 1. Let the user upload a CSV ---------------------------
uploaded = st.file_uploader(
    "Upload a CSV with columns: Topic, Question, Answer A, Answer B, Answer C, Answer D, Correct Answer",
    type="csv"
)

if uploaded is None:
    st.stop()          # nothing to do until a file is provided

# read the CSV and convert to the same list-of-dicts format you already use
df = pd.read_csv(uploaded, dtype=str)          # keep everything as strings
df = df.fillna("")                               # tidy empty cells

required_cols = {"Topic", "Question", "Answer A", "Answer B",
                 "Answer C", "Answer D", "Correct Answer"}
missing = required_cols.difference(df.columns)
if missing:
    st.error(f"CSV is missing columns: {', '.join(missing)}")
    st.stop()

st.session_state.questions = df.to_dict("records")
# -----------------------------------------------------------------------------


# -------------------- 2. initialise session state (same as before) ----------
for k, v in {"idx": 0, "score": 0, "answered": False}.items():
    if k not in st.session_state:
        st.session_state[k] = v
# -----------------------------------------------------------------------------


# -------------------- 3. everything below is unchanged -----------------------
idx = st.session_state.idx
q   = st.session_state.questions[idx]

st.markdown(f"**{q['Topic']}**")
st.write(f"Question {idx + 1} / {len(st.session_state.questions)}")
st.write(q["Question"])

choices = [q["Answer A"], q["Answer B"], q["Answer C"], q["Answer D"]]

choice = st.radio(
    "Select an answer:",
    choices,
    key=f"radio_{idx}",
    index=None
)

col1, col2, _ = st.columns([1, 1, 1])

with col1:
    submitted = st.button("Submit", disabled=st.session_state.answered, key=f"submit_{idx}")

with col2:
    next_btn = st.button("Next", disabled=not st.session_state.answered, key=f"next_{idx}")

if submitted and choice is not None:
    st.session_state.answered = True
    if choice == q["Correct Answer"]:
        st.session_state.score += 1
        st.success("✅ Correct!")
    else:
        st.error("❌ Incorrect")
    st.info(f"**Correct answer:** {q['Correct Answer']}")

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
