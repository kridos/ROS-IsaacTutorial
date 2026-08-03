# Demo: Isaac GR00T — A Single Inference Step

## Prerequisites

- NVIDIA GPU with substantial VRAM (foundation models are large — check
  the specific released checkpoint's requirements; expect this to need
  meaningfully more GPU memory than any earlier chapter's demos).
- The `gr00t` Python package and a released checkpoint, per NVIDIA's
  Isaac GR00T documentation/repository — install steps and available
  checkpoint names change as NVIDIA releases new versions, so check
  current docs rather than relying on any specific version pinned here.
- A sample image (`sample_scene.jpg` in this directory) showing a scene
  with an object matching the instruction used below (a red block, for
  the default instruction in `groot_inference_demo.py`) — substitute
  your own image and instruction to try a different scene.

## How to run

```bash
python3 groot_inference_demo.py
```

## Expected output

```
Instruction: 'pick up the red block'
Input image shape: (1, 480, 640, 3)
Predicted action:
  arm_joint_targets: shape=(7,)  values=[ 0.12 -0.34  0.02  1.11 -0.05  0.44  0.0 ]
  gripper_command: shape=(1,)  values=[0.8]
```

(Exact action keys/shapes depend on which checkpoint and embodiment tag
you use — this is illustrative of the *shape* of a GR00T policy's
output, not a specific fixed API every version guarantees identically.)

## What to actually look at

This demo doesn't move a robot or verify the action is *correct* — it
establishes that you can load a checkpoint, build a valid observation,
and get back a plausibly-shaped action. Confirming the action is
sensible for your specific robot requires either simulating it (feed the
output into a Chapter 13/14-style Isaac Sim robot and observe) or, per
DEEP_DIVE.md, fine-tuning on your specific embodiment first if the
default output doesn't map sensibly onto your robot's actual joints.

## Beyond this demo

Fine-tuning GR00T on your own robot/task data is the natural next step
this chapter deliberately doesn't cover (see OVERVIEW.md) — check
NVIDIA's Isaac GR00T fine-tuning documentation for the current
recommended workflow, which involves preparing a task-specific dataset
in GR00T's expected format and running its fine-tuning scripts against
the checkpoint loaded here.
