import streamlit as st

# --- INITIALIZE DATA ---
# We use session_state so tasks don't disappear when you click buttons
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "child_points" not in st.session_state:
    st.session_state.child_points = 0

st.sidebar.title("🏡 Family Hub 2026")
role = st.sidebar.radio("Switch Role:", ["Child (User)", "Parent (Admin)"])

# --- PARENT INTERFACE ---
if role == "Parent (Admin)":
    st.header("👨‍👩‍👧‍👦 Parent Dashboard")
    
    # 1. Create Task
    with st.expander("➕ Assign New Chore"):
        t_name = st.text_input("What needs to be done?")
        t_points = st.number_input("Points for this task", min_value=1, value=10)
        if st.button("Send to Child"):
            if t_name:
                st.session_state.tasks.append({
                    "name": t_name, 
                    "points": t_points, 
                    "status": "Pending", 
                    "proof": None
                })
                st.success(f"Task '{t_name}' assigned!")
                st.rerun() # Refresh to show in child's view

    # 2. Approve Tasks
    st.subheader("📋 Pending Approvals")
    pending_tasks = [t for t in st.session_state.tasks if t["status"] == "Submitted"]
    
    if not pending_tasks:
        st.write("No tasks waiting for approval.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if task["status"] == "Submitted":
                with st.container(border=True):
                    st.write(f"**Task:** {task['name']}")
                    st.image(task["proof"], width=300)
                    if st.button(f"✅ Approve & Give {task['points']} pts", key=f"app_{i}"):
                        task["status"] = "Completed"
                        st.session_state.child_points += task["points"]
                        st.success("Points awarded!")
                        st.rerun()

# --- CHILD INTERFACE ---
else:
    st.header("👦 Child Dashboard")
    st.metric("My Total Points ⭐", st.session_state.child_points)
    
    st.subheader("🚀 My Chores To Do")
    active_tasks = [t for t in st.session_state.tasks if t["status"] == "Pending"]
    
    if not active_tasks:
        st.info("Great job! You've finished all your tasks for today.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if task["status"] == "Pending":
                with st.container(border=True):
                    st.write(f"**{task['name']}** — Worth {task['points']} points")
                    # Unique key for each camera is required
                    img_file = st.camera_input(f"Take a photo of: {task['name']}", key=f"cam_{i}")
                    
                    if img_file:
                        task["proof"] = img_file
                        task["status"] = "Submitted"
                        st.warning("Sent! Waiting for Parent to check it.")
                        st.rerun() # This moves the task to the Parent's "Pending" list
