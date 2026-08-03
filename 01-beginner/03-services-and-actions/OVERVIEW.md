# Chapter 3: Services & Actions

## What this is

Topics (Chapter 2) are great for continuous streams of data, but not
every interaction is a stream. Sometimes you want a single question with
a single answer ("what's the current battery percentage?") — that's a
**service**. Sometimes you want to kick off something that takes a while,
watch its progress, and possibly cancel it ("navigate to this waypoint")
— that's an **action**.

## Why it matters

Picking the wrong communication pattern causes real problems: polling a
topic to simulate a one-off request wastes bandwidth and adds latency;
using a service for something that takes 30 seconds blocks the caller the
whole time with no progress feedback and no way to cancel. Nav2 and
MoveIt2 (Chapters 11-12 and 17-18) are built almost entirely on actions
for exactly this reason — "go to this pose" is a long-running goal, not
an instant request.

## Where this fits

Builds on Chapter 2's node/callback fundamentals. Services and actions
both use the same node/callback machinery under the hood — they're new
*patterns* on top of what you already know, not a new execution model.

## What the demo shows

Two independent pairs: a service server/client doing simple integer
addition (`AddTwoInts`), and an action server/client running a Fibonacci
sequence calculation that reports progress and can be cancelled
mid-flight. Both use ROS2's built-in example interfaces, so there's no
custom message-definition step yet — that's introduced later once you
need domain-specific messages.
