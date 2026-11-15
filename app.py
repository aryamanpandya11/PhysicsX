"""
PhysicsX Lab - Main Landing Page
Modern EdTech interactive portal for Physics simulations and JEE preparation.
"""

import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ui_theme import apply_custom_theme, get_plotly_layout, render_header

# Page configuration
st.set_page_config(
    page_title="PhysicsX Lab — Interactive Physics & JEE Suite",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply sleek modern theme styling
apply_custom_theme()


def enforce_active_test():
    """Anti-cheat safeguard: force return to test if one is active."""
    test = st.session_state.get("mock_test")
    if test and not test.get("submitted", False):
        test["forced_submission"] = True
        st.switch_page("pages/3_📝_JEE_Test.py")
        st.stop()


enforce_active_test()

# Hero Header
render_header(
    title="PhysicsX Lab",
    subtitle="An advanced interactive physics laboratory designed for students and JEE aspirants. Master physical concepts through real-time dynamic graphs, variable sliders, chapter-wise practice, and authentic CBT mock tests.",
    icon="⚛️",
    badge="Interactive Physics & JEE Engine",
)

# Highlights ribbon
st.markdown(
    """
    <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 25px;">
        <span class="px-badge px-badge-success">✓ 5 Interactive Physics Domains</span>
        <span class="px-badge px-badge-purple">✓ 10 JEE Main & Advanced Chapters</span>
        <span class="px-badge">✓ Real-time Plotly Visualizations</span>
        <span class="px-badge px-badge-success">✓ NTA CBT Exam Interface (+4 / -1)</span>
        <span class="px-badge">✓ 3-Level Scaffolded Hints</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------
# MAIN PORTALS NAVIGATION (CARDS)
# ----------------------------------------------------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="px-card">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">🚀</div>
            <h3 style="color: #00f0ff; margin: 0 0 8px 0;">Physics Simulator</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; min-height: 80px; line-height: 1.5;">
                Explore real-time interactive models: 2D Projectiles, SHM & Waves, Lorentz Force, Optics (YDSE & Lenses), and Carnot Heat Engines.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Launch Virtual Lab 🚀", key="btn_sim", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🚀_Simulator.py")

with c2:
    st.markdown(
        """
        <div class="px-card">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">🎯</div>
            <h3 style="color: #8b5cf6; margin: 0 0 8px 0;">JEE Practice Suite</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; min-height: 80px; line-height: 1.5;">
                Practice 10 high-weightage chapters with customizable difficulties, 3-tier progressive hints, tolerance checks, and step-by-step LaTeX solutions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Start Practice 🎯", key="btn_prac", use_container_width=True):
        st.switch_page("pages/2_🎯_JEE_Practice.py")

with c3:
    st.markdown(
        """
        <div class="px-card">
            <div style="font-size: 2.2rem; margin-bottom: 8px;">📝</div>
            <h3 style="color: #10b981; margin: 0 0 8px 0;">JEE Mock Test Arena</h3>
            <p style="color: #94a3b8; font-size: 0.95rem; min-height: 80px; line-height: 1.5;">
                Simulate authentic NTA computer-based tests with question palette, live countdown timer, Section A (MCQ) & Section B (Numerical), and full analytics.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Enter Test Arena 📝", key="btn_test", use_container_width=True):
        st.switch_page("pages/3_📝_JEE_Test.py")

st.divider()

# ----------------------------------------------------
# LIVE INTERACTIVE MINI-PREVIEW (INSTANT ENGAGEMENT)
# ----------------------------------------------------
st.subheader("⚡ Quick Experiment: Real-Time Projectile Simulator")
st.caption("Adjust the sliders below to see immediate physical trajectory changes.")

slider_col1, slider_col2, slider_col3 = st.columns(3)
with slider_col1:
    quick_speed = st.slider("Launch Speed u (m/s)", min_value=5, max_value=80, value=30, step=1, key="qs")
with slider_col2:
    quick_angle = st.slider("Launch Angle θ (degrees)", min_value=5, max_value=85, value=45, step=1, key="qa")
with slider_col3:
    planet = st.selectbox("Gravitational Field", options=["Earth (g = 9.8 m/s²)", "Moon (g = 1.6 m/s²)", "Mars (g = 3.7 m/s²)", "Jupiter (g = 24.8 m/s²)"], index=0)

g_val = 9.8 if "Earth" in planet else (1.6 if "Moon" in planet else (3.7 if "Mars" in planet else 24.8))

theta_rad = math.radians(quick_angle)
vx0 = quick_speed * math.cos(theta_rad)
vy0 = quick_speed * math.sin(theta_rad)
t_flight = 2 * vy0 / g_val
h_max = (vy0**2) / (2 * g_val)
r_range = vx0 * t_flight

m1, m2, m3, m4 = st.columns(4)
m1.metric("Time of Flight", f"{t_flight:.2f} s")
m2.metric("Maximum Height", f"{h_max:.2f} m")
m3.metric("Horizontal Range", f"{r_range:.2f} m")
m4.metric("Apex Speed", f"{vx0:.2f} m/s")

# Plotly interactive trajectory curve
t_pts = np.linspace(0, t_flight, 120)
x_pts = vx0 * t_pts
y_pts = vy0 * t_pts - 0.5 * g_val * (t_pts**2)

fig = go.Figure()

# Trajectory curve
fig.add_trace(go.Scatter(
    x=x_pts,
    y=y_pts,
    mode="lines",
    line=dict(color="#00f0ff", width=3.5),
    name="Trajectory Path",
    hovertemplate="Distance: %{x:.2f} m<br>Height: %{y:.2f} m<extra></extra>",
))

# Key markers: Apex and Landing
fig.add_trace(go.Scatter(
    x=[r_range / 2],
    y=[h_max],
    mode="markers+text",
    marker=dict(color="#d946ef", size=11, symbol="diamond"),
    text=[f"Apex ({h_max:.1f} m)"],
    textposition="top center",
    textfont=dict(color="#d946ef", size=12),
    name="Highest Point",
    hoverinfo="skip",
))

fig.add_trace(go.Scatter(
    x=[r_range],
    y=[0],
    mode="markers+text",
    marker=dict(color="#10b981", size=11, symbol="circle"),
    text=[f"Landing ({r_range:.1f} m)"],
    textposition="bottom center",
    textfont=dict(color="#10b981", size=12),
    name="Landing Target",
    hoverinfo="skip",
))

fig.update_layout(
    **get_plotly_layout(
        title=f"Trajectory: u = {quick_speed} m/s @ {quick_angle}° on {planet.split(' ')[0]}",
        x_title="Horizontal Distance x (metres)",
        y_title="Vertical Height y (metres)",
        height=380,
    )
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------------------------------
# HIGH-YIELD JEE REVISION FORMULA VAULT
# ----------------------------------------------------
with st.expander("📚 High-Yield JEE Physics Formula Vault & Revision Cards"):
    fc1, fc2 = st.columns(2)
    with fc1:
        st.markdown("#### 🚀 Mechanics & Kinematics")
        st.latex(r"T = \frac{2u\sin\theta}{g},\quad H = \frac{u^2\sin^2\theta}{2g},\quad R = \frac{u^2\sin 2\theta}{g}")
        st.latex(r"y = x\tan\theta - \frac{g x^2}{2 u^2 \cos^2\theta} = x\tan\theta\left(1 - \frac{x}{R}\right)")
        st.latex(r"a_{\text{rolling}} = \frac{g\sin\theta}{1 + I/(mR^2)},\quad \omega = \sqrt{\frac{k}{m}}")

    with fc2:
        st.markdown("#### ⚡ Electrodynamics & Modern Physics")
        st.latex(r"r_{\text{cyclotron}} = \frac{mv}{qB},\quad U_{\text{cap}} = \frac{1}{2}CV^2 = \frac{Q^2}{2C}")
        st.latex(r"\beta_{\text{YDSE}} = \frac{\lambda D}{d},\quad \Delta y = \frac{(\mu - 1)t D}{d}")
        st.latex(r"K_{\max} = h\nu - \Phi_0 = e V_0,\quad \eta_{\text{Carnot}} = 1 - \frac{T_C}{T_H}")

st.markdown(
    """
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; margin-top: 40px; padding: 20px 0;">
        PhysicsX Lab · Crafted for JEE Main & Advanced Excellence · Built with Streamlit & Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
