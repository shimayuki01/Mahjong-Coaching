from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Call the Flask report endpoint with curl")
    parser.add_argument("--file", help="Local JSON file to upload")
    parser.add_argument("--json", help="JSON body file path")
    parser.add_argument("--url", help="Tenhou log URL")
    parser.add_argument("--seat", type=int, default=0, choices=range(0, 4), help="Seat number 0..3")
    parser.add_argument("--output", default="report.html", help="Output HTML file")
    parser.add_argument("--endpoint", default="http://localhost:8000/report", help="Flask report endpoint")
    return parser


def run_curl(args: argparse.Namespace) -> int:
    if not any([args.file, args.json, args.url]):
        print("Error: one of --file, --json, or --url is required", file=sys.stderr)
        return 1

    if args.file and not os.path.exists(args.file):
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        return 1

    if args.json and not os.path.exists(args.json):
        print(f"Error: JSON file not found: {args.json}", file=sys.stderr)
        return 1

    endpoint = f"{args.endpoint}?seat={args.seat}"
    cmd = ["curl", "-X", "POST", endpoint]

    if args.url:
        cmd.extend(["-G", "--data-urlencode", f"source_type=url", "--data-urlencode", f"url={args.url}"])
    elif args.file:
        cmd.extend(["-F", f"file=@{args.file}"])
    else:
        cmd.extend(["-H", "Content-Type: application/json", "--data-binary", f"@{args.json}"])

    cmd.extend(["-o", args.output])

    print("Running:", " ".join(cmd))
    completed = subprocess.run(cmd, capture_output=True, text=True)
    if completed.returncode != 0:
        if completed.stderr:
            print(completed.stderr, file=sys.stderr)
        return completed.returncode

    print(f"Saved output to {args.output}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return run_curl(args)


if __name__ == "__main__":
    raise SystemExit(main())
