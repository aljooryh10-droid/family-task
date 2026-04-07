import time

class FamilyTaskManager:
    def __init__(self):
        self.tasks = []
        self.child_points = 0

    def parent_interface(self):
        print("\n--- Parent (Admin) Control ---")
        t_name = input("Enter task name: ")
        t_pts = int(input("Enter point value: "))
        self.tasks.append({
            "id": len(self.tasks) + 1,
            "name": t_name,
            "points": t_pts,
            "status": "Pending",
            "ai_rating": None
        })
        print(f"Task '{t_name}' assigned.")

    def child_interface(self):
        print(f"\n--- Child Dashboard (Total Points: {self.child_points}) ---")
        pending = [t for t in self.tasks if t["status"] == "Pending"]
        if not pending:
            print("No tasks assigned yet!")
            return

        for t in pending:
            print(f"[{t['id']}] {t['name']} - {t['points']} pts")
       
        choice = int(input("Enter task ID to submit proof: "))
        for t in self.tasks:
            if t["id"] == choice:
                print(f"Simulating camera capture for: {t['name']}...")
                time.sleep(1)
                t["status"] = "Submitted"
                t["ai_rating"] = 8  # Simulated AI evaluation
                print("Proof submitted! Awaiting parental approval.")

    def approval_workflow(self):
        print("\n--- Pending Approvals ---")
        to_approve = [t for t in self.tasks if t["status"] == "Submitted"]
        if not to_approve:
            print("No submissions to review.")
            return

        for t in to_approve:
            print(f"[{t['id']}] {t['name']} | AI Suggestion: {t['ai_rating']}/10")
            ans = input("Approve? (y/n): ")
            if ans.lower() == 'y':
                t["status"] = "Completed"
                self.child_points += t["points"]
                print(f"Points credited! New Balance: {self.child_points}")

# Run Application Loop
app = FamilyTaskManager()
while True:
    print("\n1. Parent: Add Task\n2. Child: Submit Proof\n3. Parent: Review Submissions\n4. Exit")
    cmd = input("Select Action: ")
    if cmd == "1": app.parent_interface()
    elif cmd == "2": app.child_interface()
    elif cmd == "3": app.approval_workflow()
    elif cmd == "4": break
