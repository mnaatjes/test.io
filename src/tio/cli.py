import argparse
import sys
from rich.console import Console
from .core import TioOrchestrator

console = Console()

def run_cli():
    parser = argparse.ArgumentParser(description="Tio-CLI: Orchestrator for TestIO Agent", add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed command instructions")
    parser.add_argument("--for", dest="for_module", help="Filter for a specific module")
    
    # Quiz Specific Flags
    parser.add_argument("--start", dest="quiz_start", help="Start a new quiz session (Optional: quiz number)")
    parser.add_argument("--eoq", "--end", "--quit", "--q", dest="quiz_end", action="store_true", help="End the current quiz session")

    parser.add_argument("cmd", nargs="?", help="Command(s) (e.g., 'g', 'sync', 'quiz')")
    parser.add_argument("module", nargs="?", help="Target or question text")
    parser.add_argument("--raw", action="store_true", help="Output raw data instead of formatted UI")
    
    args, unknown = parser.parse_known_args()
    
    options = {
        "verbose": args.verbose,
        "quiz_start": args.quiz_start,
        "quiz_end": args.quiz_end
    }
    
    tio = TioOrchestrator(raw_mode=args.raw, options=options)
    
    if args.help or args.cmd in ["h", "help"]:
        target = args.module if args.module else None
        tio.show_usage(verbose=True, target=target)
        return
    
    if args.cmd is None:
        tio.show_usage()
        return

    commands = args.cmd.split(",")
    final_target = args.for_module if args.for_module else args.module
    
    for c in commands:
        tio.execute(c.strip(), final_target)

if __name__ == "__main__":
    run_cli()
