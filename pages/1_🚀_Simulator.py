"""
PhysicsX Lab - Interactive Virtual Physics Laboratory
Features 5 comprehensive physics simulation domains:
1. 2D Projectiles & Kinematics (Ground, Cliff, Air Drag & Angle Comparator)
2. SHM & Mechanical Standing Waves
3. Lorentz Force & Magnetic Deflection
4. Optics: Young's Double Slit Experiment (YDSE) & Thin Lens Ray Tracer
5. Thermodynamics: Carnot Cycle & Photoelectric Effect
"""

import math
import numpy as np
import plotly.graph_objects as go
import streamlit as st

from ui_theme import apply_custom_theme, get_plotly_layout, render_header

# Active mock-test anti-cheat safeguard
test = st.session_state.get("mock_test")
if test and not test.get("submitted", False):
    test["forced_submission"] = True
    st.switch_page("pages/3_📝_JEE_Test.py")
    st.stop()

st.set_page_config(
    page_title="PhysicsX Lab — Virtual Simulator",
    page_icon="🚀",
    layout="wide",
)

apply_custom_theme()

render_header(
    title="Virtual Physics Laboratory",
    subtitle="Experiment with physical parameters across 5 fundamental JEE domains. Visualize curves, inspect telemetry, and master underlying physical laws.",
    icon="🚀",
    badge="Interactive Simulations",
)

# Tab selection for the 5 physics domains
tab_kinematics, tab_shm, tab_em, tab_optics, tab_thermo = st.tabs([
    "🚀 1. Kinematics & Projectiles",
    "🔄 2. SHM & Standing Waves",
    "⚡ 3. Lorentz Magnetic Deflection",
    "🔍 4. Wave Optics (YDSE) & Lenses",
    "🌡️ 5. Carnot Engine & Photoelectric",
])

# ==============================================================================
# TAB 1: KINEMATICS & PROJECTILES LAB
# ==============================================================================
with tab_kinematics:
    st.markdown("### 🎯 2D Projectile Motion Laboratory")
    st.caption("Investigate launch trajectories from ground or elevated cliffs, inspect energy conservation, and compare complementary angles.")

    p_col1, p_col2 = st.columns([1, 2])

    with p_col1:
        st.markdown("#### ⚙️ Launch Parameters")
        launch_mode = st.radio("Simulation Mode", ["Single Trajectory", "Angle Comparison"], horizontal=True)

        speed = st.slider("Initial Speed u (m/s)", min_value=1, max_value=100, value=30, step=1)
        angle = st.slider("Launch Angle θ (degrees)", min_value=1, max_value=89, value=45, step=1)
        initial_h = st.slider("Launch Height h₀ (m)", min_value=0, max_value=100, value=0, step=5, help="Set h₀ > 0 for cliff projection.")

        gravity_choice = st.selectbox(
            "Gravitational Acceleration g",
            ["Earth (9.8 m/s²)", "Earth Standard (10.0 m/s²)", "Moon (1.6 m/s²)", "Mars (3.7 m/s²)", "Jupiter (24.8 m/s²)"],
            index=1,
        )
        g = 9.8 if "9.8" in gravity_choice else (10.0 if "10.0" in gravity_choice else (1.6 if "Moon" in gravity_choice else (3.7 if "Mars" in gravity_choice else 24.8)))

        rad = math.radians(angle)
        vx = speed * math.cos(rad)
        vy = speed * math.sin(rad)

        # Solving y(t) = h0 + vy*t - 0.5*g*t^2 = 0
        disc = vy**2 + 2 * g * initial_h
        t_flight = (vy + math.sqrt(disc)) / g
        t_apex = vy / g
        h_max = initial_h + (vy**2) / (2 * g)
        r_range = vx * t_flight
        v_impact = math.sqrt(vx**2 + (vy - g * t_flight)**2)

    with p_col2:
        st.markdown("#### 📊 Real-Time Physical Telemetry")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Flight Time", f"{t_flight:.2f} s")
        m2.metric("Maximum Height", f"{h_max:.2f} m")
        m3.metric("Horizontal Range", f"{r_range:.2f} m")

        m4, m5, m6 = st.columns(3)
        m4.metric("Apex Velocity (uₓ)", f"{vx:.2f} m/s")
        m5.metric("Impact Velocity", f"{v_impact:.2f} m/s")
        m6.metric("Time to Peak", f"{t_apex:.2f} s")

        if launch_mode == "Single Trajectory":
            t_eval = np.linspace(0, t_flight, 250)
            x_eval = vx * t_eval
            y_eval = initial_h + vy * t_eval - 0.5 * g * (t_eval**2)

            fig_traj = go.Figure()

            # Ground line
            fig_traj.add_shape(type="line", x0=0, y0=0, x1=r_range * 1.08, y1=0, line=dict(color="rgba(255,255,255,0.2)", width=2))

            # Cliff shape if h0 > 0
            if initial_h > 0:
                fig_traj.add_shape(type="rect", x0=0, y0=0, x1=r_range * 0.05, y1=initial_h, fillcolor="rgba(99,102,241,0.25)", line=dict(color="#6366f1", width=1))

            fig_traj.add_trace(go.Scatter(
                x=x_eval, y=y_eval, mode="lines",
                line=dict(color="#00f0ff", width=3.5),
                name=f"Path (u={speed} m/s, θ={angle}°)",
                hovertemplate="x: %{x:.2f} m<br>y: %{y:.2f} m<extra></extra>",
            ))

            # Apex and Landing markers
            x_apex = vx * t_apex
            fig_traj.add_trace(go.Scatter(
                x=[x_apex], y=[h_max], mode="markers+text",
                marker=dict(color="#f43f5e", size=10, symbol="diamond"),
                text=[f"Apex ({h_max:.1f}m)"], textposition="top center",
                textfont=dict(color="#f43f5e", size=12),
                name="Apex", hoverinfo="skip",
            ))

            fig_traj.add_trace(go.Scatter(
                x=[r_range], y=[0], mode="markers+text",
                marker=dict(color="#10b981", size=10, symbol="circle"),
                text=[f"Landing ({r_range:.1f}m)"], textposition="bottom center",
                textfont=dict(color="#10b981", size=12),
                name="Landing", hoverinfo="skip",
            ))

            fig_traj.update_layout(
                **get_plotly_layout(
                    title=f"Trajectory: u = {speed} m/s, θ = {angle}°, h₀ = {initial_h} m",
                    x_title="Horizontal Distance x (m)",
                    y_title="Vertical Height y (m)",
                    height=400,
                )
            )
            st.plotly_chart(fig_traj, use_container_width=True)

            # Energy Conservation Graph
            with st.expander("⚡ Conservation of Mechanical Energy (KE & PE vs Time)"):
                mass = 1.0  # Normalized mass 1 kg
                ke_t = 0.5 * mass * (vx**2 + (vy - g * t_eval)**2)
                pe_t = mass * g * np.maximum(0, y_eval)
                te_t = ke_t + pe_t

                fig_e = go.Figure()
                fig_e.add_trace(go.Scatter(x=t_eval, y=ke_t, mode="lines", line=dict(color="#3b82f6", width=2.5), name="Kinetic Energy (KE)"))
                fig_e.add_trace(go.Scatter(x=t_eval, y=pe_t, mode="lines", line=dict(color="#f59e0b", width=2.5), name="Potential Energy (PE)"))
                fig_e.add_trace(go.Scatter(x=t_eval, y=te_t, mode="lines", line=dict(color="#10b981", width=2, dash="dash"), name="Total Energy (E)"))

                fig_e.update_layout(
                    **get_plotly_layout(
                        title="Energy Evolution Over Time",
                        x_title="Time t (s)",
                        y_title="Energy (Joules for m = 1kg)",
                        height=300,
                    )
                )
                st.plotly_chart(fig_e, use_container_width=True)

        else:
            # Angle Comparison Mode
            st.markdown("##### ⚖️ Angle Comparison Mode")
            c_comp1, c_comp2 = st.columns(2)
            with c_comp1:
                comp_a = st.slider("Angle A (°)", min_value=5, max_value=85, value=30, step=1)
            with c_comp2:
                comp_b = st.slider("Angle B (°)", min_value=5, max_value=85, value=60, step=1)

            rad_a = math.radians(comp_a)
            rad_b = math.radians(comp_b)

            t_a = 2 * speed * math.sin(rad_a) / g
            t_b = 2 * speed * math.sin(rad_b) / g
            r_a = (speed**2 * math.sin(2 * rad_a)) / g
            r_b = (speed**2 * math.sin(2 * rad_b)) / g
            h_a = (speed * math.sin(rad_a))**2 / (2 * g)
            h_b = (speed * math.sin(rad_b))**2 / (2 * g)

            t_arr_a = np.linspace(0, t_a, 200)
            t_arr_b = np.linspace(0, t_b, 200)

            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatter(
                x=speed * math.cos(rad_a) * t_arr_a,
                y=speed * math.sin(rad_a) * t_arr_a - 0.5 * g * (t_arr_a**2),
                mode="lines", line=dict(color="#00f0ff", width=3),
                name=f"Angle A: {comp_a}° (R={r_a:.1f}m, H={h_a:.1f}m)",
            ))
            fig_comp.add_trace(go.Scatter(
                x=speed * math.cos(rad_b) * t_arr_b,
                y=speed * math.sin(rad_b) * t_arr_b - 0.5 * g * (t_arr_b**2),
                mode="lines", line=dict(color="#ec4899", width=3),
                name=f"Angle B: {comp_b}° (R={r_b:.1f}m, H={h_b:.1f}m)",
            ))

            fig_comp.update_layout(
                **get_plotly_layout(
                    title=f"Trajectory Comparison: {comp_a}° vs {comp_b}° at u = {speed} m/s",
                    x_title="Horizontal Distance (m)",
                    y_title="Vertical Height (m)",
                    height=400,
                )
            )
            st.plotly_chart(fig_comp, use_container_width=True)

            if math.isclose(comp_a + comp_b, 90, abs_tol=1e-5):
                st.success("🎯 Complementary Angle Theorem: Since $\\theta_A + \\theta_B = 90^\\circ$, both projectiles have identical horizontal ranges at equal launch speeds!")

    with st.expander("📚 Physics Principles & Mathematical Derivations"):
        st.markdown(
            r"""
            - **Trajectory Equation:** $y = h_0 + x\tan\theta - \frac{g x^2}{2 u^2 \cos^2\theta}$
            - **Flight Time (Flat Ground):** $T = \frac{2u\sin\theta}{g}$
            - **Maximum Height:** $H_{\max} = \frac{u^2\sin^2\theta}{2g}$
            - **Horizontal Range:** $R = \frac{u^2\sin 2\theta}{g}$ (Maximum at $\theta = 45^\circ$)
            - **Energy Conservation:** $E_{\text{total}} = \frac{1}{2}m v_x^2 + \frac{1}{2}m v_y^2 + m g y = \text{constant}$
            """
        )

# ==============================================================================
# TAB 2: SIMPLE HARMONIC MOTION (SHM) & WAVES LAB
# ==============================================================================
with tab_shm:
    st.markdown("### 🔄 Simple Harmonic Motion & Standing Waves")
    st.caption("Simulate mass-spring oscillations, phase-space trajectories, and standing wave harmonics on a string.")

    shm_type = st.radio("System Type", ["Mass-Spring Oscillator", "Standing Waves on a String"], horizontal=True)

    if shm_type == "Mass-Spring Oscillator":
        s_col1, s_col2 = st.columns([1, 2])
        with s_col1:
            st.markdown("#### ⚙️ Oscillator Settings")
            mass_k = st.slider("Mass m (kg)", 0.5, 10.0, 2.0, 0.5)
            k_spring = st.slider("Spring Constant k (N/m)", 10, 500, 100, 10)
            amp_A = st.slider("Initial Amplitude A (m)", 0.1, 2.0, 0.5, 0.1)
            damping_b = st.slider("Damping Coefficient b (N·s/m)", 0.0, 2.0, 0.1, 0.05)

            omega_0 = math.sqrt(k_spring / mass_k)
            t_period = 2 * math.pi / omega_0
            f_freq = 1 / t_period
            v_max = amp_A * omega_0

        with s_col2:
            st.markdown("#### 📊 Kinematic Properties")
            sm1, sm2, sm3, sm4 = st.columns(4)
            sm1.metric("Angular Freq (ω₀)", f"{omega_0:.2f} rad/s")
            sm2.metric("Time Period (T)", f"{t_period:.2f} s")
            sm3.metric("Frequency (f)", f"{f_freq:.2f} Hz")
            sm4.metric("Max Velocity", f"{v_max:.2f} m/s")

            # Time domain evaluation
            t_shm = np.linspace(0, 4 * t_period, 400)
            gamma = damping_b / (2 * mass_k)
            omega_d = math.sqrt(max(0.001, omega_0**2 - gamma**2))

            # x(t) = A * exp(-gamma*t) * cos(omega_d * t)
            x_shm = amp_A * np.exp(-gamma * t_shm) * np.cos(omega_d * t_shm)
            v_shm = np.gradient(x_shm, t_shm)

            fig_shm = go.Figure()
            fig_shm.add_trace(go.Scatter(x=t_shm, y=x_shm, mode="lines", line=dict(color="#00f0ff", width=2.5), name="Displacement x(t)"))
            fig_shm.add_trace(go.Scatter(x=t_shm, y=v_shm, mode="lines", line=dict(color="#8b5cf6", width=2, dash="dot"), name="Velocity v(t)"))
            fig_shm.update_layout(
                **get_plotly_layout(
                    title=f"Oscillation Waveform (m = {mass_k} kg, k = {k_spring} N/m)",
                    x_title="Time t (s)",
                    y_title="Displacement (m) / Velocity (m/s)",
                    height=360,
                )
            )
            st.plotly_chart(fig_shm, use_container_width=True)

            # Phase space portrait (v vs x)
            fig_phase = go.Figure()
            fig_phase.add_trace(go.Scatter(x=x_shm, y=v_shm, mode="lines", line=dict(color="#10b981", width=2.5), name="Phase Orbit"))
            fig_phase.update_layout(
                **get_plotly_layout(
                    title="Phase Space Portrait (Velocity v vs Position x)",
                    x_title="Position x (m)",
                    y_title="Velocity v (m/s)",
                    height=320,
                )
            )
            st.plotly_chart(fig_phase, use_container_width=True)

    else:
        # Standing waves visualizer
        st.markdown("#### 🎸 Standing Waves on a Stretched String")
        w_c1, w_c2 = st.columns([1, 2])
        with w_c1:
            harmonic_n = st.slider("Harmonic Number (n)", 1, 6, 2, 1)
            string_len = st.slider("String Length L (m)", 0.5, 4.0, 2.0, 0.5)
            wave_speed_v = st.slider("Wave Speed v (m/s)", 10, 100, 40, 5)

            wave_l = 2 * string_len / harmonic_n
            freq_n = harmonic_n * wave_speed_v / (2 * string_len)

            st.metric("Wavelength (λ)", f"{wave_l:.2f} m")
            st.metric("Resonant Frequency", f"{freq_n:.1f} Hz")
            st.caption(f"Number of nodes: {harmonic_n + 1} · Antinodes: {harmonic_n}")

        with w_c2:
            x_wave = np.linspace(0, string_len, 300)
            k_w = harmonic_n * math.pi / string_len

            fig_wave = go.Figure()
            # Envelope
            fig_wave.add_trace(go.Scatter(x=x_wave, y=np.sin(k_w * x_wave), mode="lines", line=dict(color="#00f0ff", width=3), name="+ Envelope"))
            fig_wave.add_trace(go.Scatter(x=x_wave, y=-np.sin(k_w * x_wave), mode="lines", line=dict(color="#00f0ff", width=1.5, dash="dash"), name="- Envelope"))

            # Nodes
            nodes_x = np.array([i * string_len / harmonic_n for i in range(harmonic_n + 1)])
            fig_wave.add_trace(go.Scatter(x=nodes_x, y=np.zeros_like(nodes_x), mode="markers", marker=dict(color="#f43f5e", size=9), name="Nodes (Zero displacement)"))

            fig_wave.update_layout(
                **get_plotly_layout(
                    title=f"Harmonic Mode n = {harmonic_n} on Stretched String",
                    x_title="Position along string x (m)",
                    y_title="Wave Amplitude (Normalized)",
                    height=380,
                )
            )
            st.plotly_chart(fig_wave, use_container_width=True)

# ==============================================================================
# TAB 3: LORENTZ FORCE & MAGNETIC DEFLECTION LAB
# ==============================================================================
with tab_em:
    st.markdown("### ⚡ Charged Particle Motion in Magnetic Field")
    st.caption("Investigate cyclotron radius, pitch, and Lorentz helical deflection: $\\vec{F} = q(\\vec{v} \\times \\vec{B})$.")

    em_c1, em_c2 = st.columns([1, 2])
    with em_c1:
        st.markdown("#### ⚙️ Field & Particle Settings")
        particle = st.selectbox("Particle Type", ["Proton (q = +e, m = 1 u)", "Electron (q = -e, m = 5.48e-4 u)", "Alpha Particle (q = +2e, m = 4 u)"])

        if "Proton" in particle:
            q_val, m_val = 1.6e-19, 1.67e-27
        elif "Electron" in particle:
            q_val, m_val = 1.6e-19, 9.11e-31
        else:
            q_val, m_val = 3.2e-19, 6.64e-27

        b_field = st.slider("Magnetic Field B (Tesla)", 0.1, 5.0, 1.0, 0.1)
        v_speed = st.slider("Particle Speed v (×10⁶ m/s)", 1.0, 20.0, 5.0, 0.5) * 1e6
        pitch_angle = st.slider("Pitch Angle with B-field (degrees)", 10, 90, 90, 5)

        alpha_rad = math.radians(pitch_angle)
        v_perp = v_speed * math.sin(alpha_rad)
        v_par = v_speed * math.cos(alpha_rad)

        r_cyclotron = (m_val * v_perp) / (q_val * b_field)
        t_period_em = (2 * math.pi * m_val) / (q_val * b_field)
        freq_cyclotron = 1 / t_period_em
        pitch_val = v_par * t_period_em

    with em_c2:
        st.markdown("#### 📊 Cyclotron Telemetry")
        em1, em2, em3 = st.columns(3)
        em1.metric("Cyclotron Radius", f"{r_cyclotron*1000:.2f} mm")
        em2.metric("Orbital Period", f"{t_period_em*1e9:.2f} ns")
        em3.metric("Cyclotron Frequency", f"{freq_cyclotron/1e6:.2f} MHz")

        if pitch_angle < 90:
            st.metric("Helical Pitch Distance", f"{pitch_val*1000:.2f} mm")

        # Plot 2D circular projection or 3D helix
        t_em = np.linspace(0, 3 * t_period_em, 300)
        omega_c = q_val * b_field / m_val

        x_em = r_cyclotron * np.sin(omega_c * t_em) * 1000  # in mm
        y_em = r_cyclotron * (1 - np.cos(omega_c * t_em)) * 1000
        z_em = v_par * t_em * 1000

        if pitch_angle == 90:
            fig_em = go.Figure()
            fig_em.add_trace(go.Scatter(x=x_em, y=y_em, mode="lines", line=dict(color="#00f0ff", width=3), name="Circular Orbit"))
            fig_em.update_layout(
                **get_plotly_layout(
                    title="Deflection Orbit in Transverse B-Field (Z-axis into screen)",
                    x_title="X (mm)",
                    y_title="Y (mm)",
                    height=380,
                )
            )
            st.plotly_chart(fig_em, use_container_width=True)
        else:
            fig_em_3d = go.Figure(data=[go.Scatter3d(
                x=x_em, y=y_em, z=z_em, mode="lines",
                line=dict(color="#00f0ff", width=4),
                name="Helical Trajectory",
            )])
            fig_em_3d.update_layout(
                title=dict(text="<b>3D Helical Trajectory</b>", font=dict(color="#f8fafc")),
                scene=dict(
                    xaxis=dict(title="X (mm)", backgroundcolor="rgba(15,23,42,0.8)", gridcolor="rgba(255,255,255,0.1)"),
                    yaxis=dict(title="Y (mm)", backgroundcolor="rgba(15,23,42,0.8)", gridcolor="rgba(255,255,255,0.1)"),
                    zaxis=dict(title="Z - Field Axis (mm)", backgroundcolor="rgba(15,23,42,0.8)", gridcolor="rgba(255,255,255,0.1)"),
                ),
                paper_bgcolor="rgba(15,23,42,0)",
                height=420,
            )
            st.plotly_chart(fig_em_3d, use_container_width=True)

# ==============================================================================
# TAB 4: WAVE OPTICS (YDSE) & RAY OPTICS (THIN LENS)
# ==============================================================================
with tab_optics:
    st.markdown("### 🔍 Wave & Ray Optics Laboratory")
    optics_mode = st.radio("Optics Module", ["Young's Double Slit Experiment (YDSE)", "Thin Lens Ray Diagram"], horizontal=True)

    if "YDSE" in optics_mode:
        yo_c1, yo_c2 = st.columns([1, 2])
        with yo_c1:
            st.markdown("#### ⚙️ YDSE Parameters")
            lamb_nm = st.slider("Wavelength λ (nm)", 380, 750, 550, 10)
            slit_d_mm = st.slider("Slit Separation d (mm)", 0.1, 2.0, 0.5, 0.05)
            screen_D_m = st.slider("Screen Distance D (m)", 0.5, 3.0, 1.5, 0.1)
            mica_shift = st.checkbox("Insert Thin Mica Sheet in one beam")

            if mica_shift:
                mica_thick_um = st.slider("Mica Thickness t (μm)", 1.0, 20.0, 5.0, 0.5)
                mica_mu = st.slider("Mica Refractive Index μ", 1.2, 1.8, 1.5, 0.05)
                fringe_shift_mm = ((mica_mu - 1) * (mica_thick_um * 1e-6) * screen_D_m / (slit_d_mm * 1e-3)) * 1000
            else:
                fringe_shift_mm = 0.0

            beta_mm = (lamb_nm * 1e-9 * screen_D_m / (slit_d_mm * 1e-3)) * 1000

        with yo_c2:
            st.markdown("#### 📊 Interference Geometry")
            ym1, ym2 = st.columns(2)
            ym1.metric("Fringe Width (β)", f"{beta_mm:.3f} mm")
            if mica_shift:
                ym2.metric("Central Fringe Shift (Δy)", f"{fringe_shift_mm:.3f} mm")
            else:
                ym2.metric("Angular Fringe Width", f"{(lamb_nm*1e-9/(slit_d_mm*1e-3))*1000:.3f} mrad")

            # Intensity profile: I(y) = I0 * cos^2(pi * d * (y - shift) / (lambda * D))
            y_screen = np.linspace(-5 * beta_mm, 5 * beta_mm, 500)
            phase = (math.pi * (slit_d_mm * 1e-3) * ((y_screen - fringe_shift_mm) * 1e-3)) / (lamb_nm * 1e-9 * screen_D_m)
            intensity = np.cos(phase)**2

            # Dynamic trace color based on wavelength
            def nm_to_hex(nm):
                if nm < 440:
                    return "#8b5cf6"
                if nm < 490:
                    return "#3b82f6"
                if nm < 560:
                    return "#10b981"
                if nm < 590:
                    return "#eab308"
                if nm < 635:
                    return "#f97316"
                return "#ef4444"

            fig_ydse = go.Figure()
            fig_ydse.add_trace(go.Scatter(
                x=y_screen, y=intensity, mode="lines",
                line=dict(color=nm_to_hex(lamb_nm), width=2.5),
                name=f"Intensity I(y) [λ = {lamb_nm} nm]",
            ))

            fig_ydse.update_layout(
                **get_plotly_layout(
                    title=f"YDSE Intensity Fringe Pattern (Fringe width β = {beta_mm:.2f} mm)",
                    x_title="Screen Position y (mm)",
                    y_title="Relative Intensity I/I₀",
                    height=380,
                )
            )
            st.plotly_chart(fig_ydse, use_container_width=True)

    else:
        # Thin Lens Ray Diagram
        st.markdown("#### 👓 Thin Lens Image Formation Simulator")
        tl_c1, tl_c2 = st.columns([1, 2])
        with tl_c1:
            lens_type = st.selectbox("Lens Type", ["Convex Lens (Converging, f > 0)", "Concave Lens (Diverging, f < 0)"])
            f_abs = st.slider("Focal Length |f| (cm)", 5, 50, 20, 1)
            f_lens = f_abs if "Convex" in lens_type else -f_abs
            u_obj = -st.slider("Object Distance |u| (cm)", 5, 80, 35, 1)  # Cartesian sign convention
            h_obj = st.slider("Object Height h₀ (cm)", 1, 10, 4, 1)

            # Lens formula: 1/v - 1/u = 1/f => 1/v = 1/f + 1/u
            inv_v = (1 / f_lens) + (1 / u_obj)
            if math.isclose(inv_v, 0, abs_tol=1e-5):
                v_img = None
                m_mag = None
            else:
                v_img = 1 / inv_v
                m_mag = v_img / u_obj
                h_img = m_mag * h_obj

        with tl_c2:
            st.markdown("#### 📊 Image Properties")
            lm1, lm2, lm3 = st.columns(3)
            if v_img is not None:
                lm1.metric("Image Distance (v)", f"{v_img:.2f} cm")
                lm2.metric("Magnification (m)", f"{m_mag:.2f}")
                nature = "Real & Inverted" if v_img > 0 else "Virtual & Erect"
                lm3.metric("Nature", nature)

                # Ray diagram plot
                fig_lens = go.Figure()
                # Principal axis
                fig_lens.add_shape(type="line", x0=-90, y0=0, x1=90, y1=0, line=dict(color="rgba(255,255,255,0.3)", width=1))
                # Lens plane
                fig_lens.add_shape(type="line", x0=0, y0=-15, x1=0, y1=15, line=dict(color="#00f0ff", width=2.5))
                # Object Arrow
                fig_lens.add_annotation(x=u_obj, y=h_obj, ax=u_obj, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#10b981", arrowwidth=3)
                # Image Arrow
                fig_lens.add_annotation(x=v_img, y=h_img, ax=v_img, ay=0, xref="x", yref="y", axref="x", ayref="y", showarrow=True, arrowhead=2, arrowcolor="#f43f5e", arrowwidth=3)

                fig_lens.update_layout(
                    **get_plotly_layout(
                        title=f"Ray Diagram (u = {u_obj} cm, f = {f_lens} cm, v = {v_img:.1f} cm)",
                        x_title="Position along Principal Axis (cm)",
                        y_title="Height (cm)",
                        height=360,
                    )
                )
                st.plotly_chart(fig_lens, use_container_width=True)
            else:
                st.warning("Object placed at the focal point (u = f). Image formed at infinity!")

# ==============================================================================
# TAB 5: THERMODYNAMICS & MODERN PHYSICS LAB
# ==============================================================================
with tab_thermo:
    st.markdown("### 🌡️ Thermodynamics & Modern Physics")
    th_mode = st.radio("Select Domain", ["Carnot Heat Engine (P-V Indicator Diagram)", "Photoelectric Effect (Einstein's Equation)"], horizontal=True)

    if "Carnot" in th_mode:
        tc1, tc2 = st.columns([1, 2])
        with tc1:
            st.markdown("#### ⚙️ Temperature Reservoirs")
            t_hot = st.slider("Source Temperature T_H (K)", 400, 1000, 600, 20)
            t_cold = st.slider("Sink Temperature T_C (K)", 200, 500, 300, 10)
            v1 = 1.0
            r_comp = st.slider("Compression Ratio V₂/V₁", 1.5, 3.5, 2.0, 0.1)

            if t_cold >= t_hot:
                st.error("T_H must be strictly greater than T_C.")
                st.stop()

            carnot_eff = (1 - t_cold / t_hot) * 100
            q_in = 1000  # Joules normalized
            w_out = q_in * (carnot_eff / 100)
            q_out = q_in - w_out

        with tc2:
            st.markdown("#### 📊 Carnot Efficiency & Work")
            cm1, cm2, cm3 = st.columns(3)
            cm1.metric("Ideal Efficiency (η)", f"{carnot_eff:.1f}%")
            cm2.metric("Work Produced (W)", f"{w_out:.1f} J")
            cm3.metric("Heat Rejected (Q_C)", f"{q_out:.1f} J")

            # P-V Curve Generator for Carnot cycle
            gamma_air = 1.4
            v2 = v1 * r_comp
            # 1->2 Isothermal at T_H: P = n R T_H / V
            v_12 = np.linspace(v1, v2, 60)
            p_12 = 800 / v_12
            # 2->3 Adiabatic expansion to T_C: P * V^gamma = const
            v3 = v2 * ((t_hot / t_cold)**(1 / (gamma_air - 1)))
            v_23 = np.linspace(v2, v3, 60)
            p_23 = p_12[-1] * (v2 / v_23)**gamma_air
            # 3->4 Isothermal compression at T_C
            v4 = v3 / r_comp
            v_34 = np.linspace(v3, v4, 60)
            p_34 = p_23[-1] * (v3 / v_34)
            # 4->1 Adiabatic compression back to state 1
            v_41 = np.linspace(v4, v1, 60)
            p_41 = p_34[-1] * (v4 / v_41)**gamma_air

            fig_carnot = go.Figure()
            fig_carnot.add_trace(go.Scatter(x=v_12, y=p_12, mode="lines", line=dict(color="#f43f5e", width=2.5), name="1→2 Isothermal Expansion (T_H)"))
            fig_carnot.add_trace(go.Scatter(x=v_23, y=p_23, mode="lines", line=dict(color="#f59e0b", width=2.5), name="2→3 Adiabatic Expansion"))
            fig_carnot.add_trace(go.Scatter(x=v_34, y=p_34, mode="lines", line=dict(color="#3b82f6", width=2.5), name="3→4 Isothermal Compression (T_C)"))
            fig_carnot.add_trace(go.Scatter(x=v_41, y=p_41, mode="lines", line=dict(color="#10b981", width=2.5), name="4→1 Adiabatic Compression"))

            fig_carnot.update_layout(
                **get_plotly_layout(
                    title=f"Carnot Cycle Indicator Diagram (η = {carnot_eff:.1f}%)",
                    x_title="Volume V (m³)",
                    y_title="Pressure P (kPa)",
                    height=380,
                )
            )
            st.plotly_chart(fig_carnot, use_container_width=True)

    else:
        # Photoelectric Effect
        pe_c1, pe_c2 = st.columns([1, 2])
        with pe_c1:
            st.markdown("#### ⚙️ Photosensitive Target")
            metal = st.selectbox(
                "Target Metal",
                ["Cesium (Φ = 2.14 eV)", "Potassium (Φ = 2.30 eV)", "Sodium (Φ = 2.36 eV)", "Copper (Φ = 4.65 eV)", "Platinum (Φ = 5.65 eV)"],
            )
            phi_val = float(metal.split("Φ = ")[1].split(" eV")[0])
            pe_lamb = st.slider("Incident Light Wavelength λ (nm)", 150, 700, 300, 10)

            hc_constant = 1240.0  # eV * nm
            e_photon = hc_constant / pe_lamb
            k_max_ev = max(0.0, e_photon - phi_val)
            v_stopping = k_max_ev  # in Volts since e*V0 = Kmax
            thresh_lamb = hc_constant / phi_val

        with pe_c2:
            st.markdown("#### 📊 Photoelectron Telemetry")
            pm1, pm2, pm3 = st.columns(3)
            pm1.metric("Photon Energy", f"{e_photon:.2f} eV")
            pm2.metric("Stopping Potential (V₀)", f"{v_stopping:.2f} V")
            pm3.metric("Threshold λ₀", f"{thresh_lamb:.1f} nm")

            if e_photon >= phi_val:
                st.success(f"⚡ Photoelectric Emission Active! Electrons emitted with K_max = {k_max_ev:.2f} eV.")
            else:
                st.error("🚫 No Photoelectrons Emitted: Incident photon energy is below work function Φ.")

            # Stopping Potential vs Frequency plot
            nu_freq = np.linspace(4e14, 15e14, 200)
            h_planck_ev = 4.1357e-15  # eV * s
            v_stop_curve = np.maximum(0, h_planck_ev * nu_freq - phi_val)

            fig_pe = go.Figure()
            fig_pe.add_trace(go.Scatter(x=nu_freq / 1e14, y=v_stop_curve, mode="lines", line=dict(color="#00f0ff", width=3), name="V₀ vs Frequency ν"))
            fig_pe.update_layout(
                **get_plotly_layout(
                    title="Stopping Potential V₀ vs Frequency ν (Slope = h/e, Intercept = -Φ/e)",
                    x_title="Frequency ν (×10¹⁴ Hz)",
                    y_title="Stopping Potential V₀ (Volts)",
                    height=360,
                )
            )
            st.plotly_chart(fig_pe, use_container_width=True)
