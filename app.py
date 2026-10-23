
import streamlit as st


st.set_page_config(
    page_title="PhysicsX Lab",
    page_icon="⚛️",
    layout="wide",
)


def enforce_active_test():
    test = st.session_state.get("mock_test")

    if test and not test.get("submitted", False):
        test["forced_submission"] = True
        st.switch_page("pages/3_📝_JEE_Test.py")
        st.stop()


enforce_active_test()


st.title("⚛️ PhysicsX Lab")
st.subheader("Explore. Experiment. Excel.")

st.write(
    "An interactive physics learning platform to visualise "
    "concepts, practise JEE problems, and test your understanding."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🚀 Physics Simulator")
    st.write(
        "Explore projectile motion, adjust parameters, "
        "compare trajectories, and understand the physics visually."
    )

    if st.button("Open Simulator", use_container_width=True):
        st.switch_page("pages/1_🚀_Simulator.py")


with col2:
    st.subheader("🎯 JEE Practice")
    st.write(
        "Solve numerical problems, check your answers, "
        "and learn with hints and worked solutions."
    )

    if st.button("Open Practice", use_container_width=True):
        st.switch_page("pages/2_🎯_JEE_Practice.py")


st.divider()

st.subheader("📝 JEE Mock Test")
st.write(
    "Attempt timed tests with exam-style marking "
    "and detailed performance analysis."
)

if st.button("Open JEE Test", use_container_width=True):
    st.switch_page("pages/3_📝_JEE_Test.py")


st.divider()

st.caption(
    "PhysicsX Lab · Understand physics by experiencing it."
)
