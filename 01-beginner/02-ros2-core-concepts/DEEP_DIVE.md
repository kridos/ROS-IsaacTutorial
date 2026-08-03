# Chapter 2 Deep Dive: Nodes, Topics, Pub/Sub

## The ROS2 graph

At any moment, all the running nodes and the topics connecting them form
what's called the **ROS2 graph** — think of it as a live diagram: boxes
(nodes) connected by arrows (topics), where each arrow's direction shows
who's publishing and who's subscribing. Nothing about this graph is fixed
in code anywhere — it emerges from whichever nodes happen to be running
right now, which is what makes ROS2 systems modular: start, stop, or
replace a node and the graph just changes shape.

## Messages and message types

A topic carries one specific **message type** — a fixed structure of
fields, similar to a struct. `std_msgs/msg/String` (used in this
chapter's demo) has exactly one field: `data`, a string. Message types are
defined in `.msg` files shipped by packages (`std_msgs`, `sensor_msgs`,
`geometry_msgs`, etc. — you'll meet more of these as the curriculum
progresses) and code-generated into Python classes / C++ structs you
import and use directly. A publisher and subscriber on the same topic
**must** agree on the message type — ROS2 doesn't do implicit conversion.

## Node lifecycle basics (rclpy / rclcpp)

Every node, in either language, follows the same shape:

1. **Init** the ROS2 client library (`rclpy.init()` / `rclcpp::init()`) —
   sets up communication with the rest of the ROS2 graph.
2. **Create** a node object, then create publishers/subscribers/timers on
   it.
3. **Spin** — hand control to the ROS2 executor, which calls your
   callbacks (timer callbacks, subscription callbacks) whenever something
   happens. Your code doesn't poll for messages; the executor delivers
   them.
4. **Shutdown** — clean up when done.

The demo's `talker.py` uses a timer callback (fires every N seconds,
regardless of any incoming message) to publish; `listener.py` uses a
subscription callback (fires whenever a message arrives on `/chatter`).

## Topic naming conventions

Topic names are paths, e.g. `/chatter` or `/robot1/cmd_vel`. Convention:
lowercase, underscore-separated, and namespaced by robot or subsystem
when you have more than one of something (Chapter 19, multi-robot
systems, leans on this heavily). A leading `/` makes a name **global**;
without it, names resolve relative to the node's namespace — a distinction
that matters once you start namespacing nodes, but not yet in this chapter.

## Introspecting a running graph

These CLI tools work against whatever's currently running — no code
changes needed:

- `ros2 node list` — every currently running node's name.
- `ros2 topic list` — every currently active topic.
- `ros2 topic echo /chatter` — print messages on a topic live, useful for
  checking "is anything actually being published here?"
- `ros2 topic hz /chatter` — measure the actual publish rate, useful for
  checking a node is running at the rate you expect (not too slow, not
  silently stalled).
- `ros2 topic info /chatter` — shows the message type and how many
  publishers/subscribers are currently connected to it.

## QoS (a forward reference)

Every publisher and subscriber has a **Quality of Service** policy
controlling things like whether messages are guaranteed to arrive
(reliable vs. best-effort) and how many recent messages are buffered.
This chapter's demo uses ROS2's default QoS, which works fine for a
simple string topic. QoS becomes important — and can silently break
communication if publisher/subscriber QoS are incompatible — once you're
dealing with sensor data at high rates. Full treatment in Chapter 10
(ROS2 architecture deep dive).

## Common pitfall: silent non-communication

If a talker is publishing and a listener is subscribed but nothing
happens, the two most common causes are:

1. **Topic name typo** — `/chatter` vs `/Chatter` vs `/chater`. ROS2 topic
   names are case-sensitive and won't warn you about a near-miss; `ros2
   topic list` while both nodes are running is the fastest way to spot
   this (you'll see two different topics where you expected one).
2. **Mismatched message type** — a publisher using `std_msgs/msg/String`
   and a subscriber expecting `std_msgs/msg/Int32` on the same topic name
   will fail to connect at all, again without an error message pointing
   directly at the mismatch. `ros2 topic info <topic> -v` shows the
   message type each connected node is using.
