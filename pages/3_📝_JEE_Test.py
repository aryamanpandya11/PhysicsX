
import math
import random
import time
import uuid
import json
from pathlib import Path

import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="JEE Physics Mock Test",
    page_icon="📝",
    layout="wide",
)

MARKS_CORRECT = 4
MARKS_INCORRECT = -1
MARKS_UNATTEMPTED = 0
TOTAL_QUESTIONS = 15
MAX_MARKS = 60

SCORE_FILE = (
    Path(__file__).resolve().parent.parent
    / "practice_data"
    / "test_scores.json"
)

st.title("📝 JEE Physics Mock Test")
st.caption("Test 01 · Projectile Motion · JEE Main style")


# ============================================================
# QUESTION BANK — 10 MCQs + 5 NUMERICALS
# ============================================================

QUESTION_BANK = [
    {
        "id": "M01",
        "type": "MCQ",
        "difficulty": "Basic",
        "topic": "Time of flight",
        "question": (
            "A projectile is launched at 20 m/s at an angle of 30° "
            "to the horizontal. Taking g = 10 m/s², its time of flight is:"
        ),
        "options": ["1 s", "2 s", "2√3 s", "4 s"],
        "answer": "2 s",
        "explanation": (
            "T = 2u sin θ / g = 2 × 20 × sin 30° / 10 = 2 s."
        ),
    },
    {
        "id": "M02",
        "type": "MCQ",
        "difficulty": "Basic",
        "topic": "Projectile motion concepts",
        "question": "At the highest point of projectile motion:",
        "options": [
            "Velocity and acceleration are both zero",
            "Vertical velocity is zero, acceleration is downward",
            "Horizontal velocity is zero",
            "Acceleration is zero",
        ],
        "answer": "Vertical velocity is zero, acceleration is downward",
        "explanation": (
            "The vertical velocity becomes zero momentarily, but gravity "
            "continues to act downward with acceleration g."
        ),
    },
    {
        "id": "M03",
        "type": "MCQ",
        "difficulty": "Basic",
        "topic": "Horizontal range",
        "question": (
            "For a projectile launched and landing at the same height, "
            "the angle giving maximum range is:"
        ),
        "options": ["30°", "45°", "60°", "90°"],
        "answer": "45°",
        "explanation": (
            "R = u² sin 2θ / g. Range is maximum when sin 2θ = 1, "
            "so θ = 45°."
        ),
    },
    {
        "id": "M04",
        "type": "MCQ",
        "difficulty": "Intermediate",
        "topic": "Complementary angles",
        "question": (
            "Two projectiles are launched with the same speed at angles "
            "30° and 60° on level ground. Their ranges are:"
        ),
        "options": [
            "In the ratio 1:2",
            "In the ratio 2:1",
            "Equal",
            "Impossible to compare",
        ],
        "answer": "Equal",
        "explanation": (
            "The angles are complementary. Since sin 60° = sin 120°, "
            "their ranges are equal."
        ),
    },
    {
        "id": "M05",
        "type": "MCQ",
        "difficulty": "Intermediate",
        "topic": "Velocity components",
        "question": (
            "A projectile is launched at 20 m/s at 60° to the horizontal. "
            "Its initial horizontal velocity is:"
        ),
        "options": ["10 m/s", "10√3 m/s", "20√3 m/s", "20 m/s"],
        "answer": "10 m/s",
        "explanation": "uₓ = u cos θ = 20 × cos 60° = 10 m/s.",
    },
    {
        "id": "M06",
        "type": "MCQ",
        "difficulty": "Intermediate",
        "topic": "Maximum height",
        "question": (
            "If the initial speed of a projectile is doubled while its "
            "launch angle stays the same, its maximum height becomes:"
        ),
        "options": ["Two times", "Four times", "Half", "Unchanged"],
        "answer": "Four times",
        "explanation": (
            "H = u² sin² θ / (2g). Maximum height is proportional to u², "
            "so doubling u makes the height four times as large."
        ),
    },
    {
        "id": "M07",
        "type": "MCQ",
        "difficulty": "JEE Challenge",
        "topic": "Trajectory equation",
        "question": (
            "For a projectile launched with speed u at angle θ, "
            "the trajectory equation is:"
        ),
        "options": [
            "y = x tan θ − gx²/(2u² cos² θ)",
            "y = x cot θ − gx²/(2u² sin² θ)",
            "y = x tan θ + gx²/(2u² cos² θ)",
            "y = ux − gt²/2",
        ],
        "answer": "y = x tan θ − gx²/(2u² cos² θ)",
        "explanation": (
            "Eliminating time from x = u cos θ · t and "
            "y = u sin θ · t − gt²/2 gives the trajectory equation."
        ),
    },
    {
        "id": "M08",
        "type": "MCQ",
        "difficulty": "JEE Challenge",
        "topic": "Velocity at a given height",
        "question": (
            "A projectile is launched at speed u. Ignoring air resistance, "
            "its speed at a point at height h above the launch point is:"
        ),
        "options": [
            "√(u² + 2gh)",
            "√(u² − 2gh)",
            "u − gh",
            "u² − gh",
        ],
        "answer": "√(u² − 2gh)",
        "explanation": (
            "Conservation of mechanical energy gives "
            "v²/2 + gh = u²/2, hence v = √(u² − 2gh)."
        ),
    },
    {
        "id": "M09",
        "type": "MCQ",
        "difficulty": "Intermediate",
        "topic": "Acceleration",
        "question": (
            "Neglecting air resistance, the horizontal acceleration "
            "of a projectile is:"
        ),
        "options": ["g", "g/2", "Zero", "Depends on its speed"],
        "answer": "Zero",
        "explanation": (
            "Gravity acts vertically. With no horizontal force, "
            "horizontal acceleration is zero."
        ),
    },
    {
        "id": "M10",
        "type": "MCQ",
        "difficulty": "JEE Challenge",
        "topic": "Horizontal projection",
        "question": (
            "A ball is projected horizontally from a height H. "
            "If its initial horizontal speed is doubled, the time taken "
            "to reach the ground will:"
        ),
        "options": [
            "Double",
            "Become half",
            "Remain unchanged",
            "Become four times",
        ],
        "answer": "Remain unchanged",
        "explanation": (
            "Vertical motion determines time: H = gt²/2. "
            "The initial horizontal speed does not affect it."
        ),
    },
    {
        "id": "N01",
        "type": "Numerical",
        "difficulty": "Basic",
        "topic": "Time of flight",
        "question": (
            "A projectile is launched at 20 m/s at 30° to the horizontal. "
            "Find its total time of flight in seconds. Take g = 10 m/s²."
        ),
        "answer": 2.0,
        "unit": "s",
        "tolerance": 0.05,
        "explanation": "T = 2u sin θ / g = 2 × 20 × 0.5 / 10 = 2 s.",
    },
    {
        "id": "N02",
        "type": "Numerical",
        "difficulty": "Basic",
        "topic": "Maximum height",
        "question": (
            "A projectile is launched at 20 m/s at 30° to the horizontal. "
            "Find its maximum height in metres. Take g = 10 m/s²."
        ),
        "answer": 5.0,
        "unit": "m",
        "tolerance": 0.05,
        "explanation": (
            "uᵧ = 20 sin 30° = 10 m/s. "
            "H = uᵧ²/(2g) = 100/20 = 5 m."
        ),
    },
    {
        "id": "N03",
        "type": "Numerical",
        "difficulty": "Intermediate",
        "topic": "Horizontal range",
        "question": (
            "A projectile is launched at 20 m/s at 45° to the horizontal "
            "on level ground. Find its range in metres. Take g = 10 m/s²."
        ),
        "answer": 40.0,
        "unit": "m",
        "tolerance": 0.1,
        "explanation": "R = u² sin 2θ/g = 400 × 1/10 = 40 m.",
    },
    {
        "id": "N04",
        "type": "Numerical",
        "difficulty": "Intermediate",
        "topic": "Horizontal projection",
        "question": (
            "A ball is projected horizontally at 15 m/s from a cliff "
            "of height 20 m. Find the horizontal distance travelled "
            "before it reaches the ground. Take g = 10 m/s²."
        ),
        "answer": 30.0,
        "unit": "m",
        "tolerance": 0.1,
        "explanation": (
            "20 = ½ × 10 × t², so t = 2 s. "
            "Horizontal distance = 15 × 2 = 30 m."
        ),
    },
    {
        "id": "N05",
        "type": "Numerical",
        "difficulty": "JEE Challenge",
        "topic": "Maximum height and time",
        "question": (
            "A projectile is launched at 25 m/s at an angle whose sine "
            "is 3/5. Find its maximum height in metres. Take g = 10 m/s²."
        ),
        "answer": 11.25,
        "unit": "m",
        "tolerance": 0.1,
        "explanation": (
            "Initial vertical speed = 25 × 3/5 = 15 m/s. "
            "H = uᵧ²/(2g) = 225/20 = 11.25 m."
        ),
    },
]


# ============================================================
# SESSION STATE
# ============================================================

if "mock_test" not in st.session_state:
    st.session_state.mock_test = None

if "discard_confirmation" not in st.session_state:
    st.session_state.discard_confirmation = False

if "discarded_message" not in st.session_state:
    st.session_state.discarded_message = False

if "score_saved" not in st.session_state:
    st.session_state.score_saved = False

if "score_not_saved" not in st.session_state:
    st.session_state.score_not_saved = False


# ============================================================
# TEST FUNCTIONS
# ============================================================

def start_test(duration_minutes):
    mcqs = [dict(q) for q in QUESTION_BANK if q["type"] == "MCQ"]
    numericals = [
        dict(q) for q in QUESTION_BANK if q["type"] == "Numerical"
    ]

    random.shuffle(mcqs)
    random.shuffle(numericals)

    started_at = time.time()

    st.session_state.mock_test = {
        "id": str(uuid.uuid4()),
        "questions": mcqs + numericals,
        "answers": {},
        "current_index": 0,
        "started_at": started_at,
        "deadline": started_at + duration_minutes * 60,
        "duration": duration_minutes,
        "submitted": False,
        "expired": False,
        "forced_submission": False,
        "submitted_reason": "manual",
        "results": None,
    }


def evaluate_test(test):
    score = 0
    attempted = 0
    correct_count = 0
    incorrect_count = 0
    unattempted_count = 0
    results = []

    for index, q in enumerate(test["questions"]):
        raw_answer = test["answers"].get(q["id"], "")

        if raw_answer is None:
            raw_answer = ""

        if isinstance(raw_answer, str):
            raw_answer = raw_answer.strip()

        if raw_answer == "":
            status = "Unattempted"
            marks = MARKS_UNATTEMPTED
            unattempted_count += 1
            normalized_answer = ""
        else:
            attempted += 1

            if q["type"] == "MCQ":
                is_correct = raw_answer == q["answer"]
                normalized_answer = raw_answer
            else:
                try:
                    numeric_answer = float(raw_answer)
                    is_correct = (
                        math.isfinite(numeric_answer)
                        and abs(numeric_answer - q["answer"])
                        <= q.get("tolerance", 0.05)
                    )
                    normalized_answer = numeric_answer
                except (ValueError, TypeError):
                    is_correct = False
                    normalized_answer = raw_answer

            if is_correct:
                status = "Correct"
                marks = MARKS_CORRECT
                correct_count += 1
            else:
                status = "Incorrect"
                marks = MARKS_INCORRECT
                incorrect_count += 1

        score += marks

        results.append({
            "number": index + 1,
            "id": q["id"],
            "type": q["type"],
            "difficulty": q["difficulty"],
            "topic": q["topic"],
            "question": q["question"],
            "status": status,
            "marks": marks,
            "your_answer": normalized_answer,
            "correct_answer": q["answer"],
            "unit": q.get("unit", ""),
            "explanation": q["explanation"],
        })

    test["results"] = {
        "score": score,
        "attempted": attempted,
        "correct": correct_count,
        "incorrect": incorrect_count,
        "unattempted": unattempted_count,
        "accuracy": (
            correct_count / attempted * 100 if attempted else 0
        ),
        "details": results,
    }

    test["submitted"] = True


def save_answer(question_id, widget_key):
    test = st.session_state.mock_test

    if test is None or test["submitted"]:
        return

    value = st.session_state.get(widget_key, "")

    if value is None or str(value).strip() == "":
        test["answers"].pop(question_id, None)
    else:
        test["answers"][question_id] = str(value).strip()


def go_to_question(index):
    test = st.session_state.mock_test

    if test is not None and not test["submitted"]:
        test["current_index"] = index


def submit_test():
    test = st.session_state.mock_test

    if test is None or test["submitted"]:
        return

    if time.time() >= test["deadline"]:
        test["expired"] = True
        test["submitted_reason"] = "time_expired"

    evaluate_test(test)


def confirm_discard():
    st.session_state.discard_confirmation = True


def cancel_discard():
    st.session_state.discard_confirmation = False


def discard_test():
    st.session_state.mock_test = None
    st.session_state.discard_confirmation = False
    st.session_state.discarded_message = True
    st.session_state.score_saved = False
    st.session_state.score_not_saved = False


def save_test_score():
    test = st.session_state.mock_test

    if not test or not test.get("submitted") or not test.get("results"):
        return

    try:
        SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)

        if SCORE_FILE.exists():
            with SCORE_FILE.open("r", encoding="utf-8") as file:
                saved_scores = json.load(file)
        else:
            saved_scores = []

        if not isinstance(saved_scores, list):
            saved_scores = []

        saved_scores.append({
            "test_id": test["id"],
            "test_name": "Projectile Motion Mock Test",
            "score": test["results"]["score"],
            "maximum_marks": MAX_MARKS,
            "correct": test["results"]["correct"],
            "incorrect": test["results"]["incorrect"],
            "unattempted": test["results"]["unattempted"],
            "accuracy": round(test["results"]["accuracy"], 2),
            "duration_minutes": test["duration"],
            "expired": test.get("expired", False),
            "submitted_reason": test.get("submitted_reason", "manual"),
        })

        with SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump(saved_scores, file, indent=2)

        st.session_state.score_saved = True
        st.session_state.score_not_saved = False
        st.session_state.pop("score_save_error", None)

    except (OSError, json.JSONDecodeError) as error:
        st.session_state.score_save_error = str(error)


# ============================================================
# TEST INTRODUCTION AND NAVIGATION GUARD
# ============================================================

test = st.session_state.mock_test

if test and test.get("forced_submission") and not test["submitted"]:
    test["forced_submission"] = False
    test["submitted_reason"] = "page_switch"
    evaluate_test(test)
    st.rerun()


if test is None:
    st.markdown("### 📋 Before You Begin")

    st.info(
        """
        **JEE Main-style Projectile Motion Test**

        - **Total questions:** 15 (10 MCQs + 5 numericals)
        - **Question order:** All MCQs first, then numericals
        - **Duration:** Choose 40 or 45 minutes
        - **Maximum marks:** 60
        - **Correct answer:** +4 marks
        - **Incorrect answer:** −1 mark
        - **Unattempted answer:** 0 marks
        - **Calculator:** Not allowed

        **Important rules**

        1. Switching to Simulator, Practice, or another app page while
           attempting the test will automatically submit your answers.
        2. Switching browser tabs is not allowed.
        3. Use **Discard Test & Exit** if you want to abandon an attempt.
           A discarded test will not save its score.
        4. Once submitted, a test cannot be resumed.
        5. After submission, choose whether to save your score or not
        .
        """
    )

    duration = st.radio(
        "Choose your test duration",
        options=[40, 45],
        index=1,
        horizontal=True,
        format_func=lambda x: f"{x} minutes",
    )

    if st.button(
        "🚀 Start Test",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.score_saved = False
        st.session_state.score_not_saved = False
        st.session_state.discard_confirmation = False
        st.session_state.pop("score_save_error", None)
        start_test(duration)
        st.rerun()

    if st.session_state.discarded_message:
        st.info("Your previous attempt was discarded. No score was saved.")

    st.stop()


# ============================================================
# LIVE COUNTDOWN TIMER
# ============================================================

@st.fragment(run_every="1s")
def show_timer():
    current_test = st.session_state.mock_test

    if current_test is None or current_test["submitted"]:
        return

    remaining = max(
        0,
        int(current_test["deadline"] - time.time()),
    )

    minutes, seconds = divmod(remaining, 60)

    if remaining <= 5 * 60:
        st.error(f"⏳ Time remaining: {minutes:02d}:{seconds:02d}")
    else:
        st.info(f"⏱️ Time remaining: {minutes:02d}:{seconds:02d}")

    if remaining <= 0:
        current_test["expired"] = True
        current_test["submitted_reason"] = "time_expired"
        evaluate_test(current_test)
        st.rerun()


# ============================================================
# ACTIVE TEST
# ============================================================

if not test["submitted"]:
    with st.expander("🚪 Leave Test / Discard Test"):
        st.warning(
            "Discarding permanently abandons this attempt. "
            "Your score will not be saved."
        )

        st.button(
            "Discard Test & Exit",
            key=f"discard_{test['id']}",
            on_click=confirm_discard,
            use_container_width=True,
        )

    if st.session_state.discard_confirmation:
        st.error("Are you sure you want to discard this test?")

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            st.button(
                "Yes, discard test",
                key=f"confirm_discard_{test['id']}",
                type="primary",
                on_click=discard_test,
                use_container_width=True,
            )

        with cancel_col:
            st.button(
                "Keep attempting",
                key=f"cancel_discard_{test['id']}",
                on_click=cancel_discard,
                use_container_width=True,
            )

        st.stop()

    questions = test["questions"]
    total_questions = len(questions)
    current_index = test["current_index"]
    q = questions[current_index]

    header_left, header_right = st.columns([3, 2])

    with header_left:
        st.subheader("📝 Projectile Motion Mock Test")
        st.caption(f"Question {current_index + 1} of {total_questions}")

    with header_right:
        show_timer()

    st.markdown("#### Question Palette")
    palette_columns = st.columns(15)

    for i, palette_q in enumerate(questions):
        answered = palette_q["id"] in test["answers"]
        is_current = i == current_index

        if is_current:
            label = f"🔵 {i + 1}"
        elif answered:
            label = f"🟢 {i + 1}"
        else:
            label = f"⚪ {i + 1}"

        with palette_columns[i]:
            st.button(
                label,
                key=f"palette_{test['id']}_{i}",
                use_container_width=True,
                on_click=go_to_question,
                args=(i,),
                help=f"Go to Question {i + 1}",
            )

    answered_count = sum(
        1 for item in questions if item["id"] in test["answers"]
    )
    unanswered_count = total_questions - answered_count

    st.progress(answered_count / total_questions)

    st.caption(
        f"🟢 Answered: {answered_count}  ·  "
        f"⚪ Unanswered: {unanswered_count}"
    )

    st.divider()

    question_col, marks_col = st.columns([4, 1])

    with question_col:
        section = (
            "Multiple Choice Question"
            if q["type"] == "MCQ"
            else "Numerical Answer Question"
        )
        st.markdown(f"### Q{current_index + 1}. {section}")

    with marks_col:
        st.metric("Correct", "+4")
        st.metric("Incorrect", "−1")

    st.caption(
        f"Difficulty: {q['difficulty']}  ·  "
        f"Topic: {q['topic']}  ·  Type: {q['type']}"
    )

    with st.container(border=True):
        st.markdown("#### Question")
        st.write(q["question"])

        widget_key = f"answer_{test['id']}_{q['id']}"

        if widget_key not in st.session_state:
            saved_answer = test["answers"].get(q["id"], "")

            if q["type"] == "MCQ":
                st.session_state[widget_key] = (
                    saved_answer if saved_answer else None
                )
            else:
                st.session_state[widget_key] = str(saved_answer)

        if q["type"] == "MCQ":
            st.radio(
                "Choose one option:",
                options=q["options"],
                key=widget_key,
                on_change=save_answer,
                args=(q["id"], widget_key),
            )
        else:
            st.text_input(
                f"Enter your answer in {q['unit']}:",
                key=widget_key,
                placeholder="Type your numerical answer",
                on_change=save_answer,
                args=(q["id"], widget_key),
            )

    st.divider()

    previous_col, status_col, next_col = st.columns([1, 2, 1])

    with previous_col:
        if current_index > 0:
            st.button(
                "⬅️ Previous",
                key=f"prev_{test['id']}_{current_index}",
                use_container_width=True,
                on_click=go_to_question,
                args=(current_index - 1,),
            )

    with status_col:
        if q["id"] in test["answers"]:
            st.success("Answer saved")
        else:
            st.info("Not answered yet")

    with next_col:
        if current_index < total_questions - 1:
            st.button(
                "Next ➡️",
                key=f"next_{test['id']}_{current_index}",
                use_container_width=True,
                on_click=go_to_question,
                args=(current_index + 1,),
            )

    st.divider()

    with st.expander("📋 Review before submitting"):
        st.write(f"Answered: **{answered_count}/{total_questions}**")
        st.write(f"Unanswered: **{unanswered_count}**")

        if unanswered_count:
            st.warning("Unanswered questions will receive zero marks.")
        else:
            st.success("All questions have been answered.")

    st.button(
        "🏁 Submit Test & View Results",
        type="primary",
        use_container_width=True,
        key=f"submit_{test['id']}",
        on_click=submit_test,
    )

    st.stop()


# ============================================================
# RESULTS REPORT
# ============================================================

results = test["results"]

st.divider()
st.title("📊 Your Performance Report")

if test["expired"]:
    st.warning("Time is up. Your test was automatically submitted.")
elif test.get("submitted_reason") == "page_switch":
    st.warning(
        "You navigated away from the test page. "
        "Your test was automatically submitted."
    )
else:
    st.success("Test submitted successfully!")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Final Score", f"{results['score']} / {MAX_MARKS}")
c2.metric("Correct", results["correct"])
c3.metric("Incorrect", results["incorrect"])
c4.metric("Unattempted", results["unattempted"])

st.progress(max(0, min(1, results["score"] / MAX_MARKS)))

r1, r2, r3 = st.columns(3)
r1.metric("Attempted", results["attempted"])
r2.metric("Accuracy", f"{results['accuracy']:.1f}%")
r3.metric("Negative Marks", results["incorrect"])

st.caption(
    "Accuracy = correct answers ÷ attempted questions. "
    "Final score includes negative marking."
)


# ============================================================
# OPTIONAL SCORE SAVING
# ============================================================

st.subheader("💾 Save Your Score")
st.write(
    "Your report is available now. Saving the score is optional."
)

if st.session_state.score_saved:
    st.success("Your score has been saved.")
elif st.session_state.score_not_saved:
    st.info("Your score was not saved.")
else:
    save_col, skip_col = st.columns(2)

    with save_col:
        st.button(
            "Save Score",
            key=f"save_score_{test['id']}",
            on_click=save_test_score,
            use_container_width=True,
        )

    with skip_col:
        if st.button(
            "Don't Save Score",
            key=f"skip_score_{test['id']}",
            use_container_width=True,
        ):
            st.session_state.score_not_saved = True

if st.session_state.get("score_save_error"):
    st.error(
        "Unable to save score: "
        + st.session_state["score_save_error"]
    )


# ============================================================
# DIFFICULTY ANALYSIS
# ============================================================

st.subheader("🎯 Difficulty Analysis")

for difficulty in ["Basic", "Intermediate", "JEE Challenge"]:
    group = [
        item for item in results["details"]
        if item["difficulty"] == difficulty
    ]

    if not group:
        continue

    correct = sum(item["status"] == "Correct" for item in group)
    incorrect = sum(item["status"] == "Incorrect" for item in group)
    unattempted = sum(
        item["status"] == "Unattempted" for item in group
    )
    difficulty_score = sum(item["marks"] for item in group)

    with st.container(border=True):
        st.markdown(f"**{difficulty}**")
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Questions", len(group))
        d2.metric("Correct", correct)
        d3.metric("Incorrect", incorrect)
        d4.metric("Marks", difficulty_score)
        st.caption(f"Unattempted: {unattempted}")


# ============================================================
# MISTAKE ANALYSIS
# ============================================================

st.subheader("🔍 Mistake Analysis")

mistakes = [
    item for item in results["details"]
    if item["status"] == "Incorrect"
]

unattempted_items = [
    item for item in results["details"]
    if item["status"] == "Unattempted"
]

if mistakes:
    st.markdown("#### Incorrect answers")

    for item in mistakes:
        with st.expander(
            f"Q{item['number']} · {item['difficulty']} · "
            f"{item['topic']} · {item['marks']} mark"
        ):
            st.write(item["question"])
            st.write(f"**Your answer:** {item['your_answer']}")
            st.write(f"**Correct answer:** {item['correct_answer']}")
            st.write(f"**Question type:** {item['type']}")
            st.write(f"**Difficulty:** {item['difficulty']}")
            st.write(f"**Topic:** {item['topic']}")
            st.write(f"**Marks awarded:** {item['marks']}")
            st.markdown("**Explanation**")
            st.write(item["explanation"])

else:
    st.success("No incorrect answers. Excellent work!")

if unattempted_items:
    st.markdown("#### Unattempted questions")

    for item in unattempted_items:
        with st.expander(
            f"Q{item['number']} · {item['difficulty']} · {item['topic']}"
        ):
            st.write(item["question"])
            st.write(f"**Correct answer:** {item['correct_answer']}")
            st.write(f"**Difficulty:** {item['difficulty']}")
            st.write(item["explanation"])


# ============================================================
# TOPIC-WISE PERFORMANCE
# ============================================================

st.subheader("📚 Topic-wise Performance")

topics = sorted(set(item["topic"] for item in results["details"]))

for topic in topics:
    group = [
        item for item in results["details"]
        if item["topic"] == topic
    ]

    correct = sum(item["status"] == "Correct" for item in group)
    attempted = sum(
        item["status"] != "Unattempted" for item in group
    )
    accuracy = 100 * correct / attempted if attempted else 0

    st.write(
        f"**{topic}:** {correct}/{len(group)} correct · "
        f"{accuracy:.0f}% attempted accuracy"
    )


# ============================================================
# COMPLETE ANSWER KEY
# ============================================================

st.subheader("📝 Complete Answer Key")

for item in results["details"]:
    with st.expander(
        f"Q{item['number']} · {item['status']} · "
        f"{item['difficulty']}"
    ):
        st.write(item["question"])
        st.write(f"**Correct answer:** {item['correct_answer']}")
        st.write(
            f"**Your answer:** {item['your_answer'] or 'Not attempted'}"
        )
        st.write(f"**Marks:** {item['marks']:+d}")
        st.write(f"**Topic:** {item['topic']}")
        st.write(item["explanation"])


# ============================================================
# RETAKE
# ============================================================

st.divider()
st.markdown("### Ready for another attempt?")

st.write(
    "Retaking creates a fresh test with shuffled question order "
    "within the MCQ and numerical sections. Your current report "
    "will be replaced."
)

if st.button(
    "🔄 Retake Projectile Motion Test",
    type="primary",
):
    st.session_state.mock_test = None
    st.session_state.discard_confirmation = False
    st.session_state.score_saved = False
    st.session_state.score_not_saved = False
    st.session_state.pop("score_save_error", None)
    st.rerun()
