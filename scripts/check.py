"""Run existing offline checks from any directory without rebuilding assets."""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    node = shutil.which("node")
    if node is None:
        print("Node.js is required; install Node.js 22+ and retry.", file=sys.stderr)
        return 1
    if sys.version_info < (3, 11):
        print("Python 3.11+ is required.", file=sys.stderr)
        return 1

    # These scripts use only the standard library; avoid user site startup hooks
    # and bytecode writes, including when check-extras imports refresh-stats.
    python = [sys.executable, "-I", "-S", "-B", "-X", "utf8"]
    checks = [
        ("Theme and icons", python + ["scripts/check-theme.py"]),
        ("CLI companions, fonts and installer fixtures", python + ["scripts/check-extras.py"]),
        ("Site, bilingual docs and media", [node, "scripts/check-site.mjs"]),
        ("Browser JavaScript syntax", [node, "--check", "docs/app.js"]),
        ("Public example", [node, "--test", "examples/date-kit/format.test.mjs"]),
    ]
    for label, command in checks:
        print(f"\n{label}", flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode:
            print(f"Failed: {label} (exit {result.returncode})", file=sys.stderr)
            return 1
    print("\nAll offline checks passed. Visual and Orca host checks are separate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
