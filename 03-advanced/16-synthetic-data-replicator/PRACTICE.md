# Practice: Synthetic Data Generation (Replicator)

1. **Add a second object.** Extend `generate_dataset.py` to place a
   second, differently-shaped object (a sphere) alongside the cube, both
   semantically tagged, and confirm the bounding-box annotations capture
   both objects per frame.

2. **Randomize the camera too.** Add camera position/look-at
   randomization (not just the cube and light) using
   `rep.distribution.uniform`, so the viewing angle varies between
   captures as well — directly addressing DEEP_DIVE.md's "randomize
   more variables" advice.

3. **Add segmentation.** Attach the `semantic_segmentation` annotator
   alongside `rgb` and `bounding_box_2d_tight`, and update the writer's
   `initialize()` call to save it too. Open one output mask and confirm
   it highlights the cube's exact pixels.

4. **Measure diversity, quantitatively.** Generate two datasets — one
   with the demo's default randomization ranges, one with much narrower
   ranges (near-identical scenes) — and write a short script comparing
   pixel-value variance across each dataset's images, to put a number on
   DEEP_DIVE.md's "quantity without diversity" pitfall.

5. **Stretch:** wire the generated dataset into a trivial training loop
   (a tiny classifier distinguishing "cube visible" vs. not, or similar)
   using any ML framework you're comfortable with — close the loop from
   "synthetic data" to "a model trained on it," even at toy scale.
