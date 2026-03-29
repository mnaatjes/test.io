import yaml
import json
from pathlib import Path

class GeminiBridge:
    """Bridges the Python CLI to the Gemini CLI (The AI)."""

    def __init__(self, orchestrator):
        self.tio = orchestrator

    def dispatch_generator(self, module_name):
        yml_path = self.tio.get_agent_path("generators", module_name, prefix="generator")
        if not yml_path:
            self.tio.log(f"Error: Generator for '{module_name}' not found.", "red")
            return

        with open(yml_path, 'r') as f:
            data = yaml.safe_load(f)

        print(f"\n[DIRECTIVE: {module_name}]\n{yaml.dump(data)}\n")

    def dispatch_quiz_question(self, question, context_files, quiz_id):
        """Directive for Gemini to answer a quiz question using context."""
        directive = {
            "action": "quiz_answer",
            "quiz_id": quiz_id,
            "question": question,
            "context_files": context_files,
            "instruction": "Search the context_files for the best answer. Provide the answer and a short reasoning. Format and store the question/answer in a YML file in academy/quizzes/questions/."
        }
        print(f"\n[DIRECTIVE: QUIZ_QUESTION]\n{yaml.dump(directive)}\n")

    def dispatch_quiz_end(self, state, reason):
        """Directive for Gemini to finalize the quiz and write the report."""
        directive = {
            "action": "quiz_finalize",
            "state": state,
            "reason": reason,
            "instruction": "Prompt the user for the quiz outcome (score, pass/fail). Store a Markdown report in academy/quizzes/notes/ with the quiz questions, correct answers, and final score. Ensure the filename is timestamped."
        }
        print(f"\n[DIRECTIVE: QUIZ_END]\n{yaml.dump(directive)}\n")
