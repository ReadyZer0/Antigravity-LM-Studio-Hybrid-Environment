import sys
import os
import json
import time

# Portable session checkpoint handling
CHECKPOINT_FILE = os.path.join(os.path.dirname(__file__), "session_checkpoint.json")

def extract_content_from_message(msg):
    """
    Handles both Versioned (multiStep/singleStep) and Old-Style message structures from LM Studio.
    """
    if "versions" in msg:
        sel = msg.get("currentlySelected", 0)
        version = msg["versions"][sel]
        
        # Assistant Response (multiStep)
        if version.get("type") == "multiStep":
            full_text = ""
            for step in version.get("steps", []):
                if step.get("type") == "contentBlock":
                    for block in step.get("content", []):
                        if block.get("type") == "text":
                            full_text += block.get("text", "")
            return full_text.strip()
        
        # User/Simple Response (singleStep)
        elif version.get("type") == "singleStep":
            full_text = ""
            for block in version.get("content", []):
                if block.get("type") == "text":
                    full_text += block.get("text", "")
            return full_text.strip()
    return ""

def main():
    if not os.path.exists(CHECKPOINT_FILE):
        print("Error: No session checkpoint found. Did you run 'delegate.py'?")
        sys.exit(1)

    with open(CHECKPOINT_FILE, 'r', encoding='utf-8') as f:
        checkpoint = json.load(f)
        session_path = checkpoint.get("session_path")
        original_count = checkpoint.get("original_count")

    if not session_path or not os.path.exists(session_path):
        print(f"Error: Could not find session at {session_path}")
        sys.exit(1)

    print(f"\n[RECEIVE]: Watching {os.path.basename(session_path)} for Coder response...")

    # Watchdog Loop
    while True:
        try:
            with open(session_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                messages = data.get('messages', [])
                
                if len(messages) > original_count:
                    last_msg = messages[-1]
                    
                    # Check for role
                    role = ""
                    if "versions" in last_msg:
                        role = last_msg["versions"][last_msg.get("currentlySelected", 0)].get("role", "")
                    else:
                        role = last_msg.get("role", "")

                    if role == 'assistant':
                        content = extract_content_from_message(last_msg)
                        if content:
                            time.sleep(2) # Stabilize LM Studio auto-save
                            with open(session_path, 'r', encoding='utf-8') as f2:
                                data2 = json.load(f2)
                                final_content = extract_content_from_message(data2['messages'][-1])
                                if final_content == content:
                                    print("\n[SUCCESS]: Coder response detected!")
                                    print(final_content) # Final output to stdout
                                    break
        except (IOError, json.JSONDecodeError):
            time.sleep(0.5)
        time.sleep(1)

if __name__ == "__main__":
    main()
