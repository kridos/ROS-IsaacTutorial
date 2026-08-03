# Chapter 5 Deep Dive: URDF/Xacro

## Links: the rigid pieces

Each `<link>` has up to three sub-descriptions, each serving a different
purpose:

- `<visual>` — what it looks like (a mesh or primitive shape, a color) —
  used for rendering in RViz2/Gazebo, has zero effect on physics.
- `<collision>` — the shape used for physics/collision checking — often
  a simplified version of the visual shape (a box instead of a detailed
  mesh) since collision checking is cheaper on simple shapes.
- `<inertial>` — mass and the inertia tensor — used by physics engines
  (Gazebo, Chapter 7) to simulate how the link responds to forces. A
  link with no `<inertial>` is effectively treated as massless, which
  breaks physics simulation (it'll behave unrealistically or Gazebo will
  warn about it) — this chapter's RViz-only demo doesn't need accurate
  inertial values, but Chapter 7's Gazebo demo does.

## Joints: how links connect and move

A `<joint>` names a `<parent>` link and a `<child>` link, and a `type`:

- `fixed` — no motion at all, rigidly welds two links together (e.g. a
  sensor bolted to a chassis).
- `revolute` — rotates around one axis, with limited range (needs
  `<limit>` lower/upper bounds) — most robot arm joints.
- `continuous` — rotates around one axis with no limit (e.g. a wheel).
- `prismatic` — slides linearly along one axis, with limits (e.g. a
  linear actuator).

`<axis xyz="0 0 1"/>` declares which axis (in the joint's own local
frame) the joint rotates/slides around. `<origin xyz="..." rpy="..."/>`
on a joint places the child link's origin relative to the parent — this
is what actually builds up the kinematic chain.

Every link except the root must be the child of exactly one joint — a
link that's nobody's child is a disconnected, floating second robot as
far as ROS2 is concerned, which is the most common URDF authoring
mistake (usually from a copy-pasted joint with the wrong parent/child
names).

## robot_state_publisher and TF

`robot_state_publisher` reads your URDF once at startup (to learn the
static link/joint structure) and then, every time it receives a
`sensor_msgs/msg/JointState` message (telling it each joint's current
angle/position), publishes the resulting tree of coordinate transforms
on the `/tf` and `/tf_static` topics. This is how "joint 1 is at 30
degrees" becomes "link1's origin is at this specific (x, y, z) position
relative to the base" — full mechanics of consuming that transform tree
are in Chapter 8. In this chapter's demo, `joint_state_publisher_gui`
supplies those `JointState` messages from slider positions you control
by hand; a real robot would publish them from actual encoder readings
instead — `robot_state_publisher` doesn't care which.

## Xacro: macros, properties, math

Raw URDF has no variables — every number is a literal, and a two-armed
robot would mean writing every joint/link twice with no way to keep them
in sync. Xacro adds:

```xml
<xacro:property name="link1_length" value="0.3"/>
<link name="link1">
  <visual>
    <geometry><box size="0.05 0.05 ${link1_length}"/></geometry>
  </visual>
</link>
```

`${...}` evaluates a math expression using declared properties.
`<xacro:macro name="..." params="...">...</xacro:macro>` defines a
reusable block (e.g. "an arm segment") you instantiate multiple times
with different parameters — not used in this chapter's simple 2-link
demo, but essential once a robot has repeated structure (four identical
wheels, two identical arms).

Convert Xacro to plain URDF with:

```bash
xacro simple_arm.urdf.xacro > simple_arm.urdf
```

though in practice you usually don't do this by hand — `robot_state_publisher`
can be pointed at the Xacro's *expanded* URDF string directly from a
launch file, which is what `display.launch.py` does.

## Common pitfall: disconnected tree

If RViz2 shows only your base link, or the `RobotModel` display shows a
"No transform" warning for other links, the near-universal cause is a
`<joint>` whose `<parent>` or `<child>` doesn't exactly match another
link's `name` attribute (case-sensitive, no typos). `ros2 run tf2_tools
view_frames` (or just watching TF errors in the terminal) will point at
exactly which frame is missing its parent.
