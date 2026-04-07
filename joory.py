import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Family Task Tracker", layout="centered")

# --- SIMULATED DATABASE (Using Session State) ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏠 Family Hub")
menu = st.sidebar.radio(
    "Select an Option:",
    ("View Dashboard", "Parent: Add Task", "Child: Submit Proof", "Parent: Review Submissions")
)

# --- 1. DASHBOARD ---
if menu == "View Dashboard":
    st.title("📊 Task Dashboard")
    if not st.session_state.tasks:
        st.info("No tasks yet! Parent, please add one.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            status_color = "🟢" if task['status'] == "Completed" else "🟡"
            st.write(f"{status_color} **{task['name']}** - Assigned to: {task['child']}")

# --- 2. PARENT: ADD TASK ---
elif menu == "Parent: Add Task":
    st.title("➕ Assign a New Task")
    with st.form("task_form"):
        task_name = st.text_input("Task Description (e.g., Clean Room)")
        child_name = st.text_input("Child's Name")
        submitted = st.form_submit_button("Add Task")
       
        if submitted and task_name and child_name:
            st.session_state.tasks.append({
                "name": task_name,
                "child": child_name,
                "status": "Pending",
                "proof": None
            })
            st.success(f"Task assigned to {child_name}!")

# --- 3. CHILD: SUBMIT PROOF ---
elif menu == "Child: Submit Proof":
    st.title("📤 Submit Your Work")
    pending_tasks = [t['name'] for t in st.session_state.tasks if t['status'] == "Pending"]
   
    if not pending_tasks:
        st.warning("No pending tasks to complete!")
    else:
        task_to_finish = st.selectbox("Which task did you do?", pending_tasks)
        proof_text = st.text_area("Notes for Parent (e.g., 'Done!')")
        if st.button("Submit for Review"):
            for t in st.session_state.tasks:
                if t['name'] == task_to_finish:
                    t['status'] = "Reviewing"
                    t['proof'] = proof_text
            st.success("Sent! Wait for Parent to approve.")

# --- 4. PARENT: REVIEW SUBMISSIONS ---
elif menu == "Parent: Review Submissions":
    st.title("🧐 Review Work")
    review_list = [t for t in st.session_state.tasks if t['status'] == "Reviewing"]
   
    if not review_list:
        st.info("Nothing to review right now.")
    else:
        for t in review_list:
            st.write(f"**Task:** {t['name']} | **By:** {t['child']}")
            st.caption(f"Proof notes: {t['proof']}")
            if st.button(f"Approve {t['name']}"):
                t['status'] = "Completed"
                st.rerun()
