# Agent instructions

After every change to the keymap or configuration:

1. Update `README.md` to reflect any changes to layers, combos, or features.
2. Run `./build.sh` to confirm the firmware builds successfully.

## Layer switching architecture

**Normal layer switching:**
- Hold key 12 (bottom-left) to activate the layer switcher.
- While holding key 12, tap any other key to immediately switch to the corresponding user layer.

**Special layer switching:**
- While holding key 12, hold another key for 1 second to access special functions.
- Special functions are assigned to keys starting from key 0 and grow sequentially.

**Key 12 on each layer:**
- Key 12 has a dual function on every layer: tap performs a layer-specific action, hold activates the layer switcher.
- The tap action should be something useful but not something that encourages holding (to avoid accidental layer switching).

## Layer discussions

When discussing layers, treat key 12 (bottom-left) like any other key. Only mention its hold-to-switch-layer function when layer switching is specifically being discussed. When talking about macros or tap actions, just show what it sends on tap.

## Key 12 warnings

When proposing or assigning a function to key 12 that might cause the user to hold it down (e.g., drag lock, toggle behaviors, mouse movement, or anything that encourages sustained pressing), warn the user that this could accidentally trigger the layer switcher.

Note that you shouldn't avoid assigning shortcuts to key 12 altogether (since it can be tapped), only avoid assigning shortcuts that might be *held*.

## Utilities

- `misc/render_kle.py`: Renders KLE JSON files to PNG images using kle-render.herokuapp.com. Usage: `python3 misc/render_kle.py <input.json> [output.png]`
