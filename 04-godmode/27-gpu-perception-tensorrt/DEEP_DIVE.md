# Chapter 27 Deep Dive: TensorRT

## Build vs. runtime

TensorRT has two distinct phases:

- **Build**: takes a trained network and produces an **engine** — a
  compiled, hardware-specific optimized execution plan (layer fusion,
  kernel selection tuned for the exact GPU, precision calibration). This
  step is often slow (can take minutes for a real model) and is done
  once, offline, not per-inference.
- **Runtime**: loads a previously-built engine and runs inference with
  it, repeatedly, fast — this is the part that actually runs on the
  robot at operation time.

A built engine is tied to the exact GPU architecture and TensorRT
version it was built on/for — it is **not** portable the way the
original trained model file is (see this chapter's common pitfall).

## ONNX as the bridge format

TensorRT doesn't consume PyTorch/TensorFlow model files directly in the
common workflow — a model is typically first exported to **ONNX** (Open
Neural Network Exchange), a framework-agnostic model interchange format,
and TensorRT's engine builder consumes that ONNX file. This decouples
"which framework you trained in" from "which inference runtime you
deploy with," and ONNX itself is portable across many tools beyond
TensorRT, unlike a built TensorRT engine.

## Precision modes

Building an engine, you choose a precision mode trading numerical
accuracy for speed/memory:

- **FP32** (full 32-bit float precision) — the safest, slowest, most
  memory-hungry option, matching the original trained model's precision
  exactly.
- **FP16** (16-bit half precision) — commonly a substantial speedup with
  negligible accuracy loss on modern GPUs with dedicated FP16 hardware
  support, often described as a "close to free" optimization for that
  reason — this chapter's demo uses FP16.
- **INT8** (8-bit integer, quantized) — the fastest and most
  memory-efficient, but needs a **calibration** step: running a
  representative sample of real input data through the build process so
  TensorRT can choose quantization scales that preserve accuracy — INT8
  without proper calibration can degrade accuracy substantially,
  unlike FP16's comparatively low-risk trade-off.

## Wrapping an engine in a ROS2 node

At inference time, a TensorRT-based ROS2 node typically: allocates
GPU input/output memory buffers **once** at node startup (allocation is
comparatively expensive; doing it per-message would waste most of the
speed TensorRT was supposed to provide), then per incoming message,
copies the input data into the GPU buffer, runs inference
(`context.execute_v2(...)` or similar, depending on TensorRT API
version), copies the result back out, and publishes it. This chapter's
C++ demo (`tensorrt_inference_node.cpp`) follows exactly this shape.

Worth noting explicitly: a node built this way, by hand, does **not**
automatically get NITROS's zero-copy transport (Chapter 15) — NITROS
requires implementing a NITROS-compatible node interface specifically,
which this simple hand-written wrapper doesn't do. For a single node,
the CPU-GPU copy overhead NITROS exists to avoid is a real but often
acceptable cost; it becomes more consequential specifically when
chaining multiple GPU-accelerated nodes together, per Chapter 15's
original NITROS discussion.

## Common pitfall: engine portability

An engine file built on one GPU model/TensorRT version is not
guaranteed to load correctly — or to load at all — on a different GPU
model or TensorRT version. Unlike an ONNX file (portable, framework/
hardware-agnostic), a built engine is a compiled artifact specific to
its build environment. Copying a pre-built `.engine` file from a dev
workstation to a robot's different Jetson/GPU hardware, or upgrading
TensorRT without rebuilding, is a common deployment mistake — the fix
is straightforward (always rebuild the engine on, or matching, the
actual target deployment hardware/TensorRT version) but easy to overlook
if you're used to portable model files from earlier chapters' checkpoint
formats (Chapters 24-26), which don't have this constraint.
