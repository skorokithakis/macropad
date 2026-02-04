#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "Pillow",
#   "requests"
# ]
# ///
"""
Render KLE JSON layout files to PNG images.

When run without arguments, detects which layout files in config/layouts/
have uncommitted changes (or changed in the previous commit if nothing is
uncommitted) and renders those. Also regenerates KEYMAPS.md.
"""
import argparse
import io
import json
import re
import subprocess
import sys
from pathlib import Path

import requests
from PIL import Image

REPO_ROOT = Path(__file__).parent.parent
LAYOUTS_DIR = REPO_ROOT / "config" / "layouts"
OUTPUT_DIR = REPO_ROOT / "misc" / "layouts"
KEYMAPS_FILE = REPO_ROOT / "KEYMAPS.md"


TARGET_WIDTH = 849
TARGET_HEIGHT = 848


def render_kle(input_path: Path, output_path: Path) -> Path:
    """Render a single KLE JSON file to PNG using kle-render.herokuapp.com."""
    with open(input_path, "rb") as f:
        response = requests.post(
            "https://kle-render.herokuapp.com/",
            files={"json": (input_path.name, f, "application/json")},
            data={"url": ""},
            timeout=60,
        )
    response.raise_for_status()

    # Crop the image to the target size, keeping the top portion.
    image = Image.open(io.BytesIO(response.content))
    cropped = image.crop((0, 0, TARGET_WIDTH, TARGET_HEIGHT))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cropped.save(output_path, "PNG")
    print(f"Rendered {input_path.name} -> {output_path}")
    return output_path


def get_changed_layouts() -> list[Path]:
    """Get layout files that changed (uncommitted or in previous commit)."""
    changed_files = set()

    # Check for uncommitted changes (staged + unstaged).
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "--", "config/layouts/*.json"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            changed_files.add(REPO_ROOT / line.strip())

    # Check for untracked files.
    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "config/layouts/*.json"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    for line in result.stdout.strip().split("\n"):
        if line.strip():
            changed_files.add(REPO_ROOT / line.strip())

    # Also check the previous commit if no uncommitted changes found.
    if not changed_files:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "--", "config/layouts/*.json"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                changed_files.add(REPO_ROOT / line.strip())

    return sorted([f for f in changed_files if f.exists()])


def get_all_layouts() -> list[Path]:
    """Get all layout files."""
    return sorted(LAYOUTS_DIR.glob("*.json"))


def parse_layout_info(layout_path: Path) -> dict:
    """Extract layer number, name, and display name from a layout file."""
    # Parse filename: layer_<number>_<name>.json
    match = re.match(r"layer_(\d+)_(.+)\.json", layout_path.name)
    if not match:
        return {
            "number": 0,
            "name": layout_path.stem,
            "display_name": layout_path.stem,
        }

    layer_number = int(match.group(1))
    layer_name = match.group(2).replace("_", " ").title()

    # Try to get display name from JSON metadata.
    with open(layout_path) as f:
        data = json.load(f)

    display_name = f"Layer {layer_number}: {layer_name}"
    if isinstance(data, list) and data and isinstance(data[0], dict):
        if "name" in data[0]:
            display_name = data[0]["name"]

    return {
        "number": layer_number,
        "name": layer_name,
        "display_name": display_name,
    }


def generate_keymaps_md() -> None:
    """Generate KEYMAPS.md with links to all rendered layout images."""
    layouts = get_all_layouts()
    if not layouts:
        print("No layouts found, skipping KEYMAPS.md generation")
        return

    # Collect layout info and sort by layer number.
    layout_info = []
    for layout_path in layouts:
        info = parse_layout_info(layout_path)
        png_path = OUTPUT_DIR / f"{layout_path.stem}.png"
        info["png_exists"] = png_path.exists()
        info["png_relative"] = f"misc/layouts/{layout_path.stem}.png"
        info["json_relative"] = f"config/layouts/{layout_path.name}"
        layout_info.append(info)

    layout_info.sort(key=lambda x: x["number"])

    # Generate markdown.
    lines = [
        "# Keymaps",
        "",
        "Visual reference for all keymap layers.",
        "",
    ]

    for info in layout_info:
        lines.append(f"## {info['display_name']}")
        lines.append("")
        if info["png_exists"]:
            lines.append(f"![{info['display_name']}]({info['png_relative']})")
        else:
            lines.append(
                f"*Image not yet rendered. Run `python misc/render_kle.py --all` to generate.*"
            )
        lines.append("")

    KEYMAPS_FILE.write_text("\n".join(lines))
    print(f"Generated {KEYMAPS_FILE}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render KLE JSON layout files to PNG images.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s              Render changed layouts, update KEYMAPS.md
  %(prog)s --all        Render all layouts, update KEYMAPS.md
  %(prog)s layout.json  Render a single JSON file

When run without arguments, detects which layout files in config/layouts/
have uncommitted changes (or changed in the previous commit if nothing is
uncommitted) and renders those. Also regenerates KEYMAPS.md.
""",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="render all layouts instead of just changed ones",
    )
    parser.add_argument(
        "file",
        nargs="?",
        help="single JSON file to render (optional)",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Single-file mode.
    if args.file:
        input_path = Path(args.file)
        if not input_path.exists():
            print(f"Error: File not found: {input_path}", file=sys.stderr)
            sys.exit(1)
        output_path = OUTPUT_DIR / f"{input_path.stem}.png"
        render_kle(input_path, output_path)
        return

    # Determine which layouts to render.
    if args.all:
        layouts = get_all_layouts()
        print(f"Rendering all {len(layouts)} layouts...")
    else:
        layouts = get_changed_layouts()
        if not layouts:
            print("No layout changes detected in previous commit")
        else:
            print(f"Rendering {len(layouts)} changed layouts...")

    # Render each layout.
    for layout_path in layouts:
        output_path = OUTPUT_DIR / f"{layout_path.stem}.png"
        render_kle(layout_path, output_path)

    # Always regenerate KEYMAPS.md to keep it in sync.
    generate_keymaps_md()


if __name__ == "__main__":
    main()
