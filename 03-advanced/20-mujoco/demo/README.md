# Demo: MuJoCo — Direct Physics Stepping

## Prerequisites

MuJoCo's Python bindings are a plain pip package — no GPU, no ROS2, no
simulator install required. Use an isolated environment rather than your
system Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install mujoco
```

## How to run

```bash
python3 run_sim.py
```

## Expected output

```
t=0.00s  joint1=   0.0deg  joint2=   0.0deg
t=0.50s  joint1= 183.3deg  joint2= 118.8deg
t=1.00s  joint1= 180.3deg  joint2= 115.1deg
t=1.50s  joint1= 180.3deg  joint2= 115.1deg
t=2.00s  joint1= 180.3deg  joint2= 115.1deg
t=2.50s  joint1= 180.2deg  joint2= 115.1deg
t=3.00s  joint1= 180.1deg  joint2= 115.2deg
t=3.50s  joint1= 116.2deg  joint2= 115.1deg
t=4.00s  joint1=-180.3deg  joint2= 115.3deg
t=4.50s  joint1=-180.3deg  joint2= 115.1deg
Done.
```

(Verified output from an actual run — your exact numbers may differ
slightly with a different MuJoCo version, but the shape should match.)

Notice `joint2` climbs to `115.1deg` and then holds there for most of the
run — that's `simple_arm.xml`'s `range="-115 115"` joint limit doing its
job: the applied sinusoidal torque keeps pushing outward, but the joint
physically can't rotate past its configured limit, so it sits pinned
against the stop rather than continuing past it. `joint1` (no limit
tighter than a full rotation) swings more freely, crossing past 180
degrees (wrapping to negative values, since angles here aren't clamped
to a 0-360 range).

## Try it: remove the joint limit

Edit `simple_arm.xml`, remove `range="-115 115"` from `joint2`'s
definition (or widen it substantially), and re-run. Expected: `joint2`
should now swing back and forth following the sinusoidal torque more
freely, instead of pinning at a fixed value — a direct look at how a
joint limit changes the simulated behavior.

## Try it: read velocity too

Add a line printing `data.qvel[0]`, `data.qvel[1]` alongside the
position printout — direct array access, same pattern as `data.qpos`,
per DEEP_DIVE.md's description of MuJoCo's API style.
