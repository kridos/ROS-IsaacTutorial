#!/usr/bin/env python3
"""Loads simple_arm.xml, steps physics in a loop applying a sinusoidal
torque to each joint motor, and prints joint positions each step —
demonstrating MuJoCo's direct mj_step()/data.qpos programming style from
DEEP_DIVE.md, with no ROS2 involved at all."""

import math
import os

import mujoco

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simple_arm.xml")
SIM_DURATION_SECONDS = 5.0
PRINT_EVERY_N_STEPS = 250  # at timestep=0.002s, this is roughly twice a second


def main():
    # MjModel is the static description (loaded once from the MJCF file);
    # MjData is the mutable state that changes every mj_step() call — see
    # DEEP_DIVE.md for why these are two separate objects rather than one.
    model = mujoco.MjModel.from_xml_path(MODEL_PATH)
    data = mujoco.MjData(model)

    num_steps = int(SIM_DURATION_SECONDS / model.opt.timestep)

    for step in range(num_steps):
        sim_time = step * model.opt.timestep

        # Apply a simple sinusoidal torque to each motor via data.ctrl —
        # direct array assignment, not a published message, per
        # DEEP_DIVE.md's description of MuJoCo's lower-level API style.
        data.ctrl[0] = 2.0 * math.sin(sim_time)       # joint1_motor
        data.ctrl[1] = 1.0 * math.sin(sim_time * 0.5)  # joint2_motor

        # This is the call that actually advances simulated time — nothing
        # else in this script runs physics implicitly (see DEEP_DIVE.md's
        # common pitfall).
        mujoco.mj_step(model, data)

        if step % PRINT_EVERY_N_STEPS == 0:
            # data.qpos is a plain NumPy array, one entry per joint, in
            # model-definition order (joint1, then joint2 here) — read
            # directly, not via any getter method.
            joint1_pos, joint2_pos = data.qpos[0], data.qpos[1]
            print(
                f"t={sim_time:.2f}s  joint1={math.degrees(joint1_pos):6.1f}deg  "
                f"joint2={math.degrees(joint2_pos):6.1f}deg"
            )

    print("Done.")


if __name__ == "__main__":
    main()
