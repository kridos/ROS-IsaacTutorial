# Demo: Generate a Small Synthetic Dataset

## Prerequisites

Same as Chapter 13 (Isaac Sim 4.x, NVIDIA GPU). No extra installs —
Replicator ships as part of Isaac Sim.

## How to run

```bash
~/.local/share/ov/pkg/isaac-sim-<version>/python.sh generate_dataset.py
```

## Expected output

```
Captured frame 1/20
Captured frame 2/20
...
Captured frame 20/20
Done. 20 frames written to: /path/to/demo/output
```

## Inspect the dataset

```bash
ls output/
```

Expected: a folder structure containing 20 RGB images
(`rgb_0000.png` ... `rgb_0019.png`) and matching bounding-box annotation
files (`bounding_box_2d_tight_0000.npy`/`.json`, one per frame,
BasicWriter's default naming — exact filenames may vary slightly by
Isaac Sim version).

Open a few of the RGB images. Expected: a cube in a different position,
rotation, and lighting in each one — confirming the randomizer is
actually varying the scene between captures, not producing 20 copies of
the same render (see DEEP_DIVE.md's common pitfall on diversity vs. raw
image count).

## Try it: check label correctness

Load one image and its matching bounding-box annotation file (e.g. with
a short throwaway script using `numpy`/`json` plus `PIL` to draw the box
on the image) and confirm the box actually surrounds the cube. This is a
good habit for any synthetic dataset before using it for training — a
consistently-offset or misaligned bounding box usually means an
annotator/render-product configuration mistake, not a training problem
you'd otherwise only discover after wasting a training run on bad labels.

## Try it: increase diversity

Edit `NUM_FRAMES` to `50`, and widen the position/rotation distribution
ranges in `randomize_scene()` — re-run and compare how much more varied
the resulting images look, a hands-on look at the domain randomization
concept from DEEP_DIVE.md.
