
import json
import math
import random
import uuid
from pathlib import Path

import streamlit as st

# Active mock-test protection
test = st.session_state.get("mock_test")

if test and not test.get("submitted", False):
    test["forced_submission"] = True
    st.switch_page("pages/3_📝_JEE_Test.py")
    st.stop()
# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="JEE Physics Practice",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 JEE Physics Practice")
st.caption(
    "Practice projectile motion with numerical questions, MCQs, "
    "hints, worked solutions, and saved sessions."
)


# ============================================================
# SAVE FILES
# ============================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "practice_data"
DATA_FILE = DATA_DIR / "saved_sessions.json"


def load_sessions():
    """Load saved practice sessions from disk."""
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        st.warning("Saved sessions could not be loaded.")

    return {}


def save_sessions(sessions):
    """Save practice sessions to disk."""
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(sessions, file, indent=2, ensure_ascii=False)

        return True
    except OSError:
        st.error("Could not save your sessions. Check folder permissions.")
        return False


if "practice_sessions" not in st.session_state:
    st.session_state.practice_sessions = load_sessions()

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None


# ============================================================
# QUESTION BANK
# ============================================================

DIFFICULTIES = {
    "Basic": {
        "g": 10,
        "description": "Direct formula-based questions",
    },
    "Intermediate": {
        "g": 10,
        "description": "More calculation and conceptual application",
    },
    "JEE Challenge": {
        "g": 10,
        "description": "Multi-step JEE-style problems",
    },
}


def make_numerical_question(difficulty):
    """Generate a projectile-motion numerical question."""
    g = DIFFICULTIES[difficulty]["g"]

    if difficulty == "Basic":
        speed = random.choice([10, 20, 30, 40])
        angle = random.choice([30, 45, 60])
        kind = random.choice(["time", "height", "range"])

    elif difficulty == "Intermediate":
        speed = random.choice([20, 25, 30, 40, 50])
        angle = random.choice([30, 37, 45, 53, 60])
        kind = random.choice(["time", "height", "range"])

    else:
        speed = random.choice([20, 30, 40, 50, 60])
        angle = random.choice([30, 37, 45, 53, 60])
        kind = random.choice(["time", "height", "range", "horizontal"])

    radians = math.radians(angle)
    vx = speed * math.cos(radians)
    vy = speed * math.sin(radians)

    total_time = 2 * vy / g
    max_height = vy**2 / (2 * g)
    projectile_range = speed**2 * math.sin(2 * radians) / g

    if kind == "time":
        prompt = (
            f"A projectile is launched at {speed} m/s at an angle of "
            f"{angle}° to the horizontal. Find its total time of flight."
        )
        answer = total_time
        unit = "s"
        formula = "T = 2u sin(θ) / g"
        working = (
            f"T = 2 × {speed} × sin({angle}°) / {g}\n\n"
            f"T = {total_time:.4f} s"
        )

    elif kind == "height":
        prompt = (
            f"A projectile is launched at {speed} m/s at an angle of "
            f"{angle}° to the horizontal. Find its maximum height."
        )
        answer = max_height
        unit = "m"
        formula = "H = u² sin²(θ) / (2g)"
        working = (
            f"H = ({speed} × sin({angle}°))² / (2 × {g})\n\n"
            f"H = {max_height:.4f} m"
        )

    elif kind == "range":
        prompt = (
            f"A projectile is launched at {speed} m/s at an angle of "
            f"{angle}° to the horizontal on level ground. Find its range."
        )
        answer = projectile_range
        unit = "m"
        formula = "R = u² sin(2θ) / g"
        working = (
            f"R = {speed}² × sin(2 × {angle}°) / {g}\n\n"
            f"R = {projectile_range:.4f} m"
        )

    else:
        prompt = (
            f"A projectile is launched at {speed} m/s at an angle of "
            f"{angle}° to the horizontal. Find its horizontal velocity."
        )
        answer = vx
        unit = "m/s"
        formula = "uₓ = u cos(θ)"
        working = (
            f"uₓ = {speed} × cos({angle}°)\n\n"
            f"uₓ = {vx:.4f} m/s"
        )

    hints = [
        "Identify the given initial speed and launch angle.",
        f"Use g = {g} m/s² and resolve the initial velocity into components.",
        f"Relevant formula: {formula}.",
    ]

    return {
        "id": str(uuid.uuid4()),
        "type": "Numerical",
        "difficulty": difficulty,
        "prompt": prompt,
        "answer": round(answer, 4),
        "unit": unit,
        "formula": formula,
        "working": working,
        "hints": hints,
        "response": None,
        "checked": False,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
        "explanation": (
            f"The correct answer is approximately {answer:.4f} {unit}."
        ),
    }


def make_mcq_question(difficulty):
    """Generate a multiple-choice conceptual question."""
    questions = [
        {
            "prompt": (
                "At the highest point of projectile motion, "
                "which statement is correct?"
            ),
            "options": [
                "Both velocity and acceleration are zero",
                "Vertical velocity is zero, but acceleration is g downward",
                "Horizontal velocity is zero",
                "Acceleration is zero",
            ],
            "answer": "Vertical velocity is zero, but acceleration is g downward",
            "explanation": (
                "At the highest point, the vertical component of velocity "
                "is zero momentarily. Gravity still acts downward, and the "
                "horizontal velocity remains constant when air resistance "
                "is neglected."
            ),
            "hints": [
                "Consider the horizontal and vertical components separately.",
                "Gravity does not stop acting at the highest point.",
                "Only the vertical component of velocity becomes zero there.",
            ],
        },
        {
            "prompt": (
                "For a projectile launched and landing at the same height, "
                "the angle of projection for maximum range is:"
            ),
            "options": ["30°", "45°", "60°", "90°"],
            "answer": "45°",
            "explanation": (
                "For fixed launch speed on level ground, R = u² sin(2θ)/g. "
                "The range is maximum when sin(2θ) = 1, giving θ = 45°."
            ),
            "hints": [
                "Write the formula for horizontal range.",
                "The sine function has a maximum value of 1.",
                "Set 2θ = 90°.",
            ],
        },
        {
            "prompt": (
                "Ignoring air resistance, the horizontal acceleration "
                "of a projectile is:"
            ),
            "options": ["g", "g/2", "Zero", "Dependent on launch angle"],
            "answer": "Zero",
            "explanation": (
                "Gravity acts vertically downward. With air resistance "
                "neglected, there is no horizontal force, so horizontal "
                "acceleration is zero."
            ),
            "hints": [
                "Think about the direction of gravitational acceleration.",
                "There is no horizontal force in ideal projectile motion.",
                "Horizontal velocity remains constant.",
            ],
        },
        {
            "prompt": (
                "Two projectiles are launched with the same speed at "
                "angles θ and (90° − θ). If they land at the same height, "
                "their ranges are:"
            ),
            "options": [
                "Always different",
                "Equal",
                "In a 2:1 ratio",
                "Impossible to compare",
            ],
            "answer": "Equal",
            "explanation": (
                "Their ranges depend on sin(2θ). The complementary angle "
                "gives sin(180° − 2θ) = sin(2θ), so the ranges are equal."
            ),
            "hints": [
                "Use R = u² sin(2θ)/g.",
                "Substitute the complementary angle.",
                "Recall sin(180° − x) = sin(x).",
            ],
        },
    ]

    question = random.choice(questions).copy()
    question.update({
        "id": str(uuid.uuid4()),
        "type": "MCQ",
        "difficulty": difficulty,
        "response": None,
        "checked": False,
        "correct": False,
        "hint_level": 0,
        "solution_shown": False,
        "unit": "",
        "formula": "",
        "working": "",
    })

    return question


def make_question(difficulty, question_type):
    if question_type == "Numerical":
        return make_numerical_question(difficulty)

    if question_type == "MCQ":
        return make_mcq_question(difficulty)

    if random.choice(["Numerical", "MCQ"]) == "Numerical":
        return make_numerical_question(difficulty)

    return make_mcq_question(difficulty)


# ============================================================
# SESSION HELPERS
# ============================================================

def active_session():
    session_id = st.session_state.active_session_id

    if session_id is None:
        return None

    return st.session_state.practice_sessions.get(session_id)


def save_active_session():
    """Persist the current session."""
    save_sessions(st.session_state.practice_sessions)


def create_session(name, difficulty, question_type):
    session_id = str(uuid.uuid4())

    session = {
        "id": session_id,
        "name": name.strip() or "My Practice Session",
        "difficulty": difficulty,
        "question_type": question_type,
        "questions": [],
        "created_at": __import__("datetime").datetime.now().strftime(
            "%d %b %Y, %I:%M %p"
        ),
    }

    session["questions"].append(
        make_question(difficulty, question_type)
    )

    st.session_state.practice_sessions[session_id] = session
    st.session_state.active_session_id = session_id
    save_active_session()


def add_question(session):
    session["questions"].append(
        make_question(
            session["difficulty"],
            session["question_type"],
        )
    )
    save_active_session()


def get_stats(session):
    questions = session["questions"]
    attempted = [q for q in questions if q["checked"]]
    correct = sum(1 for q in attempted if q["correct"])

    return {
        "total": len(questions),
        "attempted": len(attempted),
        "correct": correct,
        "accuracy": (
            100 * correct / len(attempted)
            if attempted else 0
        ),
    }


# ============================================================
# SIDEBAR: SESSION MANAGEMENT
# ============================================================

with st.sidebar:
    st.header("📚 Practice Sessions")

    session_names = {
        session_id: (
            f"{session['name']} "
            f"({len(session.get('questions', []))} Q)"
        )
        for session_id, session
        in st.session_state.practice_sessions.items()
    }

    if session_names:
        ids = list(session_names.keys())

        current_id = st.session_state.active_session_id
        if current_id not in ids:
            current_id = ids[0]

        selected_id = st.selectbox(
            "Open a saved session",
            options=ids,
            index=ids.index(current_id),
            format_func=lambda x: session_names[x],
            key="session_selector",
        )

        if selected_id != st.session_state.active_session_id:
            st.session_state.active_session_id = selected_id
            st.rerun()

        st.divider()

        if st.button("➕ Create New Session", use_container_width=True):
            st.session_state.show_new_session_form = True

        if st.button("🗑️ Delete Current Session", use_container_width=True):
            if selected_id in st.session_state.practice_sessions:
                del st.session_state.practice_sessions[selected_id]

                remaining = list(st.session_state.practice_sessions.keys())
                st.session_state.active_session_id = (
                    remaining[0] if remaining else None
                )

                save_sessions(st.session_state.practice_sessions)
                st.rerun()

    else:
        st.info("You don't have any saved sessions yet.")
        if st.button("➕ Create Your First Session", use_container_width=True):
            st.session_state.show_new_session_form = True

    st.divider()
    st.caption("Your sessions are saved locally on this computer.")


# ============================================================
# NEW SESSION FORM
# ============================================================

if "show_new_session_form" not in st.session_state:
    st.session_state.show_new_session_form = (
        not bool(st.session_state.practice_sessions)
    )

if st.session_state.show_new_session_form:
    st.subheader("Create a Practice Session")

    with st.form("new_session_form"):
        session_name = st.text_input(
            "Session name",
            value="Projectile Motion Practice",
            help="Give this practice session a name.",
        )

        difficulty = st.selectbox(
            "Difficulty",
            options=list(DIFFICULTIES.keys()),
            index=0,
        )

        question_type = st.selectbox(
            "Question type",
            options=["Mixed", "Numerical", "MCQ"],
        )

        st.caption(DIFFICULTIES[difficulty]["description"])

        create_clicked = st.form_submit_button(
            "Start Practising 🚀",
            use_container_width=True,
        )

        if create_clicked:
            create_session(
                session_name,
                difficulty,
                question_type,
            )
            st.session_state.show_new_session_form = False
            st.rerun()


# ============================================================
# MAIN PRACTICE INTERFACE
# ============================================================

session = active_session()

if session is None:
    st.info("Create a session to start practising.")
    st.stop()

stats = get_stats(session)

st.subheader(session["name"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Questions", stats["total"])
col2.metric("Attempted", stats["attempted"])
col3.metric("Correct", stats["correct"])
col4.metric("Accuracy", f"{stats['accuracy']:.1f}%")

st.progress(
    stats["attempted"] / stats["total"]
    if stats["total"] else 0
)

st.caption(
    f"Difficulty: {session['difficulty']} · "
    f"Question type: {session['question_type']}"
)

st.divider()


# ============================================================
# DISPLAY QUESTIONS
# ============================================================

for index, question in enumerate(session["questions"]):
    with st.container(border=True):
        st.markdown(
            f"### Question {index + 1} · {question['type']}"
        )

        st.caption(question["difficulty"])
        st.write(question["prompt"])

        if question["type"] == "Numerical":
            st.caption(
                f"Enter your answer in {question['unit']}. "
                "You may use decimals."
            )

            # IMPORTANT:
            # This is a text input, not a number_input.
            # It starts blank, so it will not display 0.000.
            input_key = f"num_{session['id']}_{question['id']}"

            saved_response = question.get("response")
            initial_value = (
                str(saved_response)
                if saved_response is not None
                else ""
            )

            response_text = st.text_input(
                "Your numerical answer",
                value=initial_value,
                placeholder="Type your answer here...",
                key=input_key,
                disabled=question["checked"],
            )

            response = response_text.strip()

        else:
            options = question["options"]
            mcq_key = f"mcq_{session['id']}_{question['id']}"

            saved_response = question.get("response")
            default_index = (
                options.index(saved_response)
                if saved_response in options
                else None
            )

            response = st.radio(
                "Choose your answer",
                options=options,
                index=default_index,
                key=mcq_key,
                disabled=question["checked"],
            )

        button_col1, button_col2, button_col3 = st.columns(3)

        with button_col1:
            if not question["checked"]:
                check_clicked = st.button(
                    "Check Answer",
                    key=f"check_{session['id']}_{question['id']}",
                    use_container_width=True,
                )
            else:
                check_clicked = False

        with button_col2:
            if not question["checked"]:
                hint_clicked = st.button(
                    "💡 Hint",
                    key=f"hint_{session['id']}_{question['id']}",
                    use_container_width=True,
                )
            else:
                hint_clicked = False

        with button_col3:
            solution_clicked = st.button(
                "📖 Show Solution",
                key=f"solution_{session['id']}_{question['id']}",
                use_container_width=True,
            )

        if hint_clicked:
            question["hint_level"] = min(
                question["hint_level"] + 1,
                len(question["hints"]),
            )
            save_active_session()
            st.rerun()

        if question["hint_level"] > 0:
            st.markdown("**Hints**")
            for hint in question["hints"][:question["hint_level"]]:
                st.info(hint)

        if check_clicked:
            if question["type"] == "Numerical":
                if not response:
                    st.warning("Enter an answer before checking.")
                    continue

                try:
                    numeric_response = float(response)
                except ValueError:
                    st.warning("Please enter a valid number.")
                    continue

                question["response"] = numeric_response

                # Accept small rounding differences.
                tolerance = max(
                    0.05,
                    abs(question["answer"]) * 0.02,
                )

                question["correct"] = (
                    math.isfinite(numeric_response)
                    and abs(numeric_response - question["answer"])
                    <= tolerance
                )

            else:
                if response is None:
                    st.warning("Choose an option before checking.")
                    continue

                question["response"] = response
                question["correct"] = response == question["answer"]

            question["checked"] = True
            save_active_session()
            st.rerun()

        if question["checked"]:
            if question["correct"]:
                st.success("Correct! Well done. 🎉")
            else:
                st.error("Not quite. Review the solution below.")

            if question["type"] == "Numerical":
                st.write(
                    f"**Your answer:** {question['response']} "
                    f"{question['unit']}"
                )
                st.write(
                    f"**Correct answer:** {question['answer']:.4f} "
                    f"{question['unit']}"
                )
            else:
                st.write(f"**Your answer:** {question['response']}")
                st.write(f"**Correct answer:** {question['answer']}")

        if solution_clicked:
            question["solution_shown"] = True
            save_active_session()

        if question["solution_shown"] or question["checked"]:
            st.markdown("#### Worked Solution")

            if question["type"] == "Numerical":
                st.markdown(f"**Formula:** `{question['formula']}`")
                st.code(question["working"], language="text")
            else:
                st.write(question["explanation"])


# ============================================================
# SESSION ACTIONS
# ============================================================

st.divider()
st.subheader("Keep Practising")

action_col1, action_col2 = st.columns(2)

with action_col1:
    if st.button("➕ Generate Next Question", use_container_width=True):
        add_question(session)
        st.rerun()

with action_col2:
    if st.button("🔄 Start a New Session", use_container_width=True):
        st.session_state.show_new_session_form = True
        st.rerun()


# ============================================================
# SESSION SUMMARY
# ============================================================

stats = get_stats(session)

st.divider()
st.subheader("📊 Session Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

summary_col1.metric("Total Questions", stats["total"])
summary_col2.metric("Questions Attempted", stats["attempted"])
summary_col3.metric("Correct Answers", stats["correct"])

if stats["attempted"]:
    st.write(f"**Current accuracy:** {stats['accuracy']:.1f}%")

    if stats["attempted"] == stats["total"]:
        if stats["accuracy"] >= 80:
            st.success("Excellent work! You're building a strong foundation.")
        elif stats["accuracy"] >= 50:
            st.info("Good effort. Review the mistakes and practise another set.")
        else:
            st.info(
                "Focus on understanding the formulas and worked solutions "
                "before attempting another set."
            )
else:
    st.write("Attempt your first question to start tracking your progress.")

st.caption(
    "Numerical answers allow a small rounding tolerance. "
    "Projectile-motion calculations assume no air resistance and use "
    "g = 10 m/s²."
)
