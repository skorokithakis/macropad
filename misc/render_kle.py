#!/usr/bin/env python3
"""
Render a KLE JSON file using the kle-render.herokuapp.com web form.

Usage: python render_kle.py <input.json> [output.png]
"""

import sys
from pathlib import Path

import requests


def render_kle(input_path: str, output_path: str | None = None) -> Path:
    input_file = Path(input_path)
    if output_path is None:
        output_file = input_file.with_suffix(".png")
    else:
        output_file = Path(output_path)

    with open(input_file, "rb") as f:
        response = requests.post(
            "https://kle-render.herokuapp.com/",
            files={"json": (input_file.name, f, "application/json")},
            data={"url": ""},
            timeout=60,
        )
    response.raise_for_status()

    output_file.write_bytes(response.content)
    print(f"Rendered to {output_file}")
    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.json> [output.png]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    render_kle(input_path, output_path)
