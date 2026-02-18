#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

VERSION="v2"
OUTPUT_DIR=""

while getopts "v:" opt; do
	case $opt in
	v)
		VERSION="v$OPTARG"
		;;
	*)
		echo "Usage: $0 [-v 1|2] [output_dir]" >&2
		echo "  -v 1  Build for hand-wired version" >&2
		echo "  -v 2  Build for PCB version (default)" >&2
		exit 1
		;;
	esac
done
shift $((OPTIND - 1))

OUTPUT_DIR="$1"

if [[ "$VERSION" != "v1" && "$VERSION" != "v2" ]]; then
	echo "Error: version must be 1 or 2" >&2
	exit 1
fi

PINS_FILE="$SCRIPT_DIR/config/boards/shields/stavropad/pins_${VERSION}.overlay"
OVERLAY_FILE="$SCRIPT_DIR/config/boards/shields/stavropad/stavropad.overlay"

cp "$PINS_FILE" "$OVERLAY_FILE"
echo "Using pin configuration: $VERSION"

docker run --rm \
	-v "$SCRIPT_DIR:/zmk-workspace" \
	-w /zmk-workspace \
	zmkfirmware/zmk-dev-arm:stable \
	/bin/bash -c "git config --global --add safe.directory '*' && \
    [ -d .west ] || west init -l config && \
    west update && \
    west zephyr-export && \
    west build -s zmk/app -b nice_nano_v2 -p -- -DSHIELD=stavropad -DZMK_CONFIG=/zmk-workspace/config -DZMK_EXTRA_MODULES='/zmk-workspace/zmk-modules/batt_type;/zmk-workspace/zmk-modules/persistent_layer'"

echo "Firmware built: $SCRIPT_DIR/build/zephyr/zmk.uf2"

if [ -n "$OUTPUT_DIR" ]; then
	if [ -d "$OUTPUT_DIR" ]; then
		cp "$SCRIPT_DIR/build/zephyr/zmk.uf2" "$OUTPUT_DIR"
		echo "Copied firmware to: $OUTPUT_DIR/zmk.uf2"
	else
		echo "Error: '$OUTPUT_DIR' is not a valid directory" >&2
		exit 1
	fi
fi
