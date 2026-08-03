#!/usr/bin/env python3
"""Loads a TensorRT engine built by build_engine.py and runs inference on
a sample random input, printing the output and measured inference
latency — the RUNTIME phase from DEEP_DIVE.md (fast, repeated, as
opposed to build_engine.py's slow one-time BUILD phase).

Usage: python3 run_inference.py <model.engine>
"""

import sys
import time

import numpy as np
import tensorrt as trt
import pycuda.driver as cuda
import pycuda.autoinit  # noqa: F401  (initializes the CUDA context as an import side effect)

TRT_LOGGER = trt.Logger(trt.Logger.WARNING)
NUM_WARMUP_RUNS = 5
NUM_TIMED_RUNS = 20


def load_engine(engine_path: str):
    with open(engine_path, "rb") as f:
        runtime = trt.Runtime(TRT_LOGGER)
        return runtime.deserialize_cuda_engine(f.read())


def main():
    if len(sys.argv) != 2:
        print("Usage: run_inference.py <model.engine>")
        sys.exit(1)
    engine_path = sys.argv[1]

    engine = load_engine(engine_path)
    context = engine.create_execution_context()

    # Allocate GPU input/output buffers ONCE here, not per-inference-call
    # — see DEEP_DIVE.md on why per-message allocation would waste most
    # of TensorRT's speed advantage. This demo has one input, one output
    # tensor for simplicity; a real model may have more of each.
    input_shape = engine.get_tensor_shape(engine.get_tensor_name(0))
    output_shape = engine.get_tensor_shape(engine.get_tensor_name(1))

    input_host = np.random.randn(*input_shape).astype(np.float32)
    output_host = np.empty(output_shape, dtype=np.float32)

    input_device = cuda.mem_alloc(input_host.nbytes)
    output_device = cuda.mem_alloc(output_host.nbytes)
    stream = cuda.Stream()

    context.set_tensor_address(engine.get_tensor_name(0), int(input_device))
    context.set_tensor_address(engine.get_tensor_name(1), int(output_device))

    def infer_once():
        cuda.memcpy_htod_async(input_device, input_host, stream)
        context.execute_async_v3(stream_handle=stream.handle)
        cuda.memcpy_dtoh_async(output_host, output_device, stream)
        stream.synchronize()

    # Warmup runs: the first few inference calls are often slower due to
    # one-time GPU kernel selection/caching overhead — excluded from the
    # latency measurement below so the reported number reflects steady-state
    # performance, not startup cost.
    for _ in range(NUM_WARMUP_RUNS):
        infer_once()

    latencies_ms = []
    for _ in range(NUM_TIMED_RUNS):
        start = time.perf_counter()
        infer_once()
        latencies_ms.append((time.perf_counter() - start) * 1000)

    print(f"Output shape: {output_host.shape}")
    print(f"Output sample values: {output_host.flatten()[:5].round(3)}")
    print(f"Mean inference latency over {NUM_TIMED_RUNS} runs: {np.mean(latencies_ms):.3f} ms")


if __name__ == "__main__":
    main()
