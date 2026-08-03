# Chapter 18: Advanced MoveIt2 — Pick-and-Place Pipelines

## What this is

Chapter 12 planned a single free-form move to one target pose. A real
pick-and-place task is a sequence of several coordinated moves — approach
an object in a straight line, grasp it, retreat, transport it, approach
the place location, release it — with the arm's understanding of what
it's carrying changing partway through.

## Why it matters

Picking something up is one of the most common real manipulation tasks,
and it exposes planning needs Chapter 12 didn't touch: obstacles the arm
must plan around (the table, the object itself before it's grasped),
controlled straight-line motion for the actual grasp/release moments
(you don't want an arbitrary curved path when approaching something to
grab it), and correctly modeling "the arm is now holding this object" so
later planning doesn't collide the held object with something.

## Where this fits

Directly extends Chapter 12's arm, SRDF, and MoveGroupInterface usage —
everything here is additional capability layered on that same
foundation, not a new starting point.

## What the demo shows

The Chapter 12 arm picking up a small block off a table and placing it
at a different location, using the Planning Scene Interface, Cartesian
path planning, and attach/detach — the full sequence DEEP_DIVE.md walks
through, run end to end and logged stage by stage.
