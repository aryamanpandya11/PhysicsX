
import math

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# Active mock-test protection
test = st.session_state.get("mock_test")

if test and not test.get("submitted", False):
    test["forced_submission"] = True
    st.switch_page("pages/3_📝_JEE_Test.py")
    st.stop()

st.set_page_config(
    page_title="PhysicsX Lab — Simulator",
    page_icon="⚛️",
    layout="wide",
)



st.title("⚛️ PhysicsX Lab")
st.subheader("Interactive Physics Simulator")

st.write(
    "Explore projectile motion, experiment with launch conditions, "
    "visualise trajectories, and understand the physics behind "
    "every result."
)


st.info(
    "Assumptions: no air resistance, constant gravity, "
    "and the projectile lands at its launch height."
)

g = 9.8

# --------------------------------------------------
# SAVED SETTINGS
# These keys store values independently of the widgets.
# --------------------------------------------------

defaults = {
    "saved_speed": 20,
    "saved_angle": 45,
    "saved_angle_a": 30,
    "saved_angle_b": 60,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Widget keys are separate from the saved values.
widget_defaults = {
    "speed_slider": st.session_state.saved_speed,
    "speed_input": st.session_state.saved_speed,
    "angle_slider": st.session_state.saved_angle,
    "angle_input": st.session_state.saved_angle,
    "angle_a_slider": st.session_state.saved_angle_a,
    "angle_a_input": st.session_state.saved_angle_a,
    "angle_b_slider": st.session_state.saved_angle_b,
    "angle_b_input": st.session_state.saved_angle_b,
}

for key, value in widget_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Synchronisation callbacks
def save_speed_slider():
    value = st.session_state.speed_slider
    st.session_state.saved_speed = value
    st.session_state.speed_input = value


def save_speed_input():
    value = st.session_state.speed_input
    st.session_state.saved_speed = value
    st.session_state.speed_slider = value


def save_angle_slider():
    value = st.session_state.angle_slider
    st.session_state.saved_angle = value
    st.session_state.angle_input = value


def save_angle_input():
    value = st.session_state.angle_input
    st.session_state.saved_angle = value
    st.session_state.angle_slider = value


def save_angle_a_slider():
    value = st.session_state.angle_a_slider
    st.session_state.saved_angle_a = value
    st.session_state.angle_a_input = value


def save_angle_a_input():
    value = st.session_state.angle_a_input
    st.session_state.saved_angle_a = value
    st.session_state.angle_a_slider = value


def save_angle_b_slider():
    value = st.session_state.angle_b_slider
    st.session_state.saved_angle_b = value
    st.session_state.angle_b_input = value


def save_angle_b_input():
    value = st.session_state.angle_b_input
    st.session_state.saved_angle_b = value
    st.session_state.angle_b_slider = value


# --------------------------------------------------
# MAIN CONTROLS
# --------------------------------------------------

st.sidebar.header("Simulation Controls")

st.sidebar.slider(
    "Initial speed (m/s)",
    min_value=1,
    max_value=100,
    key="speed_slider",
    on_change=save_speed_slider,
)

st.sidebar.number_input(
    "Enter exact speed (m/s)",
    min_value=1,
    max_value=100,
    step=1,
    key="speed_input",
    on_change=save_speed_input,
)

st.sidebar.slider(
    "Launch angle (degrees)",
    min_value=1,
    max_value=89,
    key="angle_slider",
    on_change=save_angle_slider,
)

st.sidebar.number_input(
    "Enter exact angle (degrees)",
    min_value=1,
    max_value=89,
    step=1,
    key="angle_input",
    on_change=save_angle_input,
)

speed = st.session_state.saved_speed
angle = st.session_state.saved_angle
theta = math.radians(angle)

# --------------------------------------------------
# PHYSICS CALCULATIONS
# --------------------------------------------------

vx = speed * math.cos(theta)
vy = speed * math.sin(theta)

flight_time = 2 * vy / g
time_to_peak = vy / g
max_height = vy**2 / (2 * g)
horizontal_range = vx * flight_time

# --------------------------------------------------
# RESULTS
# --------------------------------------------------

st.header("📊 Simulation Results")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total time of flight", f"{flight_time:.2f} s")

with col2:
    st.metric("Time to maximum height", f"{time_to_peak:.2f} s")

with col3:
    st.metric("Maximum height", f"{max_height:.2f} m")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric("Horizontal range", f"{horizontal_range:.2f} m")

with col5:
    st.metric("Horizontal velocity", f"{vx:.2f} m/s")

with col6:
    st.metric("Initial vertical velocity", f"{vy:.2f} m/s")

st.info(
    f"Time to peak × 2 = {time_to_peak:.2f} × 2 "
    f"= {flight_time:.2f} s"
)

st.caption(
    "The doubling rule applies when the projectile returns to its launch height."
)

# --------------------------------------------------
# TRAJECTORY GRAPH
# --------------------------------------------------

st.header("📈 Projectile Trajectory")

t = np.linspace(0, flight_time, 200)
x = vx * t
y = vy * t - 0.5 * g * t**2

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(x, y, label="Projectile trajectory")
ax.scatter([horizontal_range], [0], label="Landing point")
ax.scatter([horizontal_range / 2], [max_height], label="Highest point")
ax.set_xlabel("Horizontal distance (m)")
ax.set_ylabel("Vertical height (m)")
ax.set_title(f"Projectile Motion: {speed} m/s at {angle}°")
ax.grid(True)
ax.legend()
st.pyplot(fig)
plt.close(fig)

# --------------------------------------------------
# PHYSICS FORMULAS
# --------------------------------------------------

with st.expander("📚 Physics Behind the Simulation"):
    st.markdown("**Horizontal velocity**")
    st.latex(r"u_x = u\cos\theta")

    st.markdown("**Initial vertical velocity**")
    st.latex(r"u_y = u\sin\theta")

    st.markdown("**Total time of flight**")
    st.latex(r"T = \frac{2u\sin\theta}{g}")

    st.markdown("**Time to maximum height**")
    st.latex(r"t_{\text{peak}} = \frac{u\sin\theta}{g}")

    st.markdown("**Maximum height**")
    st.latex(r"H = \frac{u^2\sin^2\theta}{2g}")

    st.markdown("**Horizontal range**")
    st.latex(r"R = \frac{u^2\sin 2\theta}{g}")

    st.caption(
        "Here, u is the initial speed, θ is the launch angle, "
        "and g is gravitational acceleration."
    )

# --------------------------------------------------
# COMPARISON MODE
# --------------------------------------------------

st.divider()
st.header("⚖️ Compare Two Launch Angles")
st.write("Compare two trajectories using the same initial speed.")

comp1, comp2 = st.columns(2)

with comp1:
    st.slider(
        "Angle A (degrees)",
        min_value=1,
        max_value=89,
        key="angle_a_slider",
        on_change=save_angle_a_slider,
    )
    st.number_input(
        "Enter exact angle A",
        min_value=1,
        max_value=89,
        step=1,
        key="angle_a_input",
        on_change=save_angle_a_input,
    )

with comp2:
    st.slider(
        "Angle B (degrees)",
        min_value=1,
        max_value=89,
        key="angle_b_slider",
        on_change=save_angle_b_slider,
    )
    st.number_input(
        "Enter exact angle B",
        min_value=1,
        max_value=89,
        step=1,
        key="angle_b_input",
        on_change=save_angle_b_input,
    )

angle_a = st.session_state.saved_angle_a
angle_b = st.session_state.saved_angle_b

theta_a = math.radians(angle_a)
theta_b = math.radians(angle_b)

time_a = 2 * speed * math.sin(theta_a) / g
time_b = 2 * speed * math.sin(theta_b) / g

range_a = speed**2 * math.sin(2 * theta_a) / g
range_b = speed**2 * math.sin(2 * theta_b) / g

height_a = (speed * math.sin(theta_a))**2 / (2 * g)
height_b = (speed * math.sin(theta_b))**2 / (2 * g)

t_a = np.linspace(0, time_a, 200)
t_b = np.linspace(0, time_b, 200)

x_a = speed * math.cos(theta_a) * t_a
y_a = speed * math.sin(theta_a) * t_a - 0.5 * g * t_a**2

x_b = speed * math.cos(theta_b) * t_b
y_b = speed * math.sin(theta_b) * t_b - 0.5 * g * t_b**2

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(x_a, y_a, label=f"Angle A: {angle_a}°")
ax2.plot(x_b, y_b, label=f"Angle B: {angle_b}°")
ax2.set_xlabel("Horizontal distance (m)")
ax2.set_ylabel("Vertical height (m)")
ax2.set_title("Trajectory Comparison")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)
plt.close(fig2)

result1, result2 = st.columns(2)

with result1:
    st.subheader(f"Angle A: {angle_a}°")
    st.metric("Time of flight", f"{time_a:.2f} s")
    st.metric("Maximum height", f"{height_a:.2f} m")
    st.metric("Horizontal range", f"{range_a:.2f} m")

with result2:
    st.subheader(f"Angle B: {angle_b}°")
    st.metric("Time of flight", f"{time_b:.2f} s")
    st.metric("Maximum height", f"{height_b:.2f} m")
    st.metric("Horizontal range", f"{range_b:.2f} m")

if math.isclose(angle_a + angle_b, 90, abs_tol=1e-9):
    st.success(
        "These angles are complementary, so they produce "
        "the same horizontal range at the same initial speed."
    )
