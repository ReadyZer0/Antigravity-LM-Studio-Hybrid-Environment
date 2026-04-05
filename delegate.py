import sys
import os
import subprocess

# Portable relative paths for GitHub Repo
CORE_DIR = os.path.join(os.path.dirname(__file__), "core")
BRIDGE_SCRIPT = os.path.join(CORE_DIR, "send_to_lmstudio.py")

# Default prompt target
EXPERT_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "expert_prompt.txt")

def main():
    if len(sys.argv) < 2:
        print("Usage: python delegate.py \"[PROMPT]\"")
        sys.exit(1)

    prompt = sys.argv[1]

    # 1. Write the prompt to the expert_prompt.txt file
    try:
        with open(EXPERT_PROMPT_PATH, "w", encoding="utf-8") as f:
            f.write(prompt)
        print(f"Successfully wrote prompt to {EXPERT_PROMPT_PATH}")
    except Exception as e:
        print(f"Error writing prompt: {e}")
        sys.exit(1)

    # 2. Call the core bridge sender
    try:
        subprocess.run(["python", BRIDGE_SCRIPT, EXPERT_PROMPT_PATH], check=True)
        print("\n[SUCCESS]: Prompt injected into LM Studio. Please click 'Generate' in the GUI.")
    except Exception as e:
        print(f"Error calling bridge script: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
