# Chapter 20 Deep Dive: MuJoCo

## MJCF

MuJoCo describes scenes in its own XML format, **MJCF**
(MuJoCo XML format) — conceptually playing the same role URDF (Chapter
5) and SDF (Chapter 7) play for their respective ecosystems: bodies
(links), joints, geometry, inertial properties. MJCF is not
interchangeable with URDF/SDF directly (though conversion tools exist for
simple cases) — this chapter's `simple_arm.xml` is written directly in
MJCF rather than converted from an earlier chapter's URDF, because a
faithful conversion tool is its own separate topic and the concepts
transfer regardless of which format taught them first.

## The Python API: a different programming style

Where ROS2 (and Gazebo/Isaac Sim's ROS2 bridges) work through
publish/subscribe message passing, MuJoCo's Python bindings work through
**direct function calls and array access**:

- `mujoco.MjModel.from_xml_path(path)` — loads an MJCF file into an
  immutable `MjModel` (the static description: bodies, joints, masses —
  doesn't change during simulation).
- `mujoco.MjData(model)` — the mutable simulation state (positions,
  velocities, forces) that *does* change every step.
- `mujoco.mj_step(model, data)` — advances the simulation by one physics
  timestep, mutating `data` in place.
- `mujoco.mj_forward(model, data)` — computes derived quantities (like
  the positions of every body given current joint angles) from the
  current state *without* advancing time — useful when you've manually
  set a joint position and want everything else to reflect it before the
  next real step.
- `data.qpos`, `data.qvel` — direct NumPy arrays of every joint's
  position and velocity, indexed by joint order in the model. Reading or
  writing simulation state means reading or writing these arrays
  directly, not calling a getter/setter API or waiting for a message.

This is a noticeably lower-level, more "just a library" style than
ROS2's node/topic model — there's no discovery, no messages, no QoS
(Chapter 10's concerns don't exist here at all) — you're calling
functions in a loop you write and control entirely yourself.

## Why MuJoCo for RL

Reinforcement learning training typically needs *many* simulated
episodes — often millions of environment steps — to learn a good policy.
MuJoCo's speed (it can simulate simple systems at many times real-time,
and supports running many independent simulation instances in parallel)
is what makes that tractable on ordinary hardware. This is the same
underlying need Chapter 22's Isaac Lab addresses differently: instead of
running many CPU-bound MuJoCo instances in parallel, Isaac Lab
GPU-parallelizes physics itself (via PhysX) so a single GPU simulates
thousands of environments simultaneously — different technical approach,
same motivating problem (training needs simulation throughput ordinary
single-instance simulation can't provide).

## No first-party ROS2 bridge

Unlike Gazebo (`ros_gz_bridge`) and Isaac Sim (the ROS2 Bridge
extension), MuJoCo has no NVIDIA/Open Robotics-maintained ROS2
integration. Community bridge packages exist, or you write a thin
publishing layer yourself (a plain rclpy node that calls `mj_step()` in
its own loop and publishes `data.qpos`/`qvel` as ROS2 messages) — a real
practical consideration if you're picking a simulator for a ROS2-centric
project: MuJoCo's speed advantage for RL comes with this integration gap,
which Gazebo and Isaac Sim don't have.

## Common pitfall

Expecting MuJoCo to behave like Gazebo or Isaac Sim — i.e., that
"starting the simulator" makes physics run automatically in the
background while you subscribe to topics — is a common first mistake for
someone coming from ROS2-integrated simulators. MuJoCo's Python API is
just a library: nothing steps physics until *your own code* calls
`mj_step()`, in a loop you write and control. There's no implicit
"simulation is running" state the way Chapter 7/13's simulators provide
by default.
