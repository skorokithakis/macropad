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
    west build -s zmk/app -b nice_nano_v2 -p -- -DSHIELD=macropad -DZMK_CONFIG=/zmk-workspace"

echo "Firmware built: $SCRIPT_DIR/build/zephyr/zmk.uf2"
