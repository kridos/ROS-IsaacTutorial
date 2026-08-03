# Chapter 17 Deep Dive: Advanced Nav2 — Custom Behavior Trees

## Behavior tree fundamentals

A **behavior tree** is a way of composing simple building blocks into
complex, reactive logic. Nav2 uses BT.CPP (a C++ behavior tree library),
described in XML. The core node types you'll actually read and write:

- **Sequence**: runs each child in order, left to right. If a child
  fails, the whole Sequence fails immediately (later children don't
  run) — "do this, then this, then this, and stop if any step fails."
- **Fallback** (also called Selector in some BT literature, but Nav2's
  XML uses `<Fallback>`): tries each child in order, and succeeds as
  soon as one child succeeds. "Try this; if it fails, try this instead;
  if that fails too, try this" — this is what a recovery branch is built
  from: try normal navigation, fall back to recovery behaviors on
  failure.
- **Decorator**: wraps exactly one child, modifying its behavior —
  e.g. `RateController` (only lets its child run at a limited rate,
  even if ticked faster), `RecoveryNode` (runs a main child, and on
  failure runs a recovery child a limited number of times before giving
  up entirely — Nav2's stock tree uses this pattern extensively).
- **Condition** and **Action** leaves: the actual work. A Condition
  checks something and immediately returns success/failure (no side
  effects); an Action does something that takes time (like
  `ComputePathToPose` or `FollowPath`) and returns
  running/success/failure.

The whole tree is "ticked" (evaluated) repeatedly, and each node reports
its status back up — this is what makes it reactive: a condition that
starts failing partway through execution (an obstacle appears) can
redirect the tree's flow on the very next tick, not just at the start.

## Reading Nav2's default tree

Nav2 ships `navigate_to_pose_w_replanning_and_recovery.xml`, roughly
structured as:

```
RecoveryNode (main: navigate, recovery: clear costmaps)
  PipelineSequence
    RateController (1 Hz)
      ComputePathToPose
    FollowPath
```

with the outer `RecoveryNode`'s recovery branch itself being a
`RoundRobinNode` cycling through clearing costmaps, spinning in place,
waiting, and backing up — trying a different recovery each time the
main behavior fails again, rather than repeating the same one. Reading
this structure top-down against the node type definitions above is
usually enough to understand exactly what a stock Nav2 robot does when
navigation isn't going smoothly, without needing to read any Nav2 source
code.

## Writing a custom tree from existing nodes

You don't need to write a new compiled BT plugin to customize behavior
meaningfully — arranging Nav2's **existing** registered nodes (Sequence,
Fallback, RecoveryNode, Wait, BackUp, Spin, ComputePathToPose,
FollowPath, and others Nav2 already ships) into a different XML
structure is itself a real, useful form of customization, and it's what
this chapter's demo does. A genuinely new node *type* (custom C++ class
implementing a new condition or action Nav2 doesn't already have) is a
bigger step — worth knowing it's possible, via a BT.CPP plugin registered
so `bt_navigator` can load it by name, but out of scope for this
chapter's demo in favor of showing tree composition concretely first.

## Swapping in a custom tree

Point `bt_navigator`'s `default_nav_to_pose_bt_xml` parameter at your
custom XML file's path (via `nav2_params.yaml`, same file Chapter 11
introduced) instead of Nav2's built-in default — no code changes, no
rebuild, just a config change and a `bt_navigator` restart.

## Common pitfall

A custom XML tree referencing a node type name that doesn't match
anything `bt_navigator` has registered (a typo in a node's XML tag name,
or a node type genuinely not available in your Nav2 installation) fails
at `bt_navigator` startup, typically with an error naming the unknown
node type — but easy to misread as a deeper configuration problem rather
than what it actually is: a simple name mismatch, the BT equivalent of
Chapter 2's topic-name-typo class of bug. Always double check every
`<NodeName ...>` tag in a custom tree against Nav2's list of registered
BT nodes if `bt_navigator` fails to start after a tree change.
