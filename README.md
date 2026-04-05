<<<<<<< HEAD
# Antigravity - LM Studio Hybrid Environment

This repository provides a lightweight **"Native Session Bridge"** that allows a cloud-based AI Agent (the "Manager") to delegate complex, context-heavy coding tasks to a local Expert Coder (the "Coder") running in LM Studio.

---

## 🌟 Why Use This? (The Benefits)

As AI models like **Gemini 2.0 Flash** become faster and smarter, the main bottleneck remains **Token Cost & Context Bloat**. If you ask a cloud model to refactor a 500-line file using Windows APIs, you pay for thousands of tokens in and out. 

### This "Hybrid" pattern provides three massive advantages:
1. **📉 80-90% Token Savings**: You only send a short task description to the cloud Manager. The bulky code generation happens on your local GPU for **$0**.
2. **⚡ Specialist Performance**: Local models like **Qwen 2.5 Coder** are specifically fine-tuned for heavy development. They often outperform general-purpose cloud models on low-level system logic (Win32, C++, Hardware APIs).
3. **🔒 Privacy by Design**: Your proprietary codebase context stays within the LM Studio session on your machine; only the minimal task instructions are sent to the "Manager" model.

---

## 🛠️ How to Use with OpenClaw

This tool is designed to work seamlessly within the **OpenClaw** ecosystem. By adding the bridge to your agent's instructions, you can turn any agent (like Zen4 or Delta) into a **Strategic Manager**.

### 1. Configure the Agent (Zen4 / SOUL.md):
Add these delegation instructions to your agent's `SOUL.md` or `AGENTS.md`:
> "For any task involving complex logic, Windows APIs, or large refactors, you **must** delegate. 
> 📤 **To Delegate**: Run `python delegate.py "[Detailed Prompt]"`
> 📥 **To Retrieve**: Run `python retrieve.py` then read `expert_solution.txt`."

### 2. The Workflow:
1. **The Ask**: You ask your OpenClaw agent for a complex feature (e.g., "Add a Live Thumbnail viewer using gdi32").
2. **The Handoff**: The agent recognizes the complexity and runs `delegate.py`. 
   - *Result*: Your LM Studio GUI instantly lights up with the full technical prompt.
3. **The Generation**: You click **"Generate"** in LM Studio.
4. **The Retrieval**: You tell your agent "Retrieve" or "Done".
   - *Result*: The agent runs `retrieve.py`, grabs the professional code from the bridge, and applies it to your project.

---

## 📦 Script Overview

- **`delegate.py`**: The "Sender". It automatically detects your active LM Studio session, formats the prompt using the **Versioning Schema**, and injects it into the chat.
- **`retrieve.py`**: The "Receiver". It polls the LM Studio session file and extracts the latest `assistant` response, cleaning up any conversational meta-data.
- **`/core`**: The low-level bridge engine that handles the `.conversation.json` file parsing.

---

### Part of the OpenClaw Ecosystem
This project is part of a growing movement to decentralize AI coding by combining the planning power of the cloud with the specialized strength of local hardware.

**Created by**: [ReadyZer0](https://github.com/ReadyZer0) AKA
 [Ali Dheyaa Abdulwahab](https://www.linkedin.com/in/ali-dheyaa-abdulwahab-6bbbb1239/)
