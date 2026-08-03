# Chapter 26: Isaac GR00T Foundation Models

## What this is

**Isaac GR00T** is NVIDIA's foundation model stack for humanoid and
general robot manipulation — a large, pre-trained model that takes in
visual observations (and often language instructions) and outputs robot
actions, meant to be fine-tuned for a specific robot and task rather than
trained from scratch.

## Why it matters

Chapters 23-24 trained a policy entirely from scratch for one narrow
task (balancing a pole). That works, but needs a full training run per
task. A foundation model flips this: train one large, broadly-capable
model once (on large, diverse data — including synthetic data of the
kind Chapter 16 generates), then adapt it to new specific tasks with far
less task-specific data and training time than starting over — the same
pattern that made large language models practical to reuse across many
applications, now applied to robot control.

## Where this fits

The "god mode" end of this curriculum's spectrum: from Chapter 24's
from-scratch, single-task RL policy to a large pre-trained, broadly
capable model. Connects back to Chapter 15 (perception feeding into
action) and Chapter 16 (synthetic data as training fuel for models like
this).

## What the demo shows

A minimal script establishing the shape of working with GR00T: load a
released checkpoint, construct an observation from a camera image plus a
text instruction, run one inference step, and inspect the resulting
action output — deliberately not a full fine-tuning pipeline, which is
its own substantial undertaking beyond a single demo chapter.
