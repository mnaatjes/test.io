import argparse
import sys
from rich.console import Console
from .core import TioOrchestrator

console = Console()

def run_cli():
    parser = argparse.ArgumentParser(description="Tio-CLI: Orchestrator for TestIO Agent", add_help=False)
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show detailed command instructions")
    parser.add_argument("--for", dest="for_module", help="Filter quick reference for a specific module")
    parser.add_argument("cmd", nargs="?", help="Command shorthand (g, s, m, sync, d, q, l)")
    parser.add_argument("module", nargs="?", help="Target module (e.g., 'bugs')")
    parser.add_argument("--raw", action="store_true", help="Output raw data instead of formatted UI")
    
    # We need to handle the case where --for might be passed as --for academy
    args, unknown = parser.parse_known_args()
    
    tio = TioOrchestrator(raw_mode=args.raw)
    
    if args.help or args.cmd in ["h", "help"]:
        target = args.module if args.module else None
        tio.show_usage(verbose=True, target=target)
        return
    
    if args.cmd is None:
        tio.show_usage()
        return

    # Logical target selection
    # If 'q' is used with --for, use that. Otherwise use the positional 'module'
    final_module = args.for_module if args.for_module else args.module
    
    tio.execute(args.cmd, final_module)

if __name__ == "__main__":
    run_cli()
