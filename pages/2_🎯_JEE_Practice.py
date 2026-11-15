"""
PhysicsX Lab - Comprehensive JEE Practice Suite
Includes chapter-wise practice across 10 JEE domains,
3-tier scaffolded hints, numerical tolerance checking,
step-by-step LaTeX worked solutions, and session tracking.
"""

import json
import math
from pathlib import Path
import streamlit as st

from question_bank import CHAPTERS, DIFFICULTIES, get_practice_question
from ui_theme import apply_custom_theme, render_header

# Active mock-test anti-cheat safeguard
test = st.session_state.get("mock_test")
if test and not test.get("submitted", False):
    test["forced_submission"] = True
    st.switch_page("pages/3_📝_JEE_Test.py")
    st.stop()

st.set_page_config(
    page_title="PhysicsX Lab — JEE Practice Suite",
    page_icon="🎯",
    layout="wide",
)

apply_custom_theme()

render_header(
    title="JEE Physics Practice Suite",
    subtitle="Master chapter-wise concepts through numerical and conceptual problems. Unlock 3-level progressive hints, examine detailed worked solutions, and track your accuracy.",
    icon="🎯",
    badge="Chapter-Wise Practice & Analytics",
)

# Persistent Session Directory
DATA_DIR = Path(__file__).resolve().parent.parent / "practice_data"
DATA_FILE = DATA_DIR / "saved_sessions.json"


def load_sessions():
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        pass
    return {}


def save_sessions(sessions):
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with DATA_FILE.open("w", encoding="utf-8") as f:
            json.dump(sessions, f, indent=2, ensure_ascii=False)
        return True
    except OSError:
        st.error("Could not write practice session to disk. Check directory permissions.")
        return False


if "practice_sessions" not in st.session_state:
    st.session_state.practice_sessions = load_sessions()

if "active_session_id" not in st.session_state:
    st.session_state.active_session_id = None


def active_session():
    s_id = st.session_state.active_session_id
    return st.session_state.practice_sessions.get(s_id) if s_id else None


def save_active_session():
    save_sessions(st.session_state.practice_sessions)


def create_session(name, chapter, difficulty, question_type):
    import uuid
    import datetime

    session_id = str(uuid.uuid4())
    first_q = get_practice_question(chapter=chapter, difficulty=difficulty, q_type=question_type)

    session = {
        "id": session_id,
        "name": name.strip() or f"{chapter} Practice",
        "chapter": chapter,
        "difficulty": difficulty,
        "question_type": question_type,
        "questions": [first_q],
        "created_at": datetime.datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }
    st.session_state.practice_sessions[session_id] = session
    st.session_state.active_session_id = session_id
    save_active_session()


def add_question(session):
    new_q = get_practice_question(
        chapter=session.get("chapter", "All Chapters (Mixed)"),
        difficulty=session.get("difficulty", "Basic"),
        q_type=session.get("question_type", "Mixed"),
    )
    session["questions"].append(new_q)
    save_active_session()


def get_stats(session):
    q_list = session["questions"]
    attempted = [q for q in q_list if q.get("checked")]
    correct = sum(1 for q in attempted if q.get("correct"))
    return {
        "total": len(q_list),
        "attempted": len(attempted),
        "correct": correct,
        "accuracy": (100 * correct / len(attempted)) if attempted else 0,
    }


# ============================================================
# SIDEBAR: SESSIONS & CHAPTER SELECTOR
# ============================================================
with st.sidebar:
    st.markdown("### 📚 Practice Sessions")

    session_names = {
        s_id: f"{s['name']} ({len(s.get('questions', []))} Q)"
        for s_id, s in st.session_state.practice_sessions.items()
    }

    if session_names:
        ids = list(session_names.keys())
        curr_id = st.session_state.active_session_id
        if curr_id not in ids:
            curr_id = ids[0]

        sel_id = st.selectbox(
            "Select Practice Session",
            options=ids,
            index=ids.index(curr_id),
            format_func=lambda x: session_names[x],
            key="practice_session_selector",
        )

        if sel_id != st.session_state.active_session_id:
            st.session_state.active_session_id = sel_id
            st.rerun()

        st.divider()

        if st.button("➕ Create New Session", use_container_width=True, type="primary"):
            st.session_state.show_new_session_form = True
            st.rerun()

        if st.button("🗑️ Delete Current Session", use_container_width=True):
            if sel_id in st.session_state.practice_sessions:
                del st.session_state.practice_sessions[sel_id]
                rem = list(st.session_state.practice_sessions.keys())
                st.session_state.active_session_id = rem[0] if rem else None
                save_sessions(st.session_state.practice_sessions)
                st.rerun()
    else:
        st.info("No saved sessions yet. Create one below to begin!")
        if st.button("➕ Create Your First Session", use_container_width=True, type="primary"):
            st.session_state.show_new_session_form = True

    st.divider()
    st.caption("Sessions are automatically saved locally and persist between runs.")


# ============================================================
# NEW SESSION MODAL / FORM
# ============================================================
if "show_new_session_form" not in st.session_state:
    st.session_state.show_new_session_form = not bool(st.session_state.practice_sessions)

if st.session_state.show_new_session_form:
    with st.container(border=True):
        st.markdown("### 🛠️ Configure New Practice Session")
        with st.form("new_session_creator_form"):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                sess_name = st.text_input("Session Title", value="Mechanics Mastery", placeholder="e.g., Kinematics Deep Dive")
                sess_chapter = st.selectbox("Physics Chapter", options=CHAPTERS, index=0)
            with f_col2:
                sess_diff = st.selectbox("Difficulty Level", options=list(DIFFICULTIES.keys()), index=1)
                sess_type = st.selectbox("Question Format", options=["Mixed (MCQ + Numerical)", "Numerical Only", "MCQ Only"], index=0)

            st.caption(f"ℹ️ {DIFFICULTIES[sess_diff]}")
            create_btn = st.form_submit_button("Start Practicing 🚀", use_container_width=True)

            if create_btn:
                q_mapped = "Mixed" if "Mixed" in sess_type else ("Numerical" if "Numerical" in sess_type else "MCQ")
                create_session(sess_name, sess_chapter, sess_diff, q_mapped)
                st.session_state.show_new_session_form = False
                st.rerun()


# ============================================================
# ACTIVE SESSION INTERFACE
# ============================================================
session = active_session()
if session is None:
    st.info("Please create or select a practice session from the sidebar.")
    st.stop()

stats = get_stats(session)

# Header Stats Dashboard
st.subheader(f"📖 {session['name']}")
st.caption(f"Chapter: **{session.get('chapter', 'All Chapters')}** · Level: **{session.get('difficulty', 'Intermediate')}** · Format: **{session.get('question_type', 'Mixed')}**")

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
stat_col1.metric("Total Questions", stats["total"])
stat_col2.metric("Attempted", stats["attempted"])
stat_col3.metric("Correct Answers", stats["correct"])
stat_col4.metric("Accuracy", f"{stats['accuracy']:.1f}%")

st.progress(stats["attempted"] / stats["total"] if stats["total"] else 0)
st.divider()

# Display questions in session
for idx, q in enumerate(session["questions"]):
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-weight: 700; font-size: 1.15rem; color: #f8fafc;">Question {idx + 1}</span>
                <span class="px-badge px-badge-purple">{q.get('chapter', 'JEE Physics')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.caption(f"Type: **{q['type']}** · Difficulty: **{q['difficulty']}**")
        st.markdown(q["prompt"])

        if q["type"] == "Numerical":
            st.caption(f"Enter numerical answer in **{q['unit']}** (tolerates small decimal rounding differences).")
            input_key = f"input_num_{session['id']}_{q['id']}"
            saved_resp = q.get("response")
            init_val = str(saved_resp) if saved_resp is not None else ""

            user_num_str = st.text_input(
                "Your Answer:",
                value=init_val,
                placeholder="Type numerical value...",
                key=input_key,
                disabled=q.get("checked", False),
            ).strip()

        else:
            options = q["options"]
            mcq_key = f"input_mcq_{session['id']}_{q['id']}"
            saved_resp = q.get("response")
            default_idx = options.index(saved_resp) if saved_resp in options else None

            user_choice = st.radio(
                "Select one option:",
                options=options,
                index=default_idx,
                key=mcq_key,
                disabled=q.get("checked", False),
            )

        btn1, btn2, btn3 = st.columns(3)

        with btn1:
            if not q.get("checked"):
                check_btn = st.button("Check Answer ⚡", key=f"chk_{session['id']}_{q['id']}", use_container_width=True, type="primary")
            else:
                check_btn = False

        with btn2:
            if not q.get("checked"):
                hint_btn = st.button("💡 Hint (3 Levels)", key=f"hnt_{session['id']}_{q['id']}", use_container_width=True)
            else:
                hint_btn = False

        with btn3:
            sol_btn = st.button("📖 View Full Solution", key=f"sol_{session['id']}_{q['id']}", use_container_width=True)

        # Hint logic
        if hint_btn:
            q["hint_level"] = min(q.get("hint_level", 0) + 1, len(q.get("hints", [])))
            save_active_session()
            st.rerun()

        if q.get("hint_level", 0) > 0:
            st.markdown("##### 💡 Progressive Hints:")
            for h_idx in range(q["hint_level"]):
                st.info(f"**Hint {h_idx + 1}:** {q['hints'][h_idx]}")

        # Check logic
        if check_btn:
            if q["type"] == "Numerical":
                if not user_num_str:
                    st.warning("Please type a numerical answer first.")
                    continue
                try:
                    num_val = float(user_num_str)
                except ValueError:
                    st.warning("Invalid numerical input. Please enter numbers and decimals only.")
                    continue

                q["response"] = num_val
                # Check tolerance
                tol = q.get("tolerance", 0.08)
                is_correct = math.isfinite(num_val) and abs(num_val - q["answer"]) <= max(tol, abs(q["answer"]) * 0.02)
                q["correct"] = is_correct

            else:
                if user_choice is None:
                    st.warning("Please select an option before checking.")
                    continue
                q["response"] = user_choice
                q["correct"] = user_choice == q["answer"]

            q["checked"] = True
            save_active_session()
            st.rerun()

        # Display result banner
        if q.get("checked"):
            if q.get("correct"):
                st.success("🎉 Correct Answer! Outstanding work.")
            else:
                st.error("❌ Incorrect answer. Check the step-by-step solution below.")

            if q["type"] == "Numerical":
                st.write(f"**Your Answer:** `{q['response']} {q['unit']}`  |  **Target Answer:** `{q['answer']} {q['unit']}`")
            else:
                st.write(f"**Your Answer:** {q['response']}")
                st.write(f"**Correct Answer:** {q['answer']}")

        # Solution view
        if sol_btn:
            q["solution_shown"] = True
            save_active_session()

        if q.get("solution_shown") or q.get("checked"):
            with st.expander("📝 Step-by-Step Worked Solution", expanded=True):
                if q["type"] == "Numerical":
                    if q.get("formula"):
                        st.markdown(f"**Governing Formula:**")
                        st.latex(q["formula"])
                    st.markdown("**Detailed Working:**")
                    st.markdown(q["working"])
                else:
                    st.markdown(f"**Correct Choice:** `{q['answer']}`")
                    st.markdown(f"**Conceptual Explanation:** {q['explanation']}")

# Session Actions
st.divider()
st.subheader("Keep Practicing")
a_col1, a_col2 = st.columns(2)

with a_col1:
    if st.button("➕ Generate Next Question in this Chapter", use_container_width=True, type="primary"):
        add_question(session)
        st.rerun()

with a_col2:
    if st.button("🔄 Configure Another Session", use_container_width=True):
        st.session_state.show_new_session_form = True
        st.rerun()
