import streamlit as st

def show_question() -> None:
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
        index=None,          # no pre-selection on first view
        disabled=st.session_state.answered
    )

    col1, col2, _ = st.columns([1, 1, 1])
    with col1:
        submitted = st.button("Submit", disabled=st.session_state.answered)
    with col2:
        next_btn = st.button("Next", disabled=not st.session_state.answered)

    if submitted and selected is not None:
        st.session_state.answered = True
        if selected == q["Correct Answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error("❌ Incorrect.")
        st.info(f"**Correct answer:** {q['Correct Answer']}")
        st.rerun()

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
