import sys
import os
import json
import time
import logging

# Portable conversation directory detection
USER_PROFILE = os.environ.get("USERPROFILE", "")
CONVERSATIONS_DIR = os.path.join(USER_PROFILE, ".lmstudio", "conversations")

# Local session checkpoint
CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), "session_checkpoint.json")

def get_latest_session():
    """Finds the most recently modified LM Studio conversation file."""
    if not os.path.exists(CONVERSATIONS_DIR):
        print(f"Error: Could not find LM Studio conversations at {CONVERSATIONS_DIR}")
        return None
    try:
        files = [os.path.join(CONVERSATIONS_DIR, f) for f in os.listdir(CONVERSATIONS_DIR) if f.endswith(".json")]
        if not files:
            return None
        return max(files, key=os.path.getmtime)
    except Exception as e:
        print(f"Failed to list conversations: {e}")
        return None

def inject_message(session_path, prompt):
    """Appends a new user message to the specified conversation JSON with Versioning Schema."""
    for _ in range(5): # Retry loop for file locks
        try:
            with open(session_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            ms_now = int(time.time() * 1000)
            
            new_msg = {
                "versions": [
                    {
                        "type": "singleStep",
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ],
                "currentlySelected": 0
            }
            
            data.setdefault('messages', []).append(new_msg)
            data['userLastMessagedAt'] = ms_now
            
            with open(session_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            
            return len(data['messages']) # Return the message count
            
        except (IOError, json.JSONDecodeError) as e:
            time.sleep(0.5)
    return -1

def main():
    if len(sys.argv) < 2:
        print("Error: No prompt file provided.")
        sys.exit(1)

    prompt_file = sys.argv[1]
    if not os.path.exists(prompt_file):
        print(f"Error: Could not find {prompt_file}")
        sys.exit(1)

    with open(prompt_file, 'r', encoding='utf-8') as f:
        prompt_text = f.read()

    session_path = get_latest_session()
    if not session_path:
        sys.exit(1)

    new_count = inject_message(session_path, prompt_text)
    if new_count == -1:
        print("Error: Could not inject prompt (file locked).")
        sys.exit(1)

    checkpoint = {
        "session_path": session_path,
        "original_count": new_count
    }
    with open(CHECKPOINT_FILE, 'w', encoding='utf-8') as f:
        json.dump(checkpoint, f, indent=2)

    print(f"\n[SEND]: Successfully injected prompt into {os.path.basename(session_path)}.")

if __name__ == "__main__":
    main()
