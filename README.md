# Macropad

A 4x4 macro pad running ZMK firmware on a Nice!Nano v2.

## Features

- 15 layers, switchable via the top row buttons and button combinations
- All keys send RCtrl+Shift+Cmd + a character (for use as global hotkeys)
- Layers 0-3: Single button press on top row
  - Layer 0: Numbers 1-0, minus, equals
  - Layer 1: Q through ]
  - Layer 2: A through `
  - Layer 3: Z through Tab
- Layers 4-14: Activated by pressing multiple layer buttons simultaneously

## Building

Run the build script:

```bash
./build.sh
```

This uses Docker to build the firmware. Output is `build/zephyr/zmk.uf2`.

## Flashing

1. Put the board in bootloader mode (see below)
2. Copy `build/zephyr/zmk.uf2` to the USB mass storage device that appears

## Special combos

**Bootloader mode:** Long-press layer buttons 0 and 3 (leftmost and rightmost in top row) simultaneously.

**Clear Bluetooth pairings:** Long-press all four layer buttons (top row) simultaneously.
