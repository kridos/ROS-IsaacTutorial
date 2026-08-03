# Chapter 17: Advanced Nav2 — Custom Behavior Trees

## What this is

Chapter 11 mentioned that Nav2's `bt_navigator` sequences navigation
using a behavior tree, without going into what that tree actually looks
like or how to change it. This chapter opens that up: behavior tree
fundamentals, reading Nav2's default tree, and building your own custom
tree using Nav2's existing building blocks arranged differently.

## Why it matters

The default behavior tree's recovery strategy (what to do when
navigation gets stuck) is one reasonable choice, not the only one. A
robot in a particular environment or task might need a different
strategy — more patient retries, a different obstacle-clearing sequence,
custom conditions specific to your robot. Behavior trees are how Nav2
exposes that customization without you touching Nav2's own source code.

## Where this fits

Directly extends Chapter 11's Nav2 stack — same robot, same map, same
`NavigateToPose` action interface — swapping only which behavior tree
XML `bt_navigator` loads.

## What the demo shows

A custom behavior tree that tries normal navigation first, and on
failure runs a distinctly more patient recovery sequence (wait longer,
back up further, retry) than Nav2's stock tree — loaded into the Chapter
11 stack and exercised with a goal sent the same way Chapter 11 did.
