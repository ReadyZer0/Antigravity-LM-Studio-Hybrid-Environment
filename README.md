# Hybrid Environment: LM Studio + Antigravity Bridge

This repository provides a lightweight "Native Session Bridge" that allows an AI Agent (the "Manager") to delegate complex coding tasks to a local Expert Coder (the "Coder") running in LM Studio.

## 🌟 Why this approach?

When using cloud-based LLMs like **Gemini Flash**, token costs can escalate quickly if the entire conversation history and codebase context are sent with every single turn. This "Hybrid Environment" pattern solves this problem by using a **Manager-Coder Delegation** workflow.

### 🚀 Key Benefits:
- **Major Token Savings**: The "Manager" only handles high-level reasoning and task distribution. The heavy lifting (writing hundreds of lines of code) is done locally in LM Studio.
- **Extreme Speed**: Local models like **Qwen 2.5 Coder** are incredibly fast for specialized development tasks.
- **Enhanced Accuracy**: By delegating low-level system logic (Windows APIs, complex threading) to a specialized coding model, you reduce hallucinations in the Manager.
- **Privacy & Control**: Code generation happens on your local GPU, meaning sensitive codebase context stays on your machine.

---

## 🛠️ How it Works

The system consists of two primary layers:

### 1. The Manager layer
- **`delegate.py`**: A macro that takes a task description, writes it to a prompt file, and injects it directly into the active LM Studio conversation.
- **`retrieve.py`**: A polling script that watches the LM Studio session and automatically retrieves the generated code once it is finished.

### 2. The Core Bridge (`/core`)
- **`send_to_lmstudio.py`**: Interacts with LM Studio's internal `.conversation.json` files using the modern **Versioning Schema**.
- **`get_lmstudio_content.py`**: Parses the `multiStep` assistant responses from LM Studio.

---

## 📦 Setup & Usage

### Prerequisites:
1. **LM Studio** installed and running on your machine.
2. A coding model loaded (e.g., `Qwen 2.5 Coder 14B`).

### Workflow:
1. Identify a complex task in your workspace.
2. Run the delegation macro:
   ```bash
   python delegate.py "Refactor my Window Manager using ctypes and Win32"
   ```
3. Go to **LM Studio GUI** and click **"Generate"** on the newly injected message.
4. Once finished, run the retrieval macro:
   ```bash
   python retrieve.py
   ```
5. The finished code will be saved to `expert_solution.txt`, ready for implementation!

### Why Gemini Flash?
Using this bridge with **Gemini 2.0 Flash** is the current "Sweet Spot" for AI development:
- **Flash** provides the lightning-fast planning.
- **LM Studio** provides the deep coding expertise.
- **Result**: A professional-grade coding experience with near-zero API costs for large file generations.

---
**Maintained by**: [Your GitHub Profile]
**Part of the OpenClaw Ecosystem**
