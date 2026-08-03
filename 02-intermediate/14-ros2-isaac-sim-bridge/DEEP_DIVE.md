# Chapter 14 Deep Dive: ROS2 <-> Isaac Sim Bridge

## Architecturally different from ros_gz_bridge

Chapter 7's `ros_gz_bridge` is a **separate process** translating
between two independent transport layers (Gazebo's own transport and
ROS2's DDS). Isaac Sim's ROS2 Bridge (`isaacsim.ros2.bridge`) is
different: it runs **inside the same process** as the simulator itself,
as an extension, and publishes/subscribes ROS2 topics using DDS
directly — there's no second process and no translation layer between
two different transports, because Isaac Sim's bridge speaks DDS
natively rather than needing to bridge it to something else.

## OmniGraph

The mechanism connecting simulation data to ROS2 publishers/subscribers
is **OmniGraph** — Isaac Sim's node-based visual scripting system (think
of it like a flow chart you either build in the GUI or construct
programmatically, where each node does one small job and data flows
along the connections between them). This chapter's demo builds an
OmniGraph with, at minimum:

- A **"ROS2 Subscribe Twist"** node — subscribes to `/cmd_vel`, outputs
  linear/angular velocity values into the graph.
- An **articulation controller** node — takes those velocity values and
  translates them into wheel joint velocity commands on the robot's
  articulation (Isaac Sim's term for a kinematic chain of joints,
  matching the imported URDF's joint structure from Chapter 13).
- A **"ROS2 Publish Odometry"** node — reads the robot's current
  position/velocity from the physics simulation and publishes it as
  `nav_msgs/msg/Odometry` on `/odom`.
- An **"On Playback Tick"** node (or equivalent) driving the whole graph
  once per simulation step, since OmniGraph nodes need something to
  trigger their execution each frame.

You can build this graph either through the Isaac Sim GUI (Window ->
Visual Scripting -> Action Graph) or, as this chapter's demo does,
programmatically via the `omni.graph.core` API — useful for
reproducible, scriptable setups rather than manual GUI clicking every
time.

## DDS and ROS_DOMAIN_ID carry over unchanged

Because Isaac Sim's ROS2 Bridge uses the same DDS layer as every other
ROS2 process (rather than a separate protocol needing its own bridging),
everything from Chapter 10 (QoS, `ROS_DOMAIN_ID`) applies identically
here. A plain `rclpy` node (like this chapter's `drive_and_log_odom.py`)
run in a normal terminal with no Isaac Sim involvement at all can
publish and subscribe to Isaac Sim's bridged topics exactly as if they
came from any other ROS2 node — because, from DDS's perspective, they
are just another ROS2 node's topics.

## Common pitfall: extension not enabled

Like the URDF importer in Chapter 13, the ROS2 Bridge extension is not
always enabled by default — a stock Isaac Sim install may need it turned
on once (Window -> Extensions, search "ROS2 Bridge", or
`enable_extension("isaacsim.ros2.bridge")` in a script, same pattern
Chapter 13 used for the URDF importer). If `/cmd_vel` and `/odom` simply
never appear in `ros2 topic list` at all while Isaac Sim is running, this
is the first thing to check — it's the Isaac Sim equivalent of Chapter
2's silent non-communication pitfall and Chapter 7's forgotten-bridge-topic
pitfall: the same underlying lesson (check `ros2 topic list` first,
always, before assuming a deeper bug) showing up in new machinery.
