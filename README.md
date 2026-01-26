# Macropad

A 4x4 macro pad running ZMK firmware on a Nice!Nano v2.

## Features

- 15 layers (0-14), each with 15 usable keys
- Layer switching via dedicated modifier key (bottom-left, key 12)
- All hotkey layers send RCtrl+Shift+Cmd + a character (for use as global hotkeys)
- Idle deep sleep enabled; wakes on any key press after inactivity
- 14 Bluetooth profiles via dedicated BT control layer

## Layer switching

Hold the modifier key (bottom-left, key 12) to activate the layer switcher (layer 16). While holding key 12:

**Normal switching (tap):**
- Tap keys 0-11 to switch to layers 0-11.
- Tap keys 13-15 to switch to layers 12-14.
- This gives you 15 user layers (0-14) accessible via immediate tap.

**Special functions (hold for 1 second, ordered by increasing danger):**
- Key 0: Type battery voltage (e.g., "Battery: 3.98V").
- Key 1: Switch to Bluetooth control layer.
- Key 2: Enter bootloader mode.

Special functions are assigned starting from key 0 and grow sequentially as new functions are added.

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
- **Layer 7**: Gaming (ESC/1/2/3, Shift/Q/W/E, Ctrl/A/S/D, Tab/Alt/Enter/Space)
- **Layer 8**: Numpad (7-8-9/*, 4-5-6/-, 1-2-3/+, 0/./Enter/)
- **Layer 9**: Cluster (1/2/3/4, Q/W/E/R, A/S/D/F, Z/X/C/V)
- **Layers 10-14**: Placeholder layers
- **Layer 15**: Bluetooth control (profiles 0-13, clear all bonds) - accessed via special function
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

1. Put the board in bootloader mode (hold modifier + hold key 2 for 1 second)
2. Copy `build/zephyr/zmk.uf2` to the USB mass storage device that appears
