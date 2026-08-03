# Chapter 4: Parameters & Launch Files

## What this is

A **parameter** is a named, typed value a node reads at startup (and can
optionally react to changes of) without you editing and re-running code —
things like a publish rate, a topic name, a threshold. A **launch file**
is a script that starts a whole set of nodes together, with their
parameters, in one command, instead of you opening a terminal per node.

## Why it matters

Chapter 2's talker was hardcoded to publish once a second with a fixed
message. A real robot doesn't work that way — you don't want to edit
source code every time you need a different publish rate or a different
sensor topic name. And a real robot system is never one node: it's
dozens, and starting each by hand in its own terminal doesn't scale. This
chapter is the difference between toy demos and something you could
actually deploy.

## Where this fits

Directly extends the talker pattern from Chapter 2. Every chapter from
here on uses launch files to start demos with more than one node — this
is the last "new mechanism" chapter before things start composing.

## What the demo shows

A parameterized version of the Chapter 2 talker (`publish_rate_hz` and
`message_text` as parameters), a YAML file setting non-default values,
and a launch file that starts the node with that YAML file while also
letting you override the rate from the command line.
