# Chapter 28: Capstone — Autonomous Mobile Manipulator

## What this is

This chapter doesn't teach a new concept — it integrates the
curriculum's major threads into one mission: a mobile robot with an arm
mounted on it navigates to a location, perceives a target object, picks
it up, navigates to a second location, and places it down.

## Why it matters

Every earlier chapter built one capability in relative isolation:
navigation alone (Chapter 11/17), manipulation alone (Chapter 12/18),
perception alone (Chapter 9/15). Real robots need these working
*together*, at the same time, on the same robot, coordinated — which
surfaces integration problems none of the individual chapters needed to
face (an extended arm changing the robot's navigable footprint, for
instance). This is genuinely a different, harder problem than any single
capability, and is where a lot of real-world robotics engineering effort
actually goes.

## Where this fits

This is the curriculum's final chapter — it draws on Chapter 7 (mobile
base), Chapter 8 (TF, now with a moving root for the arm), Chapter 11/17
(Nav2), Chapter 12/18 (MoveIt2), and notes where Chapter 15/16/27's real
perception would plug in, rather than teaching anything new on its own.

## What the demo shows

A combined mobile-base-plus-arm robot running Nav2 and MoveIt2
simultaneously, executing a full navigate -> detect -> pick -> navigate
-> place mission end to end, coordinated by a single mission node that
sequences each stage and explicitly manages the arm-stow-before-navigate
integration detail DEEP_DIVE.md describes.
