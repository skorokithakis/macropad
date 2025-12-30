# Macropad

A 4x4 macro pad running ZMK firmware on a Nice!Nano v2.

## Features

- 4 layers, switchable via the top row buttons
- All keys send Ctrl+Shift+Cmd + a character (for use as global hotkeys)
- Layer 0: Numbers 1-0, minus, equals
- Layer 1: Q through ]
- Layer 2: A through `
- Layer 3: Z through Tab

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

**Bootloader mode:** Hold all four corner keys simultaneously.

**Clear Bluetooth pairings:** Hold all four layer buttons (top row) simultaneously.
