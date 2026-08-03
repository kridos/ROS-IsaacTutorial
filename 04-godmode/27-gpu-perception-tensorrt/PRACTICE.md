# Practice: GPU-Accelerated Custom Perception (TensorRT)

1. **Compare precision modes.** Build the same ONNX model as an FP32
   engine (skip the FP16 flag in `build_engine.py`) and as an FP16
   engine, then compare `run_inference.py`'s measured latency and
   output values between the two — quantify DEEP_DIVE.md's "FP16 is
   often a near-free speedup" claim on your own hardware.

2. **A real model.** Export an actual trained model (e.g. a small image
   classifier you train or download, converted to ONNX via
   `torch.onnx.export`) instead of the placeholder, and build/run it
   through this chapter's pipeline end to end.

3. **Break engine portability, if you can.** If you have access to two
   different GPU models or TensorRT versions, do demo/README.md's "Try
   it: break engine portability" exercise for real, and document exactly
   what error (or wrong output) you got.

4. **Add real preprocessing.** Fill in the "real preprocessing" comment
   in `tensorrt_inference_node.cpp` — actually resize/normalize incoming
   `sensor_msgs/msg/Image` data into the float layout your model
   expects, rather than leaving it as a documented gap.

5. **Stretch:** measure end-to-end latency including ROS2 message
   transport (publish an image, timestamp when the inference result
   arrives) vs. `run_inference.py`'s pure-inference latency measurement
   — quantify how much of your total pipeline latency is TensorRT
   inference itself vs. everything around it (message serialization,
   the lack of NITROS zero-copy per DEEP_DIVE.md).
