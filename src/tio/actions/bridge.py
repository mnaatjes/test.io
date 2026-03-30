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
        """Directive for Gemini to answer a quiz question and update state."""
        directive = {
            "action": "quiz_answer",
            "quiz_id": quiz_id,
            "question": question,
            "context_files": context_files,
            "instruction": (
                "1. Search the context_files for the best answer.\n"
                "2. Provide the answer and a short reasoning to the user.\n"
                "3. UPDATE '.agents/state/state.quiz.yml' by filling in the 'answer' and 'reasoning' fields for this question entry."
            )
        }
        print(f"\n[DIRECTIVE: QUIZ_QUESTION]\n{yaml.dump(directive)}\n")

    def dispatch_quiz_end(self, state, reason):
        """Directive for Gemini to finalize the quiz and write the SINGLE log file."""
        directive = {
            "action": "quiz_finalize",
            "state": state,
            "reason": reason,
            "instruction": (
                "1. Prompt the user for the quiz outcome (score, pass/fail).\n"
                "2. SAVE a SINGLE YML file containing ALL questions/answers to 'academy/quizzes/questions/{quiz_id}.yml'.\n"
                "3. SAVE a timestamped Markdown report to 'academy/quizzes/notes/'."
            )
        }
        print(f"\n[DIRECTIVE: QUIZ_END]\n{yaml.dump(directive)}\n")

    def dispatch_intake_start(self, session_id, title):
        """Directive for Gemini to acknowledge a new intake session."""
        directive = {
            "action": "intake_start",
            "session_id": session_id,
            "title": title,
            "instruction": "Acknowledge the start of a new Academy intake session. Prepare to receive raw content."
        }
        print(f"\n[DIRECTIVE: INTAKE_START]\n{yaml.dump(directive)}\n")

    def dispatch_intake_content(self, session_id, content):
        """Directive for Gemini to process raw content and save to academy/tmp/."""
        directive = {
            "action": "intake_content",
            "session_id": session_id,
            "content": content,
            "instruction": (
                "1. ANALYZE the raw content provided.\n"
                "2. ORGANIZE it into a structured YML format for efficiency.\n"
                "3. SAVE the structured data as a new file in 'academy/tmp/' using a descriptive filename (e.g., 'academy/tmp/{topic}.yml').\n"
                "4. CONFIRM the file has been saved."
            )
        }
        print(f"\n[DIRECTIVE: INTAKE_CONTENT]\n{yaml.dump(directive)}\n")

    def dispatch_intake_end(self, state):
        """Directive for Gemini to finalize the intake session."""
        directive = {
            "action": "intake_finalize",
            "state": state,
            "instruction": (
                "1. REVIEW all content recently added to 'academy/tmp/' during this session.\n"
                "2. CREATE new quick_ref YML files in '.agents/generators/' (if applicable) using 'generator.quick_reference.{topic}.yml'.\n"
                "3. CREATE new notes Markdown files in 'academy/notes/' using 'notes_{topic}.md'.\n"
                "4. INDICATE completion and SUMMARIZE all content input during this session."
            )
        }
        print(f"\n[DIRECTIVE: INTAKE_END]\n{yaml.dump(directive)}\n")
