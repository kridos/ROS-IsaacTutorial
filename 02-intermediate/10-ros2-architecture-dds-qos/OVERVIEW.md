# Chapter 10: ROS2 Architecture Deep Dive — DDS & QoS

## What this is

Every topic, service, and action you've used since Chapter 2 has
actually been running over **DDS** (Data Distribution Service), an
existing industrial pub/sub communication standard — ROS2 is built on
top of it rather than implementing its own networking from scratch.
**QoS** (Quality of Service) is DDS's system for controlling, per-topic,
things like whether message delivery is guaranteed and whether late
subscribers get old data.

## Why it matters

You've been using default QoS settings without issue so far, which is
fine for simple demos — but defaults aren't always right, and a QoS
*mismatch* between a publisher and subscriber causes exactly the kind of
silent, hard-to-diagnose non-communication Chapter 2 warned about for
topic name/type mismatches, except QoS mismatches are sneakier: the topic
name and type both look correct in every basic check.

## Where this fits

This is a "look under the hood" chapter — it doesn't introduce new robot
capabilities, but explains machinery you've been relying on since
Chapter 2, in enough depth that Nav2 (Chapter 11) and beyond, where
getting QoS right for sensor and map data actually matters, won't be
mysterious.

## What the demo shows

A publisher and subscriber where you choose the QoS profile (`reliable`
or `best_effort`) for each independently from the command line. Running
matched profiles works normally; running mismatched profiles demonstrates
the silent non-connection firsthand, plus how to diagnose it with `ros2
topic info -v`.
