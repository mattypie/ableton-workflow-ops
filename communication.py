import json
import os
import time

class AutomationState:
    def __init__(self, state_file="automation_state.json"):
        self.state_file = state_file

    def write_state(self, state_dict):
        """Writes current state to the JSON file."""
        with open(self.state_file, 'w') as f:
            json.dump(state_dict, f, indent=4)

    def read_state(self):
        """Reads current state from the JSON file."""
        if not os.path.exists(self.state_file):
            return {}
        try:
            with open(self.state_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def wait_for_status(self, target_status, timeout=300, poll_interval=2):
        """
        Polls the state file until a target status is reached or timeout occurs.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            state = self.read_state()
            current_status = state.get("status")
            if current_status == target_status:
                return state
            
            # Handle error status if M4L reports one
            if current_status == "error":
                raise Exception(f"M4L reported an error: {state.get('message')}")
                
            time.sleep(poll_interval)
            
        raise TimeoutError(f"Timed out waiting for status: {target_status}")

if __name__ == "__main__":
    # Example usage
    state = AutomationState()
    state.write_state({"status": "idle", "project": "None"})
    print("State initialized.")
