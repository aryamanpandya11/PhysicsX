"""
PhysicsX Lab - Authentic JEE CBT Mock Test Arena
Features:
- Multiple test modes: Full-Length JEE Main (25 Q), Mechanics Special (15 Q),
  Electrodynamics Special (15 Q), Optics & Modern Physics (15 Q), Quick Sprint (10 Q).
- Standard NTA CBT question palette (Answered, Not Answered, Marked for Review).
- Real-time countdown timer with timeout auto-submission.
- Standard JEE marking scheme: +4 for correct, -1 for incorrect, 0 for unattempted.
- Deep performance analytics: score, estimated percentile, difficulty analysis,
  topic breakdown, mistake review, and downloadable report.
"""

import json
import math
from pathlib import Path
import random
import time
import uuid
import streamlit as st

from question_bank import CONCEPTUAL_MCQS, make_electrostatics_numerical, make_kinematics_numerical, make_modern_numerical, make_nlm_numerical, make_wep_numerical
from ui_theme import apply_custom_theme, render_header

st.set_page_config(
    page_title="PhysicsX Lab — JEE CBT Mock Test",
    page_icon="📝",
    layout="wide",
)

apply_custom_theme()

SCORE_FILE = Path(__file__).resolve().parent.parent / "practice_data" / "test_scores.json"

TEST_PRESETS = {
    "Full-Length JEE Main Physics Test": {
        "mcq_count": 20,
        "num_count": 5,
        "duration": 60,
        "max_marks": 100,
        "description": "20 MCQs + 5 Numerical Value questions covering the entire Class 11 & 12 JEE syllabus.",
    },
    "Mechanics Mastery Mock": {
        "mcq_count": 10,
        "num_count": 5,
        "duration": 40,
        "max_marks": 60,
        "description": "Kinematics, Newton's Laws, Friction, Work-Energy, and Rotational Dynamics.",
    },
    "Electrodynamics & Magnetism Mock": {
        "mcq_count": 10,
        "num_count": 5,
        "duration": 40,
        "max_marks": 60,
        "description": "Electrostatics, Capacitors, Current Electricity, Magnetism & Lorentz Force.",
    },
    "Optics, Waves & Modern Physics Mock": {
        "mcq_count": 10,
        "num_count": 5,
        "duration": 40,
        "max_marks": 60,
        "description": "Ray Optics, Wave Optics (YDSE), SHM, Sound Waves, and Photoelectric Effect.",
    },
    "Quick Sprint Physics Mock": {
        "mcq_count": 8,
        "num_count": 2,
        "duration": 20,
        "max_marks": 40,
        "description": "A high-intensity 20-minute rapid drill to test test-taking speed and accuracy.",
    },
}


def build_test_questions(preset_name):
    cfg = TEST_PRESETS[preset_name]
    mcqs = []
    nums = []

    # Filter MCQs based on category
    if "Mechanics" in preset_name:
        cand_mcqs = [q for q in CONCEPTUAL_MCQS if any(k in q["chapter"] for k in ["Kinematics", "Newton", "Work", "Rotation", "Gravitation"])]
    elif "Electro" in preset_name:
        cand_mcqs = [q for q in CONCEPTUAL_MCQS if any(k in q["chapter"] for k in ["Electrostatics", "Current"])]
    elif "Optics" in preset_name:
        cand_mcqs = [q for q in CONCEPTUAL_MCQS if any(k in q["chapter"] for k in ["Optics", "SHM", "Modern"])]
    else:
        cand_mcqs = list(CONCEPTUAL_MCQS)

    if not cand_mcqs:
        cand_mcqs = list(CONCEPTUAL_MCQS)

    # Pick MCQs
    random.shuffle(cand_mcqs)
    for i in range(cfg["mcq_count"]):
        src = cand_mcqs[i % len(cand_mcqs)].copy()
        src["id"] = f"MCQ_{i+1}_{uuid.uuid4().hex[:6]}"
        src["type"] = "MCQ"
        src["unit"] = ""
        mcqs.append(src)

    # Generate Numericals
    num_gens = [make_kinematics_numerical, make_nlm_numerical, make_wep_numerical, make_electrostatics_numerical, make_modern_numerical]
    for j in range(cfg["num_count"]):
        gen = num_gens[j % len(num_gens)]
        diff = random.choice(["Basic", "Intermediate", "JEE Challenge"])
        q_obj = gen(diff)
        q_obj["id"] = f"NUM_{j+1}_{uuid.uuid4().hex[:6]}"
        nums.append(q_obj)

    return mcqs + nums


# ============================================================
# STATE INITIALIZATION
# ============================================================
if "mock_test" not in st.session_state:
    st.session_state.mock_test = None

if "score_saved" not in st.session_state:
    st.session_state.score_saved = False


def start_test(preset_name, duration_min):
    q_list = build_test_questions(preset_name)
    now = time.time()
    st.session_state.mock_test = {
        "id": str(uuid.uuid4()),
        "name": preset_name,
        "questions": q_list,
        "answers": {},
        "marked_for_review": set(),
        "visited": {0},
        "current_index": 0,
        "started_at": now,
        "deadline": now + duration_min * 60,
        "duration": duration_min,
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
    results_detail = []

    for idx, q in enumerate(test["questions"]):
        user_val = test["answers"].get(q["id"])
        is_attempted = user_val is not None and str(user_val).strip() != ""

        if not is_attempted:
            status = "Unattempted"
            marks = 0
            unattempted_count += 1
            norm_val = "Not Attempted"
        else:
            attempted += 1
            if q["type"] == "MCQ":
                is_correct = str(user_val).strip() == str(q["answer"]).strip()
                norm_val = str(user_val)
            else:
                try:
                    num_val = float(str(user_val).strip())
                    norm_val = f"{num_val} {q.get('unit', '')}"
                    tol = q.get("tolerance", 0.08)
                    is_correct = math.isfinite(num_val) and abs(num_val - q["answer"]) <= max(tol, abs(q["answer"]) * 0.02)
                except ValueError:
                    is_correct = False
                    norm_val = str(user_val)

            if is_correct:
                status = "Correct"
                marks = 4
                correct_count += 1
            else:
                status = "Incorrect"
                marks = -1
                incorrect_count += 1

        score += marks
        results_detail.append({
            "number": idx + 1,
            "id": q["id"],
            "type": q["type"],
            "chapter": q.get("chapter", "Physics"),
            "difficulty": q.get("difficulty", "Standard"),
            "prompt": q["prompt"],
            "status": status,
            "marks": marks,
            "user_answer": norm_val,
            "target_answer": f"{q['answer']} {q.get('unit', '')}",
            "explanation": q.get("explanation") or q.get("working", "See formula."),
        })

    max_marks = len(test["questions"]) * 4
    accuracy = (correct_count / attempted * 100) if attempted else 0
    est_percentile = min(99.9, max(10.0, 50.0 + (score / max_marks) * 50.0))

    test["results"] = {
        "score": score,
        "max_marks": max_marks,
        "attempted": attempted,
        "correct": correct_count,
        "incorrect": incorrect_count,
        "unattempted": unattempted_count,
        "accuracy": accuracy,
        "estimated_percentile": est_percentile,
        "details": results_detail,
    }
    test["submitted"] = True


# ============================================================
# LIVE TIMER FRAGMENT
# ============================================================
@st.fragment(run_every="1s")
def render_live_timer():
    t_obj = st.session_state.mock_test
    if t_obj is None or t_obj.get("submitted"):
        return

    rem = max(0, int(t_obj["deadline"] - time.time()))
    mins, secs = divmod(rem, 60)

    if rem <= 300:  # <= 5 min
        st.markdown(
            f"""
            <div style="background: rgba(244, 63, 94, 0.2); border: 1px solid #f43f5e; padding: 8px 16px; border-radius: 8px; color: #f43f5e; font-weight: 700; text-align: center;">
                ⏳ TIME CRITICAL: {mins:02d}:{secs:02d}
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="background: rgba(0, 240, 255, 0.1); border: 1px solid rgba(0, 240, 255, 0.3); padding: 8px 16px; border-radius: 8px; color: #00f0ff; font-weight: 600; text-align: center;">
                ⏱️ TIME REMAINING: {mins:02d}:{secs:02d}
            </div>
            """,
            unsafe_allow_html=True,
        )

    if rem <= 0:
        t_obj["expired"] = True
        t_obj["submitted_reason"] = "time_expired"
        evaluate_test(t_obj)
        st.rerun()


# ============================================================
# TEST SELECTION & START SCREEN
# ============================================================
test = st.session_state.mock_test

if test and test.get("forced_submission") and not test["submitted"]:
    test["forced_submission"] = False
    test["submitted_reason"] = "page_switch"
    evaluate_test(test)
    st.rerun()

if test is None:
    render_header(
        title="JEE Computer-Based Test (CBT) Arena",
        subtitle="Experience real exam pressure under timed conditions with standard NTA marking (+4, -1, 0), interactive question palette, and granular performance analytics.",
        icon="📝",
        badge="NTA CBT Exam Simulator",
    )

    st.markdown("### 📋 Choose Your Mock Test")
    t_col1, t_col2 = st.columns([2, 1])

    with t_col1:
        sel_preset = st.radio(
            "Select Test Paper",
            options=list(TEST_PRESETS.keys()),
            format_func=lambda x: f"{x} ({TEST_PRESETS[x]['duration']} mins · {TEST_PRESETS[x]['max_marks']} Marks)",
        )
        st.info(TEST_PRESETS[sel_preset]["description"])

    with t_col2:
        with st.container(border=True):
            st.markdown("#### ⚖️ Marking Scheme")
            st.markdown("- **Correct:** :green[**+4 Marks**]")
            st.markdown("- **Incorrect:** :red[**-1 Mark**]")
            st.markdown("- **Unattempted:** **0 Marks**")
            st.markdown("- **Calculator:** **Strictly Prohibited**")

    if st.button("🚀 Start Test Now", type="primary", use_container_width=True):
        st.session_state.score_saved = False
        start_test(sel_preset, TEST_PRESETS[sel_preset]["duration"])
        st.rerun()

    st.stop()


# ============================================================
# ACTIVE TEST RUNNING INTERFACE
# ============================================================
elif not test["submitted"]:
    q_list = test["questions"]
    curr_idx = test["current_index"]
    test["visited"].add(curr_idx)
    curr_q = q_list[curr_idx]

    # Top Control Bar
    top_c1, top_c2, top_c3 = st.columns([3, 2, 2])
    with top_c1:
        st.markdown(f"#### 📝 {test['name']}")
        st.caption(f"Question {curr_idx + 1} of {len(q_list)} · Category: **{curr_q.get('chapter', 'Physics')}**")
    with top_c2:
        render_live_timer()
    with top_c3:
        if st.button("🚪 Discard Test", use_container_width=True):
            st.session_state.mock_test = None
            st.rerun()

    # Question Palette
    st.markdown("##### Question Palette")
    cols_per_row = 15 if len(q_list) <= 15 else 13
    palette_cols = st.columns(cols_per_row)

    for i, p_q in enumerate(q_list):
        has_ans = p_q["id"] in test["answers"]
        is_marked = p_q["id"] in test["marked_for_review"]
        is_curr = i == curr_idx

        # NTA standard colors
        if is_curr:
            label = f"🔵 {i+1}"
        elif is_marked and has_ans:
            label = f"🟣🟢 {i+1}"
        elif is_marked:
            label = f"🟣 {i+1}"
        elif has_ans:
            label = f"🟢 {i+1}"
        elif i in test["visited"]:
            label = f"🔴 {i+1}"
        else:
            label = f"⚪ {i+1}"

        with palette_cols[i % cols_per_row]:
            if st.button(label, key=f"pal_{test['id']}_{i}", use_container_width=True):
                test["current_index"] = i
                st.rerun()

    st.markdown(
        """
        <div style="font-size: 0.8rem; color: #94a3b8; margin: 8px 0 16px 0; display: flex; gap: 16px; flex-wrap: wrap;">
            <span>🟢 Answered</span>
            <span>🔴 Not Answered</span>
            <span>⚪ Not Visited</span>
            <span>🟣 Marked for Review</span>
            <span>🔵 Current</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Question Box
    with st.container(border=True):
        st.markdown(f"### Q{curr_idx + 1}. {curr_q['type']} Question")
        st.caption(f"Difficulty: {curr_q.get('difficulty', 'Standard')} · Topic: {curr_q.get('chapter', 'Physics')}")
        st.markdown(curr_q["prompt"])

        widget_key = f"cbt_ans_{test['id']}_{curr_q['id']}"

        if curr_q["type"] == "MCQ":
            cur_saved = test["answers"].get(curr_q["id"])
            opts = curr_q["options"]
            def_idx = opts.index(cur_saved) if cur_saved in opts else None

            choice = st.radio("Choose Option:", options=opts, index=def_idx, key=widget_key)
            if choice is not None:
                test["answers"][curr_q["id"]] = choice
        else:
            cur_saved = test["answers"].get(curr_q["id"], "")
            val_in = st.text_input(f"Enter Numerical Answer in {curr_q.get('unit', '')}:", value=str(cur_saved) if cur_saved else "", key=widget_key, placeholder="Type number...").strip()
            if val_in:
                test["answers"][curr_q["id"]] = val_in

    # Navigation Buttons Bar
    nav1, nav2, nav3, nav4 = st.columns(4)

    with nav1:
        if st.button("💾 Save & Next ➡️", type="primary", use_container_width=True):
            if curr_q["id"] in test["marked_for_review"]:
                test["marked_for_review"].remove(curr_q["id"])
            if curr_idx < len(q_list) - 1:
                test["current_index"] += 1
            st.rerun()

    with nav2:
        if st.button("🟣 Mark for Review & Next", use_container_width=True):
            test["marked_for_review"].add(curr_q["id"])
            if curr_idx < len(q_list) - 1:
                test["current_index"] += 1
            st.rerun()

    with nav3:
        if st.button("🧹 Clear Response", use_container_width=True):
            test["answers"].pop(curr_q["id"], None)
            test["marked_for_review"].discard(curr_q["id"])
            st.rerun()

    with nav4:
        if curr_idx > 0:
            if st.button("⬅️ Previous Question", use_container_width=True):
                test["current_index"] -= 1
                st.rerun()

    st.divider()

    # Submission footer
    sub_col1, sub_col2 = st.columns([3, 1])
    with sub_col1:
        ans_count = len([k for k, v in test["answers"].items() if str(v).strip()])
        st.write(f"Answered: **{ans_count} / {len(q_list)}** questions")
    with sub_col2:
        if st.button("🏁 Submit Test", type="primary", use_container_width=True):
            evaluate_test(test)
            st.rerun()

    st.stop()


# ============================================================
# RESULTS & PERFORMANCE REPORT SCREEN
# ============================================================
elif test is not None:
    res = test["results"]

    render_header(
        title="Comprehensive Performance Scorecard",
        subtitle=f"Official Evaluation Report for {test['name']}",
        icon="📊",
        badge="Scorecard & Analysis",
    )

    if test.get("expired"):
        st.warning("⏱️ Time expired! The test was automatically evaluated.")
    elif test.get("submitted_reason") == "page_switch":
        st.warning("⚠️ You switched tabs or pages during an active test. Your answers have been submitted.")
    else:
        st.success("🎉 Test submitted successfully!")

    # Score Metrics Cards
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Final Score", f"{res['score']} / {res['max_marks']}")
    sc2.metric("Estimated Percentile", f"{res['estimated_percentile']:.1f}%ile")
    sc3.metric("Correct Answers", f"{res['correct']} (+{res['correct']*4})")
    sc4.metric("Negative Marks", f"-{res['incorrect']}")

    sc5, sc6, sc7, sc8 = st.columns(4)
    sc5.metric("Attempted", f"{res['attempted']} / {len(test['questions'])}")
    sc6.metric("Unattempted", f"{res['unattempted']}")
    sc7.metric("Accuracy", f"{res['accuracy']:.1f}%")
    mins_taken = int((time.time() - test["started_at"]) / 60)
    sc8.metric("Time Taken", f"{min(mins_taken, test['duration'])} mins")

    st.divider()

    # Save score option
    st.markdown("#### 💾 Save Score Report")
    if st.session_state.score_saved:
        st.success("✅ Score recorded in your test history.")
    else:
        if st.button("Save Score to Local History 💾", type="primary"):
            try:
                SCORE_FILE.parent.mkdir(parents=True, exist_ok=True)
                saved = []
                if SCORE_FILE.exists():
                    with SCORE_FILE.open("r", encoding="utf-8") as f:
                        saved = json.load(f)
                        if not isinstance(saved, list):
                            saved = []
                saved.append({
                    "test_name": test["name"],
                    "score": res["score"],
                    "max_marks": res["max_marks"],
                    "accuracy": round(res["accuracy"], 1),
                    "date": time.strftime("%d %b %Y, %I:%M %p"),
                })
                with SCORE_FILE.open("w", encoding="utf-8") as f:
                    json.dump(saved, f, indent=2)
                st.session_state.score_saved = True
                st.rerun()
            except OSError as e:
                st.error(f"Could not save score: {e}")

    st.divider()

    # Granular Question Breakdown
    st.markdown("### 📝 Question-by-Question Detailed Review")
    for item in res["details"]:
        with st.expander(f"Q{item['number']} · {item['chapter']} · {item['status']} ({item['marks']:+d} Marks)"):
            st.markdown(item["prompt"])
            st.write(f"**Your Answer:** `{item['user_answer']}`")
            st.write(f"**Correct Target:** `{item['target_answer']}`")
            st.markdown("**Explanation & Derivation:**")
            st.markdown(item["explanation"])

    # Retake button
    st.divider()
    if st.button("🔄 Retake Another Test", type="primary", use_container_width=True):
        st.session_state.mock_test = None
        st.rerun()
