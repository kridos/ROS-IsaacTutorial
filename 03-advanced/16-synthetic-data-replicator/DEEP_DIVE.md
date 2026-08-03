# Chapter 16 Deep Dive: Isaac Sim Replicator

## Domain randomization

A model trained on renders of one exact scene (same lighting, same
textures, same camera angle every time) will overfit to that scene's
specific visual quirks rather than learning the general appearance of
the object it's supposed to detect — it might, for instance, learn "this
object is whatever's in the center of a brightly-lit gray room," which
fails completely on a real photo. **Domain randomization** is the fix:
vary lighting intensity/color, textures/materials, object poses, camera
angle and distance, and background, across renders, so no single
irrelevant visual detail is a reliable signal the model can (over)fit
to. Replicator provides randomizer functions (`rep.randomizer.*`) for
exactly this — attaching randomization to object pose, light parameters,
material assignment, and more, each re-rolled on every capture.

## Annotators

An **annotator** is a specific labeled output you attach to a camera (a
"render product" in Replicator's terminology): `rgb` (the plain image),
`bounding_box_2d_tight`/`bounding_box_2d_loose` (2D boxes around each
object), `semantic_segmentation` (per-pixel class labels),
`instance_segmentation` (per-pixel object-instance labels, distinguishing
two objects of the same class), `distance_to_camera` (depth). You attach
whichever annotators your downstream training task needs — object
detection needs bounding boxes, segmentation needs the segmentation
annotator, and so on; attaching more annotators than you need just slows
down each capture for no benefit.

## Writers

A **writer** takes annotator output and saves it to disk in a specific
format. `BasicWriter` (used in this chapter's demo) writes a generic
folder structure of images plus JSON/NumPy annotation files — good for a
first look at what's being generated. Format-specific writers (COCO,
KITTI) exist for producing data directly in the exact format a specific
training framework or existing dataset convention expects, saving you
from writing your own conversion script from `BasicWriter`'s generic
output.

## The render-and-capture loop

Structurally, a Replicator script is:

1. Set up the scene (load/place objects, set up a camera and render
   product, attach annotators and a writer).
2. Loop N times: trigger randomizers (re-roll object pose, lighting,
   etc.), trigger a render, capture the annotator outputs for that frame
   via the writer.

Each iteration through step 2 produces one labeled training example —
this chapter's demo runs this loop directly to make the structure
concrete, though large-scale dataset generation would typically run many
more iterations, often across multiple parallel simulation instances,
than a learning demo needs.

## Common pitfall: quantity without diversity

Randomizing only *some* relevant variables — say, object position but
not lighting or texture — can produce a dataset that looks large by
image count (thousands of files) but is actually low-diversity: every
image still shares the same lighting and material, so a model trained on
it can overfit to those unchanging details just as easily as it would
overfit to a single static scene, just with more copies of the same
underlying bias. The fix isn't "generate more images," it's "randomize
more of the variables that shouldn't matter to the task" — a smaller
dataset with genuine variation in lighting/texture/pose/background
usually trains a more robust model than a much larger one lacking that
variety.
