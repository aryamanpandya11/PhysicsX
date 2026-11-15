"""
PhysicsX Lab - Comprehensive JEE Physics Question Bank & Generator
Covers 10 core Class 11 & 12 JEE Main and Advanced chapters with MCQs,
Numerical Value questions, 3-tier progressive hints, and step-by-step LaTeX solutions.
"""

import math
import random
import uuid

CHAPTERS = [
    "All Chapters (Mixed)",
    "Kinematics & Projectiles",
    "Newton's Laws & Friction",
    "Work, Power & Energy",
    "Rotational Dynamics",
    "Gravitation & Satellites",
    "SHM & Mechanical Waves",
    "Electrostatics & Capacitance",
    "Current Electricity & Magnetism",
    "Ray & Wave Optics",
    "Thermodynamics & Modern Physics",
]

DIFFICULTIES = {
    "Basic": "Direct formula-based JEE Main fundamentals",
    "Intermediate": "Standard multi-step JEE Main level problems",
    "JEE Challenge": "Multi-concept JEE Advanced caliber problems",
}


def make_kinematics_numerical(difficulty):
    g = 10.0
    if difficulty == "Basic":
        speed = random.choice([20, 25, 30, 40])
        angle = random.choice([30, 45, 60])
        kind = random.choice(["flight_time", "max_height", "range"])
    elif difficulty == "Intermediate":
        speed = random.choice([25, 35, 45, 50])
        angle = random.choice([37, 53, 30, 45])
        kind = random.choice(["flight_time", "max_height", "range", "cliff"])
    else:
        speed = random.choice([30, 40, 50])
        angle = random.choice([30, 45, 60])
        kind = random.choice(["cliff", "apex_speed", "trajectory_height"])

    rad = math.radians(angle)
    sin_a = math.sin(rad)
    cos_a = math.cos(rad)

    if kind == "flight_time":
        ans = (2 * speed * sin_a) / g
        prompt = (
            f"A projectile is launched from flat ground with initial speed $u = {speed}\\text{{ m/s}}$ "
            f"at an elevation angle of $\\theta = {angle}^\\circ$. "
            f"Taking $g = 10\\text{{ m/s}}^2$, compute the total time of flight $T$ in seconds."
        )
        formula = r"T = \frac{2u\sin\theta}{g}"
        working = (
            f"1. Initial vertical velocity: $u_y = u\\sin\\theta = {speed} \\times {sin_a:.3f} = {speed*sin_a:.2f}\\text{{ m/s}}$\n\n"
            f"2. Time of flight: $T = \\frac{{2 \\times {speed*sin_a:.2f}}}{{10}} = {ans:.2f}\\text{{ s}}$"
        )
        unit = "s"
    elif kind == "max_height":
        ans = (speed * sin_a) ** 2 / (2 * g)
        prompt = (
            f"A stone is projected from the ground with speed $u = {speed}\\text{{ m/s}}$ at $\\theta = {angle}^\\circ$. "
            f"Find the maximum vertical height $H_{{max}}$ attained above the ground in metres ($g = 10\\text{{ m/s}}^2$)."
        )
        formula = r"H_{\max} = \frac{u^2\sin^2\theta}{2g}"
        working = (
            f"1. $u_y = {speed}\\sin({angle}^\\circ) = {speed*sin_a:.2f}\\text{{ m/s}}$\n\n"
            f"2. $H = \\frac{{({speed*sin_a:.2f})^2}}{{2 \\times 10}} = \\frac{{{((speed*sin_a)**2):.2f}}}{{20}} = {ans:.2f}\\text{{ m}}$"
        )
        unit = "m"
    elif kind == "range":
        ans = (speed**2 * math.sin(2 * rad)) / g
        prompt = (
            f"A shell is fired with velocity $u = {speed}\\text{{ m/s}}$ at an angle of {angle}° to the horizontal on level terrain. "
            f"Calculate its horizontal range $R$ in metres ($g = 10\\text{{ m/s}}^2$)."
        )
        formula = r"R = \frac{u^2\sin(2\theta)}{g}"
        working = (
            f"1. $\\sin(2\\theta) = \\sin({2*angle}^\\circ) = {math.sin(2*rad):.4f}$\n\n"
            f"2. $R = \\frac{{{speed}^2 \\times {math.sin(2*rad):.4f}}}{{10}} = {ans:.2f}\\text{{ m}}$"
        )
        unit = "m"
    elif kind == "cliff":
        h = random.choice([20, 45, 80])
        # t = sqrt(2h/g)
        ans_t = math.sqrt(2 * h / g)
        ans = speed * ans_t
        prompt = (
            f"A body is projected horizontally with velocity $u = {speed}\\text{{ m/s}}$ from the top of a cliff of height $h = {h}\\text{{ m}}$. "
            f"Find the horizontal distance (in metres) from the base of the cliff to the point where it strikes the ground ($g = 10\\text{{ m/s}}^2$)."
        )
        formula = r"x = u \cdot \sqrt{\frac{2h}{g}}"
        working = (
            f"1. Vertical fall time: $h = \\frac{{1}}{{2}}gt^2 \\implies t = \\sqrt{{\\frac{{2 \\times {h}}}{{10}}}} = {ans_t:.2f}\\text{{ s}}$\n\n"
            f"2. Horizontal distance: $x = u \\times t = {speed} \\times {ans_t:.2f} = {ans:.2f}\\text{{ m}}$"
        )
        unit = "m"
    else:
        ans = speed * cos_a
        prompt = (
            f"A projectile is fired at $u = {speed}\\text{{ m/s}}$ at $\\theta = {angle}^\\circ$ to horizontal. "
            f"What is its kinetic speed at the highest point of its trajectory in $\\text{{m/s}}$?"
        )
        formula = r"v_{\text{apex}} = u_x = u\cos\theta"
        working = f"$v_{{apex}} = {speed} \\times \\cos({angle}^\\circ) = {speed} \\times {cos_a:.3f} = {ans:.2f}\\text{{ m/s}}$"
        unit = "m/s"

    hints = [
        "Recall that horizontal and vertical motions in projectile trajectories are completely decoupled.",
        f"Relevant formula: ${formula}$. Acceleration along vertical is $-g$, along horizontal is $0$.",
        f"Substitute $u = {speed}$, $\\theta = {angle}^\\circ$, and $g = 10$. Keep standard SI units.",
    ]

    return {
        "id": str(uuid.uuid4()),
        "chapter": "Kinematics & Projectiles",
        "type": "Numerical",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": round(ans, 2),
        "tolerance": 0.08,
        "unit": unit,
        "formula": formula,
        "working": working,
        "hints": hints,
        "checked": False,
        "response": None,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
    }


def make_nlm_numerical(difficulty):
    m1 = random.choice([2, 4, 6])
    m2 = random.choice([3, 5, 8])
    g = 10.0
    if m1 > m2:
        m1, m2 = m2, m1  # m2 is heavier

    acc = (m2 - m1) * g / (m1 + m2)
    t = (2 * m1 * m2 * g) / (m1 + m2)

    kind = random.choice(["acc", "tension"])
    if kind == "acc":
        ans = acc
        prompt = (
            f"In an ideal Atwood machine, two masses $m_1 = {m1}\\text{{ kg}}$ and $m_2 = {m2}\\text{{ kg}}$ are connected "
            f"by a light inextensible string over a frictionless pulley. Find the magnitude of acceleration of the system in $\\text{{m/s}}^2$ ($g = 10\\text{{ m/s}}^2$)."
        )
        formula = r"a = \frac{m_2 - m_1}{m_1 + m_2} g"
        working = (
            f"Net pulling force: $F_{{net}} = (m_2 - m_1)g = ({m2} - {m1}) \\times 10 = {(m2-m1)*10}\\text{{ N}}$\n\n"
            f"Total mass: $M = {m1} + {m2} = {m1+m2}\\text{{ kg}}$\n\n"
            f"Acceleration: $a = \\frac{{{(m2-m1)*10}}}{{{m1+m2}}} = {ans:.2f}\\text{{ m/s}}^2$"
        )
        unit = "m/s²"
    else:
        ans = t
        prompt = (
            f"Two blocks of masses $m_1 = {m1}\\text{{ kg}}$ and $m_2 = {m2}\\text{{ kg}}$ are suspended via a massless string over a smooth pulley. "
            f"Determine the tension $T$ in the string in Newtons ($g = 10\\text{{ m/s}}^2$)."
        )
        formula = r"T = \frac{2 m_1 m_2}{m_1 + m_2} g"
        working = (
            f"$T = \\frac{{2 \\times {m1} \\times {m2} \\times 10}}{{{m1} + {m2}}} = \\frac{{{20*m1*m2}}}{{{m1+m2}}} = {ans:.2f}\\text{{ N}}$"
        )
        unit = "N"

    hints = [
        "Draw Free Body Diagrams (FBD) for both masses $m_1$ and $m_2$.",
        f"Apply Newton's second law: $m_2 g - T = m_2 a$ and $T - m_1 g = m_1 a$.",
        f"Use formula ${formula}$.",
    ]

    return {
        "id": str(uuid.uuid4()),
        "chapter": "Newton's Laws & Friction",
        "type": "Numerical",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": round(ans, 2),
        "tolerance": 0.08,
        "unit": unit,
        "formula": formula,
        "working": working,
        "hints": hints,
        "checked": False,
        "response": None,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
    }


def make_wep_numerical(difficulty):
    m = random.choice([2, 5, 10])
    k = random.choice([200, 500, 800])
    x = random.choice([0.1, 0.2, 0.4])  # compression
    # 0.5 * k * x^2 = 0.5 * m * v^2 => v = x * sqrt(k/m)
    v = x * math.sqrt(k / m)
    prompt = (
        f"A horizontal spring of spring constant $k = {k}\\text{{ N/m}}$ is compressed by $x = {x}\\text{{ m}}$ and releases a block "
        f"of mass $m = {m}\\text{{ kg}}$ on a frictionless surface. What is the maximum velocity acquired by the block in $\\text{{m/s}}$?"
    )
    formula = r"\frac{1}{2} k x^2 = \frac{1}{2} m v^2 \implies v = x\sqrt{\frac{k}{m}}"
    working = (
        f"1. Potential energy stored in spring: $U = \\frac{{1}}{{2}} k x^2 = 0.5 \\times {k} \\times ({x})^2 = {0.5*k*x**2:.2f}\\text{{ J}}$\n\n"
        f"2. Kinetic energy of block: $K = \\frac{{1}}{{2}} m v^2 = {0.5*m} v^2$\n\n"
        f"3. Equating $K = U \\implies v = {x} \\times \\sqrt{{\\frac{{{k}}}{{{m}}}}} = {v:.2f}\\text{{ m/s}}$"
    )

    hints = [
        "Apply the Law of Conservation of Mechanical Energy since the surface is frictionless.",
        f"Elastic potential energy stored in a spring is $\\frac{{1}}{{2}}kx^2$.",
        f"Solve for $v$: $v = x\\sqrt{{k/m}}$.",
    ]

    return {
        "id": str(uuid.uuid4()),
        "chapter": "Work, Power & Energy",
        "type": "Numerical",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": round(v, 2),
        "tolerance": 0.05,
        "unit": "m/s",
        "formula": formula,
        "working": working,
        "hints": hints,
        "checked": False,
        "response": None,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
    }


def make_electrostatics_numerical(difficulty):
    # C = q/V or Energy = 0.5 * C * V^2
    c_uF = random.choice([2, 5, 10, 20])
    v_volts = random.choice([10, 20, 50, 100])
    # Energy in mJ = 0.5 * C * V^2 * 1e-6 * 1e3 = 0.5 * C * V^2 * 1e-3
    energy_mJ = 0.5 * c_uF * 1e-6 * (v_volts**2) * 1000

    prompt = (
        f"A parallel-plate capacitor of capacitance $C = {c_uF}\\,\\mu\\text{{F}}$ is charged across a battery of voltage $V = {v_volts}\\text{{ V}}$. "
        f"Calculate the electrostatic potential energy stored in the capacitor in milli-Joules ($\\text{{mJ}}$)."
    )
    formula = r"U = \frac{1}{2} C V^2"
    working = (
        f"1. $C = {c_uF} \\times 10^{{-6}}\\,\\text{{F}}$, $V = {v_volts}\\,\\text{{V}}$\n\n"
        f"2. $U = \\frac{{1}}{{2}} \\times ({c_uF} \\times 10^{{-6}}) \\times ({v_volts})^2 = {0.5*c_uF*1e-6*(v_volts**2):.5f}\\,\\text{{J}}$\n\n"
        f"3. In milli-Joules: $U = {energy_mJ:.2f}\\,\\text{{mJ}}$"
    )

    hints = [
        "Identify the capacitance and the applied potential difference.",
        f"Use formula: $U = \\frac{{1}}{{2}}CV^2$.",
        "Remember to convert capacitance from $\\mu\\text{F}$ to Farads, and finally express the answer in $\\text{mJ}$ ($1\\text{ J} = 1000\\text{ mJ}$).",
    ]

    return {
        "id": str(uuid.uuid4()),
        "chapter": "Electrostatics & Capacitance",
        "type": "Numerical",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": round(energy_mJ, 2),
        "tolerance": 0.05,
        "unit": "mJ",
        "formula": formula,
        "working": working,
        "hints": hints,
        "checked": False,
        "response": None,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
    }


def make_modern_numerical(difficulty):
    # Photoelectric effect: K_max = h * nu - phi in eV
    # E = 1240 / lambda(nm)
    lamb_nm = random.choice([200, 250, 300, 350])
    work_func = random.choice([2.0, 2.5, 3.0])
    photon_energy = 1240.0 / lamb_nm
    k_max = max(0.0, photon_energy - work_func)

    prompt = (
        f"Light of wavelength $\\lambda = {lamb_nm}\\text{{ nm}}$ is incident on a photosensitive metal surface of work function $\\Phi_0 = {work_func:.1f}\\text{{ eV}}$. "
        f"Taking $hc \\approx 1240\\text{{ eV}}\\cdot\\text{{nm}}$, find the maximum kinetic energy $K_{{\\max}}$ of emitted photoelectrons in $\\text{{eV}}$."
    )
    formula = r"K_{\max} = \frac{hc}{\lambda} - \Phi_0"
    working = (
        f"1. Energy of incident photon: $E = \\frac{{1240}}{{{lamb_nm}}} = {photon_energy:.2f}\\text{{ eV}}$\n\n"
        f"2. Einstein's equation: $K_{{\\max}} = E - \\Phi_0 = {photon_energy:.2f} - {work_func} = {k_max:.2f}\\text{{ eV}}$"
    )

    hints = [
        "Recall Einstein's Photoelectric Equation: $h\\nu = \\Phi_0 + K_{\\max}$.",
        "Compute incident photon energy using the shortcut $E(\\text{eV}) = \\frac{1240}{\\lambda(\\text{nm})}$.",
        f"Subtract the work function $\\Phi_0 = {work_func}\\text{{ eV}}$ from the incident energy.",
    ]

    return {
        "id": str(uuid.uuid4()),
        "chapter": "Thermodynamics & Modern Physics",
        "type": "Numerical",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": round(k_max, 2),
        "tolerance": 0.05,
        "unit": "eV",
        "formula": formula,
        "working": working,
        "hints": hints,
        "checked": False,
        "response": None,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
    }


# Static Curated Question Bank of High-Yield JEE MCQs
CONCEPTUAL_MCQS = [
    # Kinematics
    {
        "chapter": "Kinematics & Projectiles",
        "difficulty": "Basic",
        "prompt": "At the highest point of projectile motion on flat ground, which of the following is non-zero?",
        "options": [
            "Vertical velocity",
            "Horizontal velocity",
            "Vertical displacement from launch plane",
            "Both horizontal velocity and acceleration",
        ],
        "answer": "Both horizontal velocity and acceleration",
        "explanation": "At the apex, $v_y = 0$, but the horizontal velocity $v_x = u\\cos\\theta$ remains constant, and downward acceleration $a_y = -g$ is always present.",
        "hints": [
            "Break the motion into independent $x$ and $y$ components.",
            "Does gravity ever switch off during flight?",
            "Remember that only the vertical velocity momentarily vanishes at peak height.",
        ],
    },
    {
        "chapter": "Kinematics & Projectiles",
        "difficulty": "Intermediate",
        "prompt": "Two bullets are fired simultaneously horizontally with different speeds $u_1$ and $u_2$ ($u_1 > u_2$) from the same height. Which one strikes the ground first?",
        "options": [
            "The faster bullet ($u_1$)",
            "The slower bullet ($u_2$)",
            "Both strike simultaneously",
            "Depends on the bullet masses",
        ],
        "answer": "Both strike simultaneously",
        "explanation": "Vertical motion is governed strictly by $h = \\frac{1}{2}gt^2$. Since both have zero initial vertical velocity ($u_y = 0$) and identical drop heights, $t = \\sqrt{2h/g}$ for both.",
        "hints": [
            "What is the initial vertical velocity of each bullet?",
            "Look at the vertical equation of motion under constant gravity.",
            "Horizontal speed affects range, not the vertical time of fall.",
        ],
    },
    # Newton's Laws
    {
        "chapter": "Newton's Laws & Friction",
        "difficulty": "Basic",
        "prompt": "A block of mass $m$ rests on an incline of angle $\\theta$. If the coefficient of static friction is $\\mu_s > \\tan\\theta$, the frictional force acting on the block is:",
        "options": [
            "$\\mu_s mg \\cos\\theta$",
            "$mg \\sin\\theta$",
            "$\\mu_s mg$",
            "Zero",
        ],
        "answer": "$mg \\sin\\theta$",
        "explanation": "Since $\\tan\\theta < \\mu_s$, the block is at rest. Static friction is self-adjusting and precisely equals the opposing component of gravity: $f_s = mg\\sin\\theta$.",
        "hints": [
            "Is the block sliding or at rest?",
            "Static friction does not automatically take its maximum limiting value $\\mu_s N$.",
            "Equate forces parallel to the inclined plane for equilibrium.",
        ],
    },
    # Work, Energy & Power
    {
        "chapter": "Work, Power & Energy",
        "difficulty": "Intermediate",
        "prompt": "A particle moves in a circular path of radius $R$ under the action of a central attractive force $F = -k/r^2$. The total mechanical energy $E$ of the system is related to its kinetic energy $K$ by:",
        "options": ["$E = K$", "$E = -K$", "$E = 2K$", "$E = -2K$"],
        "answer": "$E = -K$",
        "explanation": "From the Virial Theorem for inverse-square force ($U = -k/r$), $\\frac{m v^2}{r} = \\frac{k}{r^2} \\implies K = \\frac{k}{2r}$. Since $U = -\\frac{k}{r} = -2K$, total energy $E = K + U = K - 2K = -K$.",
        "hints": [
            "Equate centripetal force to the attractive inverse-square force.",
            "Derive potential energy by integrating $U = -\\int F\\,dr$.",
            "Substitute $U = -2K$ into $E = K + U$.",
        ],
    },
    # Rotational Dynamics
    {
        "chapter": "Rotational Dynamics",
        "difficulty": "Intermediate",
        "prompt": "A solid cylinder and a hollow cylinder of identical mass and radius roll down an inclined plane without slipping from rest. Which reaches the bottom first?",
        "options": [
            "Solid cylinder",
            "Hollow cylinder",
            "Both reach simultaneously",
            "Depends on the incline angle",
        ],
        "answer": "Solid cylinder",
        "explanation": "Acceleration in rolling without slipping is $a = \\frac{g\\sin\\theta}{1 + I/(mR^2)}$. For solid cylinder, $I/(mR^2) = 0.5$, while for hollow cylinder it is $1.0$. Thus, $a_{solid} > a_{hollow}$.",
        "hints": [
            "Compare the radius of gyration $k$ or moment of inertia $I$ of both cylinders.",
            "Rolling acceleration formula: $a = \\frac{g\\sin\\theta}{1 + k^2/R^2}$.",
            "Smaller rotational inertia means faster linear acceleration down the incline.",
        ],
    },
    # Gravitation
    {
        "chapter": "Gravitation & Satellites",
        "difficulty": "Basic",
        "prompt": "If the radius of the Earth were to shrink by 1% while its mass remains constant, the acceleration due to gravity on its surface would:",
        "options": [
            "Decrease by 2%",
            "Increase by 2%",
            "Increase by 1%",
            "Remain unchanged",
        ],
        "answer": "Increase by 2%",
        "explanation": "Since $g = GM/R^2$, taking logarithmic differentiation gives $\\frac{\\Delta g}{g} \\approx -2\\frac{\\Delta R}{R}$. For $\\Delta R/R = -1\\%$, $\\Delta g/g = +2\\%$.",
        "hints": [
            "Write the formula for surface gravity $g$ in terms of mass $M$ and radius $R$.",
            "Use fractional error approximation: $g \\propto R^{-2}$.",
            "Differentiate: $\\Delta g / g = -2 (\\Delta R / R)$.",
        ],
    },
    # SHM & Waves
    {
        "chapter": "SHM & Mechanical Waves",
        "difficulty": "Intermediate",
        "prompt": "A simple pendulum has time period $T$ on Earth. If it is placed inside a lift accelerating upward with acceleration $a = g$, its new time period becomes:",
        "options": ["$T$", "$T/\\sqrt{2}$", "$\\sqrt{2}T$", "$2T$"],
        "answer": "$T/\\sqrt{2}$",
        "explanation": "In an upward accelerating elevator, effective gravity becomes $g_{eff} = g + a = 2g$. Since $T = 2\\pi\\sqrt{L/g_{eff}}$, $T' = 2\\pi\\sqrt{L/(2g)} = T/\\sqrt{2}$.",
        "hints": [
            "Consider the pseudo-force acting on the bob in the accelerating reference frame.",
            "Effective acceleration due to gravity is $g_{eff} = g + a$.",
            "Substitute $g_{eff} = 2g$ into the pendulum time period formula.",
        ],
    },
    # Electrostatics
    {
        "chapter": "Electrostatics & Capacitance",
        "difficulty": "Intermediate",
        "prompt": "A parallel plate capacitor is charged and then disconnected from the battery. If the plate separation is doubled, what happens to the stored energy?",
        "options": [
            "It is halved",
            "It doubles",
            "It quadruples",
            "It remains constant",
        ],
        "answer": "It doubles",
        "explanation": "When disconnected, charge $Q$ is conserved. Capacitance $C = \\frac{\\varepsilon_0 A}{d}$ is halved when separation $d$ doubles. Stored energy $U = \\frac{Q^2}{2C}$ therefore doubles.",
        "hints": [
            "Is potential $V$ constant or charge $Q$ constant after battery disconnection?",
            "Express stored energy in terms of the conserved quantity: $U = Q^2 / (2C)$.",
            "How does capacitance $C$ depend on plate separation $d$?",
        ],
    },
    # Current Electricity
    {
        "chapter": "Current Electricity & Magnetism",
        "difficulty": "Basic",
        "prompt": "When a uniform wire of resistance $R$ is stretched to double its original length, its new electrical resistance becomes:",
        "options": ["$2R$", "$4R$", "$R/2$", "$R/4$"],
        "answer": "$4R$",
        "explanation": "Volume $V = A\\cdot L$ is constant. Stretching to $2L$ causes the cross-sectional area to halve ($A/2$). New resistance $R' = \\rho \\frac{2L}{A/2} = 4\\left(\\rho \\frac{L}{A}\\right) = 4R$.",
        "hints": [
            "The volume and mass of the wire remain strictly constant when stretched.",
            "If length doubles, what happens to the cross-sectional area?",
            "Use $R = \\rho L/A$.",
        ],
    },
    # Optics
    {
        "chapter": "Ray & Wave Optics",
        "difficulty": "Intermediate",
        "prompt": "In a Young's Double Slit Experiment, if the entire apparatus is immersed in water (refractive index $\\mu = 4/3$), the fringe width $\\beta$ will:",
        "options": [
            "Increase by a factor of 4/3",
            "Decrease to 3/4 of its original value",
            "Remain unchanged",
            "Become zero",
        ],
        "answer": "Decrease to 3/4 of its original value",
        "explanation": "In water, wavelength decreases: $\\lambda' = \\lambda / \\mu = \\frac{3}{4}\\lambda$. Since fringe width $\\beta = \\frac{\\lambda D}{d}$, $\\beta' = \\frac{3}{4}\\beta$.",
        "hints": [
            "How does wavelength change when light enters an optical medium of refractive index $\\mu$?",
            "Fringe width equation: $\\beta = \\frac{\\lambda D}{d}$.",
            "Substitute $\\lambda' = \\lambda / \\mu$.",
        ],
    },
    # Thermodynamics & Modern
    {
        "chapter": "Thermodynamics & Modern Physics",
        "difficulty": "Intermediate",
        "prompt": "An ideal gas undergoes an adiabatic expansion where its volume doubles. If $\\gamma = 1.4$, the final pressure $P_f$ compared to initial $P_i$ is:",
        "options": [
            "$P_i / 2$",
            "$P_i / 2^{1.4}$",
            "$P_i \\times 2^{1.4}$",
            "$P_i / 1.4$",
        ],
        "answer": "$P_i / 2^{1.4}$",
        "explanation": "For an adiabatic process, $P V^\\gamma = \\text{constant}$. Hence $P_f (2V_i)^\\gamma = P_i V_i^\\gamma \\implies P_f = P_i / 2^\\gamma = P_i / 2^{1.4}$.",
        "hints": [
            "State the governing equation of state for a reversible adiabatic process.",
            "Write $P_1 V_1^\\gamma = P_2 V_2^\\gamma$.",
            "Substitute $V_2 = 2V_1$ and isolate $P_2$.",
        ],
    },
    {
        "chapter": "Thermodynamics & Modern Physics",
        "difficulty": "JEE Challenge",
        "prompt": "According to Bohr's model of the hydrogen atom, the orbital radius $r_n$ and orbital velocity $v_n$ of an electron in quantum state $n$ scale as:",
        "options": [
            "$r_n \\propto n^2,\\; v_n \\propto 1/n$",
            "$r_n \\propto n,\\; v_n \\propto 1/n^2$",
            "$r_n \\propto 1/n,\\; v_n \\propto n^2$",
            "$r_n \\propto n^2,\\; v_n \\propto n$",
        ],
        "answer": "$r_n \\propto n^2,\\; v_n \\propto 1/n$",
        "explanation": "Bohr's quantization condition is $m v r = \\frac{n h}{2\\pi}$. Balance with Coulomb force gives $r_n = \\frac{\\varepsilon_0 n^2 h^2}{\\pi m e^2} \\propto n^2$, and $v_n = \\frac{e^2}{2\\varepsilon_0 n h} \\propto \\frac{1}{n}$.",
        "hints": [
            "Recall the quantization of angular momentum: $L = mvr = n\\hbar$.",
            "Balance electrostatic attraction with centripetal force: $\\frac{m v^2}{r} = \\frac{e^2}{4\\pi\\varepsilon_0 r^2}$.",
            "Solve the system for $r_n$ and $v_n$ as functions of principal quantum number $n$.",
        ],
    },
]


def get_practice_question(chapter="All Chapters (Mixed)", difficulty="Basic", q_type="Mixed"):
    """Returns a generated or curated question matching user filters."""
    # Filter candidate MCQs
    valid_mcqs = [
        q for q in CONCEPTUAL_MCQS
        if (chapter == "All Chapters (Mixed)" or q["chapter"] == chapter)
        and (difficulty == "All" or q["difficulty"] == difficulty)
    ]
    if not valid_mcqs and chapter != "All Chapters (Mixed)":
        valid_mcqs = [q for q in CONCEPTUAL_MCQS if q["chapter"] == chapter]
    if not valid_mcqs:
        valid_mcqs = CONCEPTUAL_MCQS

    pick_type = q_type
    if pick_type == "Mixed":
        pick_type = random.choice(["MCQ", "Numerical"])

    if pick_type == "MCQ":
        base = random.choice(valid_mcqs).copy()
        base.update({
            "id": str(uuid.uuid4()),
            "type": "MCQ",
            "unit": "",
            "formula": "",
            "working": "",
            "checked": False,
            "response": None,
            "correct": False,
            "hint_level": 0,
            "solution_shown": False,
        })
        return base
    else:
        # Generate numerical question based on chapter
        if "Kinematics" in chapter:
            return make_kinematics_numerical(difficulty if difficulty in DIFFICULTIES else "Basic")
        elif "Newton" in chapter:
            return make_nlm_numerical(difficulty if difficulty in DIFFICULTIES else "Intermediate")
        elif "Work" in chapter:
            return make_wep_numerical(difficulty if difficulty in DIFFICULTIES else "Intermediate")
        elif "Electrostatics" in chapter or "Current" in chapter:
            return make_electrostatics_numerical(difficulty if difficulty in DIFFICULTIES else "Basic")
        elif "Modern" in chapter or "Thermo" in chapter:
            return make_modern_numerical(difficulty if difficulty in DIFFICULTIES else "Basic")
        else:
            gen_func = random.choice([
                make_kinematics_numerical,
                make_nlm_numerical,
                make_wep_numerical,
                make_electrostatics_numerical,
                make_modern_numerical,
            ])
            return gen_func(difficulty if difficulty in DIFFICULTIES else "Basic")
