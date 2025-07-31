import streamlit as st

def show_question() -> None:
    """Render the current quiz question, radio buttons and navigation."""
    idx      = st.session_state.idx
    question = st.session_state.questions[idx]
    answered = st.session_state.answered
    choice   = st.session_state.choice

    # ── Question meta ----------------------------------------------------------
    st.markdown(f"**{question['Topic']}**")
    st.write(f"Question {idx + 1} / {len(st.session_state.questions)}")
    st.write(question["Question"])

    # ── Answer options ---------------------------------------------------------
    choices = [question["Answer A"], question["Answer B"],
               question["Answer C"], question["Answer D"]]

    # Default selection (after the first submission)
    default = choices.index(choice) if answered and choice in choices else None

    # Use a unique key so each question gets its own radio widget
    selected = st.radio(
        "Select an answer:",
        choices,
        key=f"q_{idx}",
        index=default,
        disabled=answered
    )

    # ── Buttons ----------------------------------------------------------------
    col1, col2, _ = st.columns([1, 1, 1])
    with col1:
        submitted = st.button("Submit", disabled=answered)
    with col2:
        next_btn = st.button("Next", disabled=not answered)

    # ── Submit logic -----------------------------------------------------------
    if submitted and selected is not None:
        st.session_state.answered = True
        st.session_state.choice   = selected
        if selected == question["Correct Answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")
        st.info(f"**Correct answer:** {question['Correct Answer']}")
        st.rerun()

    # ── Next / Finish logic ----------------------------------------------------
    if next_btn:
        if idx < len(st.session_state.questions) - 1:
            st.session_state.idx      += 1
            st.session_state.answered  = False
            st.session_state.choice    = None
            st.rerun()
        else:
            st.balloons()
            st.write("### 🎉 Quiz finished!")
            st.write(f"**Your score: {st.session_state.score} / {len(st.session_state.questions)}**")

            if st.button("Restart Quiz"):
                for k in ("idx", "score", "answered", "choice", "questions"):
                    st.session_state.pop(k, None)
                st.rerun()
