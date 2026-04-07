import streamlit as st

# --- 1. INITIALIZE DATA ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "child_points" not in st.session_state:
    st.session_state.child_points = 0

st.sidebar.title("🏡 Family Task Hub")
role = st.sidebar.radio("Switch Role:", ["Child (User)", "Parent (Admin)"])

# --- 2. PARENT INTERFACE ---
if role == "Parent (Admin)":
    st.header("👨‍👩‍👧‍👦 Parent Dashboard")
    
    with st.expander("➕ Assign New Task"):
        t_name = st.text_input("Task Name")
        t_pts = st.number_input("Points", min_value=1, value=10)
        if st.button("Add Task"):
            # Add new task to the list
            st.session_state.tasks.append({
                "name": t_name, "points": t_pts, "status": "Pending", "proof": None
            })
            st.success("Task added!")
            st.rerun()

    st.subheader("📋 Pending Approvals")
    # Find only tasks that are 'Submitted'
    pending = [t for t in st.session_state.tasks if t["status"] == "Submitted"]
    
    if not pending:
        st.info("No tasks waiting for approval.")
    else:
        for i, task in enumerate(st.session_state.tasks):
            if task["status"] == "Submitted":
                with st.container(border=True):
                    st.write(f"**Task:** {task['name']}")
                    st.image(task["proof"], width=300)
                    if st.button(f"✅ Approve Task {i}", key=f"app_{i}"):
                        task["status"] = "Completed"
                        st.session_state.child_points += task["points"]
                        st.rerun()

# --- 3. CHILD INTERFACE ---
else:
    st.header("👦 Child Dashboard")
    st.metric("My Points ⭐", st.session_state.child_points)
    
    st.subheader("🚀 My Chores")
    for i, task in enumerate(st.session_state.tasks):
        if task["status"] == "Pending":
            with st.container(border=True):
                st.write(f"**Task:** {task['name']} ({task['points']} pts)")
             

   

photo = st.camera_input(f"Capture proof for {task['name']}", key=f"cam_{i}")
                
                # 2. The NEW Submit Button (Only shows after photo is taken)
                if photo:
                    st.success("Photo captured! Now click submit below.")
                    if st.button(f"📤 Click here to Submit {task['name']}", key=f"sub_{i}"):
                        # Save the photo to the task list
                        st.session_state.tasks[i]["proof"] = photo
                        st.session_state.tasks[i]["status"] = "Submitted"
                        
                        st.balloons() # Fun animation for the child!
                        st.success("Sent to Parent for approval!")
                        st.rerun() # Refresh to move the task to 'Submitted'





