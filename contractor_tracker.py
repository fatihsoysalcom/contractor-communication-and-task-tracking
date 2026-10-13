import json
from collections import defaultdict

class ProjectManager:
    def __init__(self):
        self.tasks = defaultdict(list)
        self.contractor_feedback = defaultdict(list)
        self.communication_log = []

    def add_task(self, task_id, description, assigned_contractor):
        """Adds a new task to the project."""
        self.tasks[assigned_contractor].append({'id': task_id, 'description': description, 'status': 'Pending'})
        self.log_communication(f"Task {task_id} added: '{description}' assigned to {assigned_contractor}.")

    def update_task_status(self, task_id, new_status, contractor_name):
        """Updates the status of a specific task."""
        found = False
        for contractor, task_list in self.tasks.items():
            for task in task_list:
                if task['id'] == task_id:
                    if contractor == contractor_name:
                        task['status'] = new_status
                        self.log_communication(f"Task {task_id} status updated to '{new_status}' by {contractor_name}.")
                        found = True
                        break
                    else:
                        self.log_communication(f"Attempted status update for Task {task_id} by unauthorized contractor {contractor_name}. Expected {contractor}.")
                        return False
            if found:
                break
        if not found:
            self.log_communication(f"Task {task_id} not found for status update.")
        return found

    def record_feedback(self, contractor_name, feedback_message):
        """Records feedback from a contractor."""
        self.contractor_feedback[contractor_name].append(feedback_message)
        self.log_communication(f"Feedback recorded from {contractor_name}: '{feedback_message}'.")

    def log_communication(self, message):
        """Logs a communication event."""
        self.communication_log.append(message)

    def review_project_status(self):
        """Reviews the current status of all tasks and feedback."""
        print("\n--- Project Status Review ---")
        print("\nTasks by Contractor:")
        for contractor, task_list in self.tasks.items():
            print(f"  {contractor}:")
            if not task_list:
                print("    No tasks assigned.")
            for task in task_list:
                print(f"    - Task {task['id']}: {task['description']} (Status: {task['status']})")

        print("\nContractor Feedback:")
        for contractor, feedback_list in self.contractor_feedback.items():
            print(f"  {contractor}:")
            if not feedback_list:
                print("    No feedback recorded.")
            for feedback in feedback_list:
                print(f"    - {feedback}")

        print("\nCommunication Log:")
        if not self.communication_log:
            print("  No communication logged.")
        for log_entry in self.communication_log:
            print(f"  - {log_entry}")
        print("---------------------------\n")

# --- Example Usage ---
if __name__ == "__main__":
    manager = ProjectManager()

    # Adding initial tasks
    manager.add_task('T001', 'Implement user authentication', 'AlphaDevs')
    manager.add_task('T002', 'Design database schema', 'BetaCoders')
    manager.add_task('T003', 'Develop API endpoints', 'AlphaDevs')

    # Simulating updates and feedback
    manager.update_task_status('T001', 'In Progress', 'AlphaDevs')
    manager.record_feedback('AlphaDevs', 'Encountered unexpected dependency issue for T001.')
    manager.update_task_status('T002', 'Completed', 'BetaCoders')
    manager.update_task_status('T003', 'Blocked', 'AlphaDevs')
    manager.record_feedback('AlphaDevs', 'Blocked on T003 due to external API changes. Requesting clarification.')

    # Reviewing the project status - this helps identify issues early
    manager.review_project_status()

    # Simulating a communication breakdown or misunderstanding
    manager.update_task_status('T001', 'Completed', 'BetaCoders') # Incorrect contractor
    manager.record_feedback('BetaCoders', 'Completed T001 as requested.') # Misinformed feedback

    # Reviewing again to see the impact of miscommunication
    manager.review_project_status()
