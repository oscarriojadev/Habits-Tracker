def show_question():
    q = st.session_state.questions[st.session_state.idx]
    st.markdown(f"**{q['Topic']}**")
    st.write(f"Question {st.session_state.idx + 1} / {len(st.session_state.questions)}")
    st.write(q["Question"])

    choices = [q["Answer A"], q["Answer B"], q["Answer C"], q["Answer D"]]
    idx = None
    if st.session_state.answered and st.session_state.choice in choices:
        idx = choices.index(st.session_state.choice)

    choice = st.radio(
        "Select an answer:",
        choices,
        key=f"q{st.session_state.idx}",
        index=idx
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
            st.error("❌ Incorrect.")
        st.info(f"**Correct answer:** {q['Correct Answer']}")
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
