#!/usr/bin/env python3
"""Builds a TensorRT engine from a small ONNX model, using FP16 precision
(see DEEP_DIVE.md) — the BUILD phase, run once, offline, producing a
.engine file run_inference.py then loads for fast repeated inference.

The ONNX model itself is a trivial placeholder classifier (a couple of
small linear layers) — the point of this demo is the TensorRT build
process, not the model's usefulness; swap in your own trained model's
exported ONNX file to use this on something real.

Usage: python3 build_engine.py <input.onnx> <output.engine>
"""

import sys

import tensorrt as trt

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


def build_engine(onnx_path: str, engine_path: str):
    builder = trt.Builder(TRT_LOGGER)

    # EXPLICIT_BATCH is required for ONNX-parsed networks in modern
    # TensorRT versions — the batch dimension is treated as an explicit
    # part of the network's shape rather than implicit.
    network_flags = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    network = builder.create_network(network_flags)

    parser = trt.OnnxParser(network, TRT_LOGGER)
    with open(onnx_path, "rb") as f:
        if not parser.parse(f.read()):
            for i in range(parser.num_errors):
                print(f"ONNX parse error: {parser.get_error(i)}")
            raise RuntimeError(f"Failed to parse ONNX file: {onnx_path}")

    config = builder.create_builder_config()
    # 1GB workspace — the scratch memory TensorRT's optimizer is allowed
    # to use while searching for the fastest valid execution plan; a
    # larger workspace can let it find faster kernels at the cost of
    # more build-time memory usage.
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 30)

    # FP16 precision — see DEEP_DIVE.md: a near-free speedup on modern
    # GPUs with negligible accuracy loss, in contrast to INT8's
    # calibration requirement (not used in this demo).
    if builder.platform_has_fast_fp16:
        config.set_flag(trt.BuilderFlag.FP16)
        print("FP16 supported on this platform — enabling FP16 precision")
    else:
        print("FP16 not supported on this platform — building in FP32 instead")

    print("Building engine (this is the slow, one-time BUILD step)...")
    serialized_engine = builder.build_serialized_network(network, config)
    if serialized_engine is None:
        raise RuntimeError("Engine build failed")

    with open(engine_path, "wb") as f:
        f.write(serialized_engine)
    print(f"Engine written to: {engine_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: build_engine.py <input.onnx> <output.engine>")
        sys.exit(1)
    build_engine(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
