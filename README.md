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
- Layers 4-17: Activated by pressing multiple layer buttons simultaneously
  - Layer 4 (buttons 0+1): Text macros - "nootropia", "bro", "type shit", "don't do dis shit", "respect", "and shit", "failing to prepare is preparing to fail", "exelixi", "eimai panta etoimos", "read a book", "to great reset", "open the fuckin pita"
  - Layer 5 (buttons 0+2): Media controls - Bri-/Bri+/Shuffle/Repeat, Vol-/Vol+/Mute/Search, Prev/Play-Pause/Stop/Next
  - Layer 6 (buttons 0+3 short-press): Mouse control - L/M/R clicks on left column, 8-directional movement on right 3x3, hold center for scroll
  - Layer 7 (buttons 1+2 short-press): URL macro - types "https://www.stavros.io" repeatedly
  - Layer 8 (buttons 1+3): URL macro - types "https://www.stavros.io" repeatedly
  - Layer 9 (buttons 2+3): URL macro - types "https://www.stavros.io" repeatedly
  - Layer 10 (buttons 0+1+2): URL macro - types "https://www.stavros.io" repeatedly
  - Layer 11 (buttons 0+1+3): URL macro - types "https://www.stavros.io" repeatedly
  - Layer 12 (buttons 0+2+3): Gaming layer - ESC/Q/W/E, Shift/A/S/D, Ctrl/Alt/Enter/Space
  - Layer 13 (buttons 1+2+3): Numpad - 7-8-9/+, 4-5-6/Enter, 1-2-3/0
  - Layer 14 (all 4 buttons tap): QWERTY - Q/W/E/R, A/S/D/F, Z/X/C/V
  - Layer 15 (all 4 buttons hold 1s): Bluetooth control layer (see below)
  - Layer 17 (hold center key on layer 6): Scroll sub-layer - scroll up/down/left/right while held

## Building

Run the build script:

```bash
./build.sh        # PCB version (default)
./build.sh -v 1   # Hand-wired version
./build.sh -v 2   # PCB version
```

This uses Docker to build the firmware. Output is `build/zephyr/zmk.uf2`.
The custom shield and keymap live under `config/boards/shields/macropad`.

Pin mappings for each version are in `pins_v1.overlay` and `pins_v2.overlay`.

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
