# Demo: Import a URDF into Isaac Sim

## Prerequisites

- NVIDIA GPU with a recent driver (check NVIDIA's Isaac Sim
  documentation for the exact minimum — RTX-capable is required for
  full rendering, though this demo runs headless).
- Isaac Sim 4.x installed (via Omniverse Launcher, or the standalone
  pip/container distribution — see NVIDIA's Isaac Sim install docs for
  current options, this changes between releases).
- `xacro` available on your system `PATH` (installed in Chapter 1/5 as
  part of ROS2 — Isaac Sim itself doesn't need ROS2 installed for this
  chapter, only the `xacro` CLI tool to expand the Xacro file).

## How to run

Isaac Sim ships its own Python environment bundling all its dependencies
— you run scripts with its `python.sh` (Linux) rather than your system
`python3`:

```bash
~/.local/share/ov/pkg/isaac-sim-<version>/python.sh import_and_spawn.py
```

(Exact install path varies by Isaac Sim version/install method — check
your Isaac Sim installation directory for `python.sh` if this path
doesn't match.)

## Expected output

```
Imported URDF -> USD at: /path/to/demo/simple_diffdrive.usd
step=0 position=(0.000, 0.000, 0.100)
step=30 position=(0.000, 0.000, 0.052)
step=60 position=(0.000, 0.000, 0.050)
step=90 position=(0.000, 0.000, 0.050)
step=120 position=(0.000, 0.000, 0.050)
step=150 position=(0.000, 0.000, 0.050)
Done.
```

The Z position dropping from `0.100` toward roughly `0.050` (the wheel
radius, per `simple_diffdrive.urdf.xacro`'s `wheel_radius` property) and
then settling confirms the robot fell under gravity and came to rest on
the ground plane — physics is actually being simulated, not just a
static import.

## If the import fails

- `ModuleNotFoundError` for any `isaacsim.*` or `omni.*` module: you're
  running with system `python3` instead of Isaac Sim's `python.sh` — see
  "How to run" above.
- An error mentioning the URDF importer extension not found: it may need
  enabling once via the Isaac Sim GUI's Extension Manager the first time
  (Window -> Extensions, search "URDF") before `enable_extension` can
  find it — a one-time setup step on a fresh Isaac Sim install.
- A robot that imports but looks the wrong size: see DEEP_DIVE.md's
  common pitfall on unit mismatches (shouldn't affect this specific demo
  robot, since Chapter 7's URDF is already authored in meters with no
  external meshes, but worth knowing for any URDF you bring in later).
