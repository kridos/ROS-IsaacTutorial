# Chapter 27: GPU-Accelerated Custom Perception (TensorRT)

## What this is

**TensorRT** is NVIDIA's inference optimization library — it takes a
trained neural network and compiles it into a highly optimized,
hardware-specific execution plan for fast inference, the same
performance-critical role NITROS (Chapter 15) leans on for Isaac ROS's
own built-in perception pipelines.

## Why it matters

Chapter 15's Isaac ROS packages are pre-built, GPU-accelerated
perception nodes NVIDIA maintains. A model *you* trained yourself — a
custom object detector, a custom classifier — doesn't get that
pre-built acceleration automatically; TensorRT is how you give your own
trained model the same kind of optimized, fast inference path.

## Where this fits

Builds on Chapter 15's NITROS/GPU-perception concepts and Chapter 24's
"trained model -> checkpoint -> inference" pattern, applied here to
building and deploying an optimized inference engine rather than running
a training loop.

## What the demo shows

Building a TensorRT engine from a small ONNX model, running inference
with it in Python and measuring latency, and — the chapter's C++ demo,
per this curriculum's language policy — a ROS2 node wrapping the same
engine to run inference on incoming image messages.
