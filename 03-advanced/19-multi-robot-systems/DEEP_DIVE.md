# Chapter 19 Deep Dive: Multi-Robot Systems

## Namespacing

A ROS2 **namespace** prefixes every relative topic/service/action/param
name a node uses, without changing the node's own code at all. Launch
two instances of the identical `robot_state_publisher`/bridge/etc. setup
under namespaces `robot1` and `robot2`, and `cmd_vel` (a **relative**
name — no leading slash) automatically becomes `/robot1/cmd_vel` and
`/robot2/cmd_vel` respectively — this is exactly why Chapter 2's
DEEP_DIVE.md flagged the leading-slash-vs-relative distinction as "not
yet important": it becomes important here. A name written with a leading
slash (`/cmd_vel`, **global**) ignores namespacing entirely and would
collide between robots — always use relative names for anything meant to
be per-robot.

In `launch_ros`, this is `Node(namespace="robot1", ...)`, or
`PushRosNamespace("robot1")` wrapping a whole group of nodes/included
launch files at once (used in this chapter's demo, since a robot's full
stack — state publisher, bridge — is several nodes that all need the
same namespace applied together).

## TF namespacing

TF needs the same treatment, and it's easy to namespace topics correctly
while forgetting TF specifically. Two robots' `robot_state_publisher`
instances both publishing a frame literally named `base_link` onto the
same shared `/tf` topic would collide — TF2 (Chapter 8) has no way to
tell "robot1's base_link" from "robot2's base_link" if they're both just
called `base_link`. The standard fix: either namespace the frame IDs
themselves (`robot1/base_link`, `robot2/base_link` — done automatically
by `robot_state_publisher` when both the node and its `frame_prefix`
parameter are namespaced correctly), or keep each robot's TF tree
entirely separate under its own `/robot1/tf` and `/robot2/tf` topics
(less common, since it complicates any code that needs to reason about
both robots' positions relative to each other or to a shared map).

## Multi-robot Nav2

Nav2 (Chapter 11) supports running one full stack per robot, each in its
own namespace, all referencing the same shared map (published once,
globally, since the map itself isn't robot-specific) — Nav2's own
documentation includes a dedicated multi-robot bringup pattern for
exactly this. Each robot's AMCL localizes independently against the
shared map using that robot's own sensor data, and each robot's planner/
controller plans independently — there's no built-in inter-robot
collision avoidance beyond what each robot's own costmap picks up from
seeing the other robot with its own sensors (a real, sometimes limiting
constraint worth knowing about rather than assuming Nav2 handles
multi-robot coordination for you).

## A simple coordination pattern

Full multi-robot task allocation (deciding which robot does what,
resolving conflicts, negotiating shared resources) is a research field
in its own right. This chapter's demo deliberately stays simple: a
single `fleet_coordinator` node that knows both robots' namespaces and
directly publishes different commands to each — a centralized,
one-node-knows-everything pattern, not peer-to-peer negotiation. This is
a legitimate, common real pattern for small fleets (a handful of robots
under one coordinator's direct control), and a reasonable foundation to
build a more sophisticated allocation scheme on top of later, without
needing to understand distributed consensus algorithms just to get two
robots doing different things.

## Common pitfall

Namespacing every topic correctly but forgetting TF (the pitfall
described above) is the single most common multi-robot mistake — it's
easy to test "are the topics separated?" with `ros2 topic list` and see
`/robot1/cmd_vel` and `/robot2/cmd_vel` looking correctly namespaced,
declare victory, and only notice the shared/colliding `base_link` frame
problem once something that consumes TF (RViz2 showing both robots
overlapping at the same origin, or a multi-robot Nav2 setup behaving
strangely) surfaces it far less directly than a topic name collision
would.
