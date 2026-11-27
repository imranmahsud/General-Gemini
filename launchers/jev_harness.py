import sys
import json
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Jev System One Decision Harness for Coding Agents")
    parser.add_argument("--task", type=str, help="Task description / target specification", default="Inspect workspace condition")
    parser.add_argument("--workspace", type=str, help="Working directory", default=".")
    parser.add_argument("--verify", action="store_true", help="Run verification pass")
    args = parser.parse_args()

    print("==================================================")
    print("      JEV SYSTEM ONE DECISION HARNESS             ")
    print("==================================================")
    
    # 5 Typed Decision Primitives
    decision_frame = {
        "TASK": args.task,
        "STATE": {
            "cwd": os.path.abspath(args.workspace),
            "files_count": len(os.listdir(args.workspace)) if os.path.exists(args.workspace) else 0,
            "git_present": os.path.exists(os.path.join(args.workspace, ".git"))
        },
        "ROUTE": "EXECUTE_SINGLE_STATION",
        "BOUNDS": {
            "timeout_seconds": 60,
            "max_output_tokens": 1024,
            "allow_network": True,
            "prose_free": True
        },
        "VERDICT": "READY"
    }

    print(json.dumps(decision_frame, indent=2))
    print("\n[OK] Decision state locked. Dispatched without KV-cache token overhead.")

if __name__ == "__main__":
    main()
