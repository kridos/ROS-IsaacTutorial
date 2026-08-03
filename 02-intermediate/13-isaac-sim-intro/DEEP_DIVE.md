# Chapter 13 Deep Dive: Isaac Sim Intro

## USD: the format everything is built on

**USD** (Universal Scene Description, originally from Pixar) is the file
format and in-memory scene representation Isaac Sim and Omniverse are
built around. Conceptually it plays the same role Chapter 7's SDF played
for Gazebo — describing a scene of objects — but USD is a much more
general, industry-wide standard (used across VFX, film, and design tools
far beyond robotics), which is part of why NVIDIA built Isaac Sim on top
of it rather than a robotics-specific format: it gets to reuse a huge
existing ecosystem of tools, renderers, and content.

Key vocabulary:
- **Stage**: the currently loaded/edited USD scene — the Isaac Sim
  equivalent of "the world" in Gazebo. Everything you spawn or simulate
  exists on the stage.
- **Prim** (short for "primitive"): a single node in the USD scene
  graph — everything on the stage is a prim, arranged in a tree (a
  robot becomes a tree of prims: one per link, roughly, mirroring the
  URDF's link tree from Chapter 5). "Prim" here doesn't mean geometric
  primitive specifically — a whole robot, a light, or a physics setting
  can each be a prim.
- **Layer**: USD supports composing a scene from multiple layered files
  (for non-destructive editing — a base layer plus override layers) —
  more relevant to advanced Omniverse workflows than this intro chapter,
  worth knowing the term exists.

## Importing a URDF

The **URDF Importer** extension reads your existing URDF (the exact same
file format from Chapter 5/7 — no format conversion needed) and
generates the corresponding USD prims: one per link, with joints
translated into USD's physics joint schema (`UsdPhysics.RevoluteJoint`
and friends), preserving the same parent/child kinematic structure. This
means everything you already know about designing a URDF (Chapter 5)
carries over directly — Isaac Sim doesn't require a different robot
description language, just a different *simulator* consuming the same
one.

## The Isaac Sim Python API

Beyond ROS2 (which is a separate layer, covered in Chapter 14), Isaac
Sim has its own Python API for controlling the simulator directly —
package name `isaacsim.core` in current Isaac Sim releases (`omni.isaac.core`
in older ones; check your installed version). This is what
`import_and_spawn.py` uses in this chapter: creating a `World`, invoking
the URDF importer, stepping physics — all without ROS2 involved at all.
Chapter 14 layers ROS2 on top of this, but it's worth understanding this
lower-level API exists and works independently, the same way Gazebo's
own scripting/plugin API exists independently of `ros_gz_bridge`.

## Extensions

Isaac Sim's functionality — including the URDF importer and (Chapter 14)
the ROS2 bridge — is organized into **extensions**, a plugin system you
enable/disable as needed rather than always having everything loaded.
`import_and_spawn.py` explicitly enables the URDF importer extension
before using it; forgetting this step is the single most common reason a
first Isaac Sim script fails with an import error that looks like a
missing-package problem but is actually a not-yet-enabled extension.

## Common pitfall: unit and scale mismatches

URDF always uses **meters**. Some 3D meshes (especially ones authored
for VFX/design tools, given USD's origins) are exported in centimeters
or millimeters. If a URDF references a mesh authored in the wrong unit,
the imported robot can appear absurdly large or small, or — more
confusingly — visually fine but with collision geometry at the wrong
scale, causing odd physics behavior that doesn't match what you see.
PhysX (Isaac Sim's physics engine) is also stricter than Gazebo's
physics engine about needing valid, non-degenerate `<inertial>` values
on every link — a link with all-zero or missing inertia that Gazebo
silently tolerated may cause Isaac Sim's physics to behave unpredictably
or reject the link entirely. If an imported robot looks visually correct
but "explodes" or drifts oddly under physics, check inertial values
before suspecting anything else.
