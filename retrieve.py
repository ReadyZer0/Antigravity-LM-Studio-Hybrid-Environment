import subprocess
import os
import sys

# Portable relative paths for GitHub Repo
CORE_DIR = os.path.join(os.path.dirname(__file__), "core")
RETRIEVE_SCRIPT = os.path.join(CORE_DIR, "get_lmstudio_content.py")

# Default solution target
EXPERT_SOLUTION_PATH = os.path.join(os.path.dirname(__file__), "expert_solution.txt")

def main():
    # 1. Run the retrieval bridge
    try:
        # Run the script and capture the output
        result = subprocess.run(["python", RETRIEVE_SCRIPT], capture_output=True, text=True, check=True)
        
        # 2. Extract the actual code
        output = result.stdout
        if "[SUCCESS]" in output:
            code = output.split("[SUCCESS]: Coder response detected!")[-1].strip()
            
            # 3. Save the code for Zen4/Manager to read
            with open(EXPERT_SOLUTION_PATH, 'w', encoding='utf-8') as f:
                f.write(code)
            
            print(f"Successfully retrieved and saved fix to {EXPERT_SOLUTION_PATH}")
        else:
            print(f"Error: Retrieval bridge failed to find a valid response.\n{output}")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"Error calling retrieval bridge: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
