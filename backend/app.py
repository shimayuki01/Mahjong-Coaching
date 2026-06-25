from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from flask import Flask, Response, jsonify, request, send_file

app = Flask(__name__)

# Use an OCI image name or a local image name.
MJAI_REVIEWER_IMAGE = os.environ.get("MJAI_REVIEWER_IMAGE", "mjai-reviewer:latest")
CONTAINER_INPUT_PATH = "/work/input.json"


def run_mjai_reviewer(input_file: str, seat: int = 0) -> tuple[int, str, str]:
    cmd = [
        "docker",
        "run",
        "--rm",
        "-v",
        f"{input_file}:{CONTAINER_INPUT_PATH}:ro",
        MJAI_REVIEWER_IMAGE,
        "-e",
        "akochan",
        "--no-open",
        "-i",
        CONTAINER_INPUT_PATH,
        "-a",
        str(seat),
        "-o",
        "-",
    ]
    process = subprocess.run(cmd, capture_output=True, encoding='utf-8', errors='replace')
    return process.returncode, process.stdout, process.stderr


@app.route("/report", methods=["POST"])
def report() -> Response | tuple[str, int]:
    """Generate an HTML report from JSON input.

    POST body can be either JSON or multipart file upload.
    Query parameters:
      seat=0..3   東家=0 南家=1 西家=2 北家=3
    """
    seat = request.args.get("seat", "0")
    if seat not in {"0", "1", "2", "3"}:
        return jsonify(error="seat must be 0,1,2 or 3"), 400

    if request.is_json:
        body = request.get_data()
        if not body:
            return jsonify(error="Empty JSON body"), 400
    elif "file" in request.files:
        body = request.files["file"].read()
        if not body:
            return jsonify(error="Uploaded file is empty"), 400
    else:
        return jsonify(error="Provide JSON body or multipart file named 'file'"), 400

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as temp_file:
        temp_file.write(body)
        temp_path = temp_file.name

    try:
        code, stdout, stderr = run_mjai_reviewer(temp_path, int(seat))
        if code != 0:
            message = stderr or f"Docker exited with code {code}"
            return Response(message, status=500, mimetype="text/plain")
        return Response(stdout, mimetype="text/html")
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


@app.route("/", methods=["GET"])
def index() -> Response:
    return send_file(os.path.join(os.path.dirname(__file__), "frontend.html"))


@app.route("/healthz", methods=["GET"])
def healthz() -> Response:
    return Response("OK", mimetype="text/plain")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run mjai-reviewer via Flask or CLI")
    parser.add_argument("--file", help="Local JSON file to process")
    parser.add_argument("--seat", type=int, default=0, choices=range(0, 4), help="Seat number 0..3")
    parser.add_argument("--host", default="0.0.0.0", help="Flask host")
    parser.add_argument("--port", type=int, default=8000, help="Flask port")
    parser.add_argument("--serve", action="store_true", help="Start Flask server")
    args = parser.parse_args()

    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            return 1
        code, stdout, stderr = run_mjai_reviewer(args.file, args.seat)
        if code != 0:
            print(stderr or f"Docker exited with code {code}", file=sys.stderr)
            return code
        sys.stdout.buffer.write(stdout.encode("utf-8", errors="replace"))
        return 0

    if args.serve:
        app.run(host=args.host, port=args.port)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
