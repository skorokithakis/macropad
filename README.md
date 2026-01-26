# Macropad

A 4x4 macro pad running ZMK firmware on a Nice!Nano v2.

## Features

- 15 layers (0-14), each with 15 usable keys
- Layer switching via dedicated modifier key (bottom-left, key 12)
- All hotkey layers send RCtrl+Shift+Cmd + a character (for use as global hotkeys)
- Idle deep sleep enabled; wakes on any key press after inactivity
- 14 Bluetooth profiles via dedicated BT control layer

## Layer switching

Hold the modifier key (bottom-left, key 12) to access layer 16 (layer selection), then tap any key 0-14 to switch to that layer permanently. Tapping key 12 performs a layer-specific action instead.

**Special functions on layer 16** (hold key for 1 second):
- Key 13: Type battery voltage (e.g., "Battery: 3.98V")
- Key 14: Switch to Bluetooth control layer
- Key 15: Enter bootloader mode

## Layers

```
Key positions:
 0   1   2   3
 4   5   6   7
 8   9  10  11
12  13  14  15
```

- **Layer 0**: Hotkeys for numbers and symbols (1-0, - = [ ] \ `)
- **Layer 1**: Hotkeys for letters A-P
- **Layer 2**: Hotkeys for letters Q-Z and punctuation (; ' , . / Space)
- **Layer 3**: Hotkeys for function keys F1-F12 and modifiers (Tab, Esc, Enter, Backspace)
- **Layer 4**: Text macros (16 phrases including "nootropia", "bro", "type shit", "imastan big bottle boys", "afto pou leipei einai to mialo", "aristotelis", "de to paizo magkas")
- **Layer 5**: Media controls (shuffle/repeat/rewind/ff, brightness/print screen, volume/mute, prev/play/stop/next)
- **Layer 6**: Mouse control (scroll up/down and back/forward on left, 8-directional movement, clicks on bottom row, hold center for scroll)
- **Layers 7-11**: URL macro layers (placeholder)
- **Layer 12**: Gaming (ESC/Q/W/E, Shift/A/S/D, Ctrl/Alt/Enter/Space, 1/2/3)
- **Layer 13**: Numpad (7-8-9/+, 4-5-6/Enter, 1-2-3/0, ./- /*)
- **Layer 14**: QWERTY (Q/W/E/R, A/S/D/F, Z/X/C/V, T/G/B)
- **Layer 15**: Bluetooth control (profiles 0-13, clear all bonds)
- **Layer 17**: Scroll sub-layer (activated by holding center key on layer 6)

## Bluetooth control layer

On layer 15:
- Keys 0-13 select Bluetooth profiles 0-13
- Key 15 clears all stored Bluetooth bonds
- Hold modifier + tap any key to return to layers 0-14

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

1. Put the board in bootloader mode (hold modifier + hold key 15 for 1 second)
2. Copy `build/zephyr/zmk.uf2` to the USB mass storage device that appears
