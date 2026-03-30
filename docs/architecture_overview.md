# Test.io Agent Architecture Overview

This document provides a high-level evaluation of the `.agents/` system, its relationship to the `.scripts/` and `src/tio/` tools, and the nature of the AI-client/user interaction.

## 1. System Architecture

The project employs a **Directive-Based Orchestration** architecture. It separates deterministic state management from heuristic AI reasoning, using a structured middle-ware layer (Python CLI) to bridge the two.

### Core Components

| Layer | Component | Responsibility |
| :--- | :--- | :--- |
| **State & Config** | `.agents/` | The "Source of Truth." Contains YAML/JSON manifests, state tracking, and AI prompt templates (generators). |
| **Application** | `src/tio/` | The "Orchestrator." Python logic that handles CLI commands, synchronizes manifests, and prepares AI directives. |
| **Automation** | `.scripts/` | "Utility Layer." Standalone scripts for maintenance tasks like manifest synchronization and watchdog monitors. |
| **Reasoning** | Gemini CLI | The "Execution Engine." Processes high-level directives and performs complex data synthesis or file generation. |

## 2. The Manifest & Synchronization Loop

The relationship between `.agents/` and the executable tools is maintained through a synchronization loop:

1.  **Source (YAML):** Users or AI edit YAML files in `.agents/generators/` or `.agents/state/`. These are human-readable and flexible.
2.  **Sync (`tio sync`):** The `SyncManager` (in `src/tio/actions/sync.py`) parses these YAML files and generates JSON manifests in `.agents/manifests/`.
3.  **Index (JSON):** The JSON manifests serve as a fast, machine-readable index. This allows the CLI to show command registries and check file "locks" without re-parsing every YAML file on every command.

## 3. The AI-Client/User Relationship

The system defines a clear hierarchy of interaction:

### A. The User (The Director)
The user initiates high-level intent via the `tio` CLI (e.g., `tio g bug_reports` or `tio z --start`). The user does not interact with the raw AI prompt directly but triggers a pre-defined workflow.

### B. The Client/Orchestrator (The Manager)
The Python CLI (`tio`) acts as the "Manager." Its job is to:
- **Enforce Constraints:** Check if a module is "locked" or if files exist.
- **Gather Context:** Read the relevant manifests and notes.
- **Formulate Directives:** Convert the user's intent into a structured YAML "Directive" for the AI.

### C. The AI (The Worker)
Gemini receives a **Directive Object**. Unlike a standard chatbot interaction, the AI is treated as a structured worker with specific instructions:
- **Search:** Look at specific manifest-indexed files.
- **Reason:** Synthesize data or answer questions.
- **Mutate:** Update state files (`.agents/state/`) or generate new reports.

## 4. Key Mechanisms

### Generators (`.agents/generators/`)
Generators are the "Blueprints" for AI behavior. Each YAML file defines the persona, context, and output requirements for a specific task (e.g., generating bug reports).

### Monitors & State (`.agents/monitors/` & `.agents/state/`)
These provide persistence. By externalizing state into YAML files, the AI can be "stateless" between turns, as the CLI will always inject the current state into the next directive.

### The "Bridge" (`src/tio/actions/bridge.py`)
This is the critical link. It abstracts the "Directive" generation, ensuring that the AI always receives a consistent interface for complex tasks like Academy intakes or Quiz management.

---

## 5. Architectural Evaluation

**Strengths:**
- **Deterministic:** The use of JSON manifests ensures the CLI is fast and predictable.
- **Traceable:** Every AI action is driven by a YAML directive, making it easy to debug "hallucinations."
- **Modular:** New capabilities can be added simply by creating a new `generator.yml` and running `tio sync`.

**Opportunities for Growth:**
- **Automated Validation:** Implementing schema validation for the YAML files in `.agents/` would prevent runtime errors in the Orchestrator.
- **Dynamic Context Injection:** Further refining the `DiscoveryManager` to inject only the most relevant "snippets" of code/notes into the AI context to save tokens.
