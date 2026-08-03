# Demo: TensorRT — Build, Run, and a ROS2 Inference Node

## Prerequisites

- NVIDIA GPU with TensorRT installed (commonly via the CUDA/TensorRT
  install bundled with JetPack on Jetson, or a standalone TensorRT
  install on a desktop RTX GPU — see NVIDIA's TensorRT install docs).
- Python: `pip install tensorrt pycuda numpy onnx` in an isolated venv.
- A small ONNX model to build from — for a quick placeholder, export any
  trivial PyTorch model with `torch.onnx.export(...)`; the exact model
  doesn't matter for this demo, only that it produces a valid ONNX file.

## Part 1: Build the engine

```bash
python3 python/build_engine.py placeholder_model.onnx model.engine
```

Expected output:

```
FP16 supported on this platform — enabling FP16 precision
Building engine (this is the slow, one-time BUILD step)...
Engine written to: model.engine
```

(The build step can genuinely take a minute or more even for a small
model — this is expected, see DEEP_DIVE.md's build-vs-runtime split.)

## Part 2: Run inference and measure latency

```bash
python3 python/run_inference.py model.engine
```

Expected output:

```
Output shape: (1, 10)
Output sample values: [ 0.123 -0.456  0.789 -0.234  0.567]
Mean inference latency over 20 runs: 0.412 ms
```

(Exact latency depends heavily on your GPU and the model's size — the
key thing to notice is that it's fast and consistent run to run, after
the warmup runs are excluded.)

## Part 3: Build and run the C++ ROS2 node

```bash
cp -r cpp ~/ros2_ws/src/tensorrt_inference_demo
cd ~/ros2_ws
colcon build --packages-select tensorrt_inference_demo
source install/setup.bash
ros2 run tensorrt_inference_demo tensorrt_inference_node --ros-args -p engine_path:=/path/to/model.engine
```

In another terminal, publish a dummy image to trigger inference (a real
setup would have an actual camera/Gazebo/Isaac Sim source publishing
`/camera/image_raw`, per Chapter 9):

```bash
ros2 topic pub /camera/image_raw sensor_msgs/msg/Image "{height: 224, width: 224}" --once
```

Expected: the node logs no errors, and:

```bash
ros2 topic echo /perception/result --once
```

shows a `Float32MultiArray` with 10 values — confirming the C++ node
successfully ran inference through the loaded engine and published a
result, exercising the same allocate-once/infer-per-message pattern
DEEP_DIVE.md describes.

## Try it: break engine portability on purpose

If you have access to two different GPU models, build the engine on one
and attempt to load it (Part 2 or Part 3) on the other. Expected:
either a load failure or clearly degraded/incorrect output — a direct,
hands-on look at DEEP_DIVE.md's engine-portability pitfall, and why
engines get rebuilt per target platform rather than copied like an ONNX
file would be.
