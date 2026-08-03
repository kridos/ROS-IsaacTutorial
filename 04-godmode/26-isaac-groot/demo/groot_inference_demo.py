#!/usr/bin/env python3
"""Loads a released GR00T checkpoint, constructs one observation (a
camera image plus a text instruction), runs a single inference step, and
prints the resulting action's shape and values.

This is deliberately a single-inference-step script, NOT a fine-tuning
pipeline (see DEEP_DIVE.md — fine-tuning is its own substantial
undertaking, out of scope for one demo chapter). The point here is
establishing the input/output shape of working with a GR00T model: what
goes in, what comes out.

Run with the Isaac GR00T package's own Python environment — see
demo/README.md for install/version-specific setup, which changes as
GR00T's release cadence progresses.
"""

import numpy as np
import torch
from PIL import Image

from gr00t.model.policy import Gr00tPolicy
from gr00t.data.embodiment_tags import EmbodimentTag


def load_sample_observation(image_path: str, instruction: str) -> dict:
    """Builds one observation dict in the shape a GR00T policy expects:
    an RGB image plus a natural-language task instruction (see
    DEEP_DIVE.md's vision-language-action structure)."""
    image = Image.open(image_path).convert("RGB")
    image_array = np.array(image)

    return {
        "video": {"front_camera": image_array[np.newaxis, ...]},  # add a time-step axis
        "language_instruction": instruction,
    }


def main():
    # EmbodimentTag identifies which robot embodiment (joint layout,
    # action space) this inference call targets — GR00T checkpoints are
    # trained across multiple embodiments and need to know which one
    # you're asking it to act as, per DEEP_DIVE.md's common pitfall on
    # embodiment-specific adaptation.
    policy = Gr00tPolicy(
        model_path="nvidia/GR00T-N1-2B",  # a released checkpoint identifier — exact
                                            # name/version changes as NVIDIA releases
                                            # new GR00T checkpoints; check current docs
        embodiment_tag=EmbodimentTag.NEW_EMBODIMENT,
        device="cuda",
    )

    observation = load_sample_observation(
        image_path="sample_scene.jpg",
        instruction="pick up the red block",
    )

    print(f"Instruction: '{observation['language_instruction']}'")
    print(f"Input image shape: {observation['video']['front_camera'].shape}")

    with torch.no_grad():
        action = policy.get_action(observation)

    # action is a dict of action components (e.g. arm joint targets,
    # gripper command) — exact keys depend on the embodiment/checkpoint,
    # printed generically here rather than assuming a fixed robot's
    # specific action layout.
    print("Predicted action:")
    for key, value in action.items():
        value_array = np.asarray(value)
        print(f"  {key}: shape={value_array.shape}  values={value_array.round(3)}")


if __name__ == "__main__":
    main()
