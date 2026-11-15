# ⚛️ PhysicsX Lab

> **Interactive Physics Laboratory & JEE Main / Advanced Exam Preparation Suite**  
> Live Application: [physicsx-lab.streamlit.app](https://physicsx-lab.streamlit.app)

---

## 🌟 Overview

**PhysicsX Lab** is a high-performance, interactive physics learning and simulation platform designed specifically for students and JEE aspirants. Combining interactive mathematical models with responsive UI design, it allows students to **visualize complex physical phenomena**, **experiment with variables**, and **train under authentic computer-based testing conditions**.

---

## 🚀 Key Modules & Capabilities

### 1. 🔬 Interactive Virtual Physics Laboratory (`pages/1_🚀_Simulator.py`)
- **Kinematics & 2D Projectiles**: Ground and elevated cliff launches ($h_0 \ge 0$), customizable planetary gravity (Earth, Moon, Mars, Jupiter), real-time mechanical energy conservation graphs ($KE$, $PE$, $E_{\text{total}}$), and side-by-side complementary angle comparator ($30^\circ$ vs $60^\circ$).
- **Simple Harmonic Motion & Waves**: Spring-mass oscillator with damping coefficient sliders, phase-space portraits ($v$ vs $x$), and standing wave harmonic modes ($n = 1 \dots 6$) on stretched strings with nodes and antinodes.
- **Lorentz Magnetic Deflection**: Charged particle ($p^+$, $e^-$, $\alpha^{2+}$) deflection in uniform magnetic fields $\vec{B}$, calculating cyclotron radius $r = \frac{mv\sin\alpha}{qB}$, pitch, frequency, and 3D helical trajectories.
- **Wave & Ray Optics**: Young's Double Slit Experiment (YDSE) with spectral wavelength tuning, mica sheet fringe shifting $\Delta y = \frac{(\mu - 1)t D}{d}$, and thin lens ray diagram tracer with image distance and magnification.
- **Thermodynamics & Modern Physics**: 4-stage Carnot Heat Engine $P-V$ indicator diagram with Carnot efficiency $\eta = 1 - \frac{T_C}{T_H}$, and Photoelectric Effect simulator demonstrating Einstein's equation $K_{\max} = h\nu - \Phi_0$ and stopping potential.

---

### 2. 🎯 Chapter-Wise JEE Practice Suite (`pages/2_🎯_JEE_Practice.py`)
- **10 Core Syllabus Domains**:
  1. Kinematics & Projectiles
  2. Newton's Laws & Friction
  3. Work, Power & Energy
  4. Rotational Dynamics
  5. Gravitation & Satellites
  6. SHM & Mechanical Waves
  7. Electrostatics & Capacitance
  8. Current Electricity & Magnetism
  9. Ray & Wave Optics
  10. Thermodynamics & Modern Physics
- **3 Difficulty Tiers**: Basic (JEE Main Easy), Intermediate (JEE Main Moderate), and JEE Challenge (JEE Advanced multi-concept).
- **3-Level Scaffolded Hints**:
  - *Hint 1*: Core principle / physical law.
  - *Hint 2*: Governing formula and variable mapping.
  - *Hint 3*: Numerical substitution and algebraic setup.
- **Automated Grading & Tolerance Checking**: Evaluates both MCQs and Numerical Value questions with sensible floating-point precision tolerances ($\pm 0.05$ or $\pm 2\%$).
- **Persistent Practice Sessions**: Saves sessions automatically to `practice_data/saved_sessions.json`.

---

### 3. 📝 Authentic JEE CBT Mock Test Arena (`pages/3_📝_JEE_Test.py`)
- **Pre-Configured Mock Papers**:
  - *Full-Length JEE Main Physics Test* (25 Questions: 20 MCQs + 5 Numericals, 60 minutes, 100 Marks)
  - *Mechanics Mastery Mock* (15 Questions, 40 minutes, 60 Marks)
  - *Electrodynamics & Magnetism Mock* (15 Questions, 40 minutes, 60 Marks)
  - *Optics, Waves & Modern Physics Mock* (15 Questions, 40 minutes, 60 Marks)
  - *Quick Sprint Physics Mock* (10 Questions, 20 minutes, 40 Marks)
- **NTA CBT Exam Interface**:
  - Live fragment countdown timer with warning state at $\le 5$ minutes.
  - Color-coded question palette: ⚪ Not Visited, 🔴 Not Answered, 🟢 Answered, 🟣 Marked for Review.
  - Save & Next, Mark for Review, and Clear Response capabilities.
  - Official JEE marking scheme ($+4$ for correct, $-1$ for incorrect, $0$ for unattempted).
- **Comprehensive Scorecard & Analytics**:
  - Score, Accuracy %, and Estimated JEE Percentile.
  - Granular question-by-question review with full step-by-step worked LaTeX solutions.
  - Local score history persistence (`practice_data/test_scores.json`).

---

## 💻 Tech Stack & Architecture

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/) (Multi-page App architecture)
- **Interactive Visualization**: [Plotly Graph Objects](https://plotly.com/python/) (Hardware-accelerated dynamic charts)
- **Numerical Computations**: [NumPy](https://numpy.org/) & Python Standard Math Library
- **Typography & Styling**: Custom responsive CSS (Glassmorphism, dark palette, neon accents)

---

## 🛠️ Local Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/aryamanpandya11/JEE-Physics-Lab.git
   cd JEE-Physics-Lab
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch PhysicsX Lab**:
   ```bash
   streamlit run app.py
   ```

---

## ☁️ Deployment on Streamlit Cloud

1. Commit your updated code to GitHub:
   ```bash
   git add .
   git commit -m "feat: enhance UI, add 5 virtual labs, 10-chapter practice and CBT mock test"
   git push origin main
   ```
2. Streamlit Community Cloud will automatically detect changes and rebuild the live app at `physicsx-lab.streamlit.app`.

---

© 2026 PhysicsX Lab · Dedicated to conceptual clarity in Physics education.
