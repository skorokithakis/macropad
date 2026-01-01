# Macropad

A 4x4 macro pad running ZMK firmware on a Nice!Nano v2.

## Features

- 16 layers, switchable via the top row buttons and button combinations
- All keys send RCtrl+Shift+Cmd + a character (for use as global hotkeys)
- Idle deep sleep enabled; wakes on any key press after inactivity
- 11 Bluetooth profiles via dedicated BT control layer
- Layers 0-3: Single button press on top row
  - Layer 0: Numbers 1-0, minus, equals
  - Layer 1: Q through ]
  - Layer 2: A through `
  - Layer 3: Z through Tab
- Layers 4-15: Activated by pressing multiple layer buttons simultaneously
  - Layer 12 (buttons 0+2+3): Gaming layer - WASD layout with ESC/TAB/CTRL on left column, ALT/Enter/Space on bottom row
  - Layer 13 (buttons 1+2+3): Numpad - 7-8-9/4-5-6/1-2-3 with +, Enter, and 0
  - Layer 14 (all 4 buttons tap): QWERTY - Q/W/E/R, A/S/D/F, Z/X/C/V
  - Layer 15 (all 4 buttons hold 1s): Bluetooth control layer (see below)

## Building

Run the build script:

```bash
./build.sh
```

This uses Docker to build the firmware. Output is `build/zephyr/zmk.uf2`.
The custom shield and keymap live under `config/boards/shields/macropad`.

## Flashing

1. Put the board in bootloader mode (see below)
2. Copy `build/zephyr/zmk.uf2` to the USB mass storage device that appears

## Special combos

**Bootloader mode:** Long-press layer buttons 0 and 3 (leftmost and rightmost in top row) simultaneously. Short-press for layer 6.

**Bluetooth control layer:** Hold all 4 layer buttons (top row) for 1 second to switch to layer 15. On layer 15:
- Keys 1-4 (second row) select profiles 0-3
- Keys 5-8 (third row) select profiles 4-7
- Keys 9-11 (bottom row, first three keys) select profiles 8-10
- Key 12 (bottom row, last key) clears all stored Bluetooth bonds
- Top row switches back to layers 0-3

**Battery voltage:** Long-press layer buttons 1 and 2 (the two middle buttons in top row) simultaneously to type the current battery voltage (e.g., "Battery: 3.98V"). Short-press for layer 7. Uses a custom ZMK behavior that reads the battery voltage on-demand with essentially zero ongoing battery cost.
