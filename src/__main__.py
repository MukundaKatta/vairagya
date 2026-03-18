"""CLI for vairagya."""
import sys, json, argparse
from .core import Vairagya

def main():
    parser = argparse.ArgumentParser(description="Vairagya — Digital Detox Coach. AI-guided digital wellness and screen time management.")
    parser.add_argument("command", nargs="?", default="status", choices=["status", "run", "info"])
    parser.add_argument("--input", "-i", default="")
    args = parser.parse_args()
    instance = Vairagya()
    if args.command == "status":
        print(json.dumps(instance.get_stats(), indent=2))
    elif args.command == "run":
        print(json.dumps(instance.manage(input=args.input or "test"), indent=2, default=str))
    elif args.command == "info":
        print(f"vairagya v0.1.0 — Vairagya — Digital Detox Coach. AI-guided digital wellness and screen time management.")

if __name__ == "__main__":
    main()
