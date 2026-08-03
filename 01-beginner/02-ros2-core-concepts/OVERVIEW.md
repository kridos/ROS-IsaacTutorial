# Chapter 2: ROS2 Core Concepts — Nodes, Topics, Pub/Sub

## What this is

A **node** is a single running program that does one job — read a sensor,
run a control loop, log data. A real robot is made of many nodes running
at once, each focused on one thing. A **topic** is a named channel nodes
use to send each other messages, and **publish/subscribe** is the pattern
of one node *publishing* messages onto a topic without knowing who (if
anyone) is listening, while other nodes *subscribe* to receive them.

## Why it matters

This is the foundational communication pattern almost everything else in
ROS2 builds on. Camera drivers publish images, navigation stacks
subscribe to them, motor controllers publish odometry, planners subscribe
to that — all as independent nodes that don't call each other's code
directly. Understanding this decoupling is what lets you swap a simulated
camera for a real one without rewriting anything downstream.

## Where this fits

Builds directly on Chapter 1's working install. Chapter 3 (Services &
Actions) covers two *other* communication patterns for when pub/sub isn't
the right fit — you need pub/sub solid first to see why those exist.

## What the demo shows

A `talker` node publishes a counting message on the `/chatter` topic once
a second. A `listener` node subscribes to `/chatter` and prints what it
receives. You'll run both at once (in separate terminals) and watch
messages flow from one to the other — first in Python, then the same
pattern in C++.
