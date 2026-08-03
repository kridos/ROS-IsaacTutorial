# Chapter 16: Synthetic Data Generation (Isaac Sim Replicator)

## What this is

**Replicator** is Isaac Sim's synthetic data generation toolkit: instead
of manually photographing and labeling thousands of real images to train
a perception model (object detector, segmentation network), you render
them from a simulated scene, where the simulator already knows — and can
hand you for free — perfect ground-truth labels (exact bounding boxes,
segmentation masks, depth) for every image.

## Why it matters

Training a useful perception model needs a lot of labeled data, and
manual labeling is slow and expensive. Simulation flips the cost
structure: rendering is comparatively cheap, and labels come for free
from the simulator's own knowledge of the scene, at the cost of needing
your simulated scenes to be realistic and varied enough that a model
trained on them generalizes to real images (see DEEP_DIVE.md's domain
randomization discussion).

## Where this fits

Builds on Chapter 13's Isaac Sim fundamentals (stage, prims) and Chapter
9's sensor concepts (a Replicator camera annotator is conceptually a
much richer version of Chapter 9's simulated camera, producing labels
alongside the image instead of just RGB pixels).

## What the demo shows

A script that places an object in an Isaac Sim scene, randomizes its
pose and the lighting across many iterations, and writes out RGB images
plus bounding-box annotations to a local folder — a small, complete
example of the render-randomize-capture loop real dataset generation
scripts are built from.
