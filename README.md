# Stavropad

A 4x4 macro pad running ZMK firmware on a Nice!Nano v2.

## Features

- 15 normal layers with 15 usable keys each
- Layer switching via dedicated modifier key (bottom-left, key 12)
- All hotkey layers send RCtrl+Shift+Cmd + a character (for use as global hotkeys)
- Idle deep sleep enabled; wakes on any key press after inactivity
- 15 Bluetooth profiles via dedicated Bluetooth control screen

## Layer access

Hold the modifier key (bottom-left, key 12) to activate the layer switcher. While holding key 12:

**Normal layers (tap):**
- Tap keys 0-11 to switch to normal layers 0-11.
- Tap keys 13-15 to switch to normal layers 12-14.

**Special layers (hold for 1 second, ordered by increasing danger):**
- Key 0: Type battery voltage (for example: "Battery: 3.98V").
- Key 1: Open Bluetooth control.
- Key 2: Enter bootloader mode.

## Layers

See [KEYMAPS.md](KEYMAPS.md) for visual layer references.

```
Key positions:
 0   1   2   3
 4   5   6   7
 8   9  10  11
12  13  14  15
```

**Normal layers**

- **Layer 0**: Hotkeys (numbers and symbols)
- **Layer 1**: Hotkeys (letters A-P)
- **Layer 2**: Hotkeys (letters Q-Z and punctuation)
- **Layer 3**: Hotkeys (function keys and modifiers)
- **Layer 4**: Text macros
- **Layer 5**: Media controls
- **Layer 6**: Mouse control
- **Layer 7**: Gaming
- **Layer 8**: Numpad
- **Layer 9**: Cluster
- **Layer 10**: OnShape Sketch Tools
- **Layers 11-14**: Placeholder layers

**Special layers**

- **Bluetooth control**: Select Bluetooth profiles 0-14 and clear bonds.
- **Battery voltage**: Types a voltage readout.
- **Bootloader**: Enters bootloader mode.

**OnShape sublayers (accessed from Layer 10)**

- **Layer 18**: OnShape Constraints (hold Enter)
- **Layer 19**: OnShape Features (hold Esc)
## Customize

Edit `config/stavropad.keymap`.

## Building

Run the build script:

```bash
./build.sh        # PCB version (default)
./build.sh -v 1   # Hand-wired version
./build.sh -v 2   # PCB version
```

This uses Docker to build the firmware. Output is `build/zephyr/zmk.uf2`.
The custom shield and keymap live under `config/boards/shields/stavropad`.

Pin mappings for each version are in `pins_v1.overlay` and `pins_v2.overlay`.

## Flashing

1. Put the board in bootloader mode (hold modifier + hold key 2 for 1 second).
2. Copy `build/zephyr/zmk.uf2` to the USB mass storage device that appears.
