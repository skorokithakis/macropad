#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

docker run --rm \
  -v "$SCRIPT_DIR:/zmk-workspace" \
  -w /zmk-workspace \
  zmkfirmware/zmk-dev-arm:stable \
  /bin/bash -c "git config --global --add safe.directory '*' && \
    [ -d .west ] || west init -l config && \
    west update && \
    west zephyr-export && \
    west build -s zmk/app -b nice_nano_v2 -p -- -DSHIELD=macropad -DZMK_CONFIG=/zmk-workspace -DZMK_EXTRA_MODULES=/zmk-workspace/zmk-modules/batt_type"

echo "Firmware built: $SCRIPT_DIR/build/zephyr/zmk.uf2"

if [ -n "$1" ]; then
  if [ -d "$1" ]; then
    cp "$SCRIPT_DIR/build/zephyr/zmk.uf2" "$1"
    echo "Copied firmware to: $1/zmk.uf2"
  else
    echo "Error: '$1' is not a valid directory" >&2
    exit 1
  fi
fi
