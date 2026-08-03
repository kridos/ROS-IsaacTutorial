# Tier 2 (Intermediate) Curriculum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Adaptation note:** Same as the Tier 1 plan
> (`docs/superpowers/plans/2026-08-02-tier1-beginner.md`) — this builds
> tutorial content, not a tested library. "Tests" mean: syntax/structure
> checks runnable without a full ROS2/Isaac Sim install (this authoring
> machine has neither), plus documented expected output in each
> `demo/README.md` for when the reader runs it on real hardware.

**Goal:** Build all 7 chapters of Tier 2 (Intermediate): transforms,
simulated sensors, ROS2 architecture (DDS/QoS), Nav2 basics, MoveIt2
basics, and the first two Isaac Sim chapters.

**Architecture:** One directory per chapter under `02-intermediate/`,
numbered `08-...` through `14-...`, continuing the numbering from Tier 1.
Same `OVERVIEW.md` / `DEEP_DIVE.md` / `demo/` shape as Tier 1.

**Tech Stack:** ROS2 Jazzy (rclpy for all Tier 2 demos — no C++ required
per the spec's language policy, which reserves C++ for Chapters 2, 3, 15,
26 only), Gazebo Harmonic (Ch9 extends Ch7's diff-drive robot with
sensors), Nav2, MoveIt2, NVIDIA Isaac Sim (Ch13-14, Omniverse/USD-based).

## Global Constraints

- Directory layout, file naming, and doc-depth rules: identical to Tier 1
  plan's Global Constraints — see
  `docs/superpowers/plans/2026-08-02-tier1-beginner.md`.
- Chapter numbering continues from Tier 1 (8-14), matching
  `docs/superpowers/specs/2026-08-02-ros2-isaac-curriculum-design.md`.
- Isaac Sim chapters (13-14) require an NVIDIA GPU and cannot be verified
  by running on this authoring machine — content must be precise enough
  to follow correctly regardless (exact menu names, exact API calls,
  version-pinned to Isaac Sim 4.x), and demo scripts still get a
  syntax-only verification pass.
- Every task ends with a git commit.

---

### Task 8: Chapter 8 — TF2 (transforms & coordinate frames)

**Files:**
- Create: `02-intermediate/08-tf2/OVERVIEW.md`
- Create: `02-intermediate/08-tf2/DEEP_DIVE.md`
- Create: `02-intermediate/08-tf2/demo/README.md`
- Create: `02-intermediate/08-tf2/demo/static_frame_broadcaster.py`
- Create: `02-intermediate/08-tf2/demo/dynamic_frame_broadcaster.py`
- Create: `02-intermediate/08-tf2/demo/frame_listener.py`

**Content requirements:**
- OVERVIEW.md: what TF2 is (a live tree of coordinate frame
  relationships), why "where is X relative to Y" needs a dedicated system
  instead of manual math, callback to Chapter 5's robot_state_publisher
  as the first TF producer the reader met.
- DEEP_DIVE.md must cover: the TF tree (parent/child frames, must form a
  tree not a graph — no cycles, no frame with two parents), static vs.
  dynamic transforms (`tf2_ros.StaticTransformBroadcaster` vs.
  `TransformBroadcaster`), `tf2_ros.Buffer` + `TransformListener` for
  looking up a transform between any two frames (even non-adjacent ones —
  TF2 walks the tree), `lookup_transform` with a target time (and why
  `rclpy.time.Time()` meaning "latest available" is usually what you
  want), `tf2_ros.TransformException` and the common causes (frame
  doesn't exist yet, extrapolation into the future), `ros2 run tf2_tools
  view_frames` and `ros2 run tf2_ros tf2_echo <frame1> <frame2>` for
  debugging.
- Demo: `static_frame_broadcaster.py` publishes a fixed
  `sensor_mount -> base_link` static transform; `dynamic_frame_broadcaster.py`
  publishes a `base_link -> moving_frame` transform that rotates over time
  (simulating an orbiting sensor); `frame_listener.py` looks up the
  `sensor_mount -> moving_frame` transform (two hops, neither a direct
  parent of the other) once a second and logs it — demonstrating TF2
  composing transforms across a chain automatically.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write static_frame_broadcaster.py**
- [ ] **Step 3: Write dynamic_frame_broadcaster.py**
- [ ] **Step 4: Write frame_listener.py**
- [ ] **Step 5: Verify Python syntax**

Run: `python3 -c "import ast; [ast.parse(open(f).read()) for f in ['02-intermediate/08-tf2/demo/static_frame_broadcaster.py','02-intermediate/08-tf2/demo/dynamic_frame_broadcaster.py','02-intermediate/08-tf2/demo/frame_listener.py']]"`
Expected: no output.

- [ ] **Step 6: Write demo/README.md**
- [ ] **Step 7: Commit**

```bash
git add 02-intermediate/08-tf2
git commit -m "Add Ch8: TF2 (transforms and coordinate frames)"
```

---

### Task 9: Chapter 9 — Simulated sensors (camera, lidar, IMU in Gazebo)

**Files:**
- Create: `02-intermediate/09-simulated-sensors/OVERVIEW.md`
- Create: `02-intermediate/09-simulated-sensors/DEEP_DIVE.md`
- Create: `02-intermediate/09-simulated-sensors/demo/README.md`
- Create: `02-intermediate/09-simulated-sensors/demo/sensored_diffdrive.urdf.xacro`
- Create: `02-intermediate/09-simulated-sensors/demo/gazebo_sensors.launch.py`
- Create: `02-intermediate/09-simulated-sensors/demo/sensor_subscriber.py`

**Interfaces:**
- Consumes: Chapter 7's `simple_diffdrive.urdf.xacro` chassis pattern and
  `gazebo_sim.launch.py` bridge pattern (extended, not copied wholesale —
  reference the file, add sensor links/plugins on top of the same
  chassis/wheel structure).

**Content requirements:**
- OVERVIEW.md: why simulated sensors matter (developing perception code
  before touching real hardware, generating labeled data cheaply), the
  three sensor types covered (camera, lidar, IMU) and what each is
  typically used for.
- DEEP_DIVE.md: `<gazebo><sensor type="camera">`/`"gpu_lidar"`/`"imu">`
  blocks and their key parameters (update rate, field of view/range for
  lidar, resolution for camera, noise models), the corresponding
  `sensor_msgs` message types (`Image`, `LaserScan`, `Imu`) each plugin
  publishes, bridging each through `ros_gz_bridge` (extends Chapter 7's
  bridge config with three more topic mappings), common pitfall: sensor
  update rate vs. physics step rate mismatches causing choppy or
  duplicated sensor data, and camera `optical_frame` vs. `base_link`
  frame convention (REP 103 — Z-forward for optical frames vs. X-forward
  for robot frames) as a common source of confusingly-rotated camera data
  downstream.
- Demo: extends Chapter 7's diff-drive robot with a forward-facing
  camera, a 2D lidar, and an IMU, all bridged to ROS2;
  `sensor_subscriber.py` subscribes to all three topics and logs a
  one-line summary of each message as it arrives (image dimensions,
  lidar min/max range in the current scan, IMU orientation quaternion).

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write sensored_diffdrive.urdf.xacro**
- [ ] **Step 3: Verify XML well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('02-intermediate/09-simulated-sensors/demo/sensored_diffdrive.urdf.xacro')"`
Expected: no output.

- [ ] **Step 4: Write gazebo_sensors.launch.py**
- [ ] **Step 5: Write sensor_subscriber.py**
- [ ] **Step 6: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('02-intermediate/09-simulated-sensors/demo/gazebo_sensors.launch.py').read()); ast.parse(open('02-intermediate/09-simulated-sensors/demo/sensor_subscriber.py').read())"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Commit**

```bash
git add 02-intermediate/09-simulated-sensors
git commit -m "Add Ch9: Simulated sensors (camera, lidar, IMU)"
```

---

### Task 10: Chapter 10 — ROS2 architecture deep dive (DDS, QoS)

**Files:**
- Create: `02-intermediate/10-ros2-architecture-dds-qos/OVERVIEW.md`
- Create: `02-intermediate/10-ros2-architecture-dds-qos/DEEP_DIVE.md`
- Create: `02-intermediate/10-ros2-architecture-dds-qos/demo/README.md`
- Create: `02-intermediate/10-ros2-architecture-dds-qos/demo/qos_publisher.py`
- Create: `02-intermediate/10-ros2-architecture-dds-qos/demo/qos_subscriber.py`

**Content requirements:**
- OVERVIEW.md: ROS2's communication actually runs over DDS (Data
  Distribution Service), a pre-existing industrial pub/sub standard — why
  ROS2 was built on top of an existing standard instead of a custom
  protocol (interoperability, maturity, vendor choice), and that QoS
  (Quality of Service) is DDS's mechanism for controlling delivery
  guarantees per-topic, forward-referenced back in Chapter 2.
- DEEP_DIVE.md must cover: DDS's decentralized discovery (no master/roscore
  the way ROS1 had — this is why killing one node doesn't take down the
  whole system), the specific QoS policies that matter most in practice —
  **Reliability** (RELIABLE vs BEST_EFFORT), **Durability** (VOLATILE vs
  TRANSIENT_LOCAL — the latter is what lets a late-joining subscriber get
  the last published message, common for e.g. a map topic), **History**
  (KEEP_LAST with a depth vs KEEP_ALL), and **Deadline**; explicit rule
  that a publisher and subscriber with **incompatible** QoS (e.g.
  publisher BEST_EFFORT + subscriber RELIABLE) silently fail to connect —
  exactly like Chapter 2's topic-name/type mismatch pitfall, but harder
  to spot since `ros2 topic list` still shows the topic; `ros2 topic info
  -v` showing each endpoint's QoS profile as the diagnostic tool; sensor
  data convention (BEST_EFFORT, KEEP_LAST depth 5 — dropping an old
  camera frame is fine) vs. critical command/state data convention
  (RELIABLE, sometimes TRANSIENT_LOCAL); ROS_DOMAIN_ID revisited from
  Chapter 1 now explained properly as a DDS domain ID partitioning
  discovery.
- Demo: `qos_publisher.py` and `qos_subscriber.py` accept a QoS profile
  name (`reliable` or `best_effort`) as a CLI argument; running matched
  profiles connects and delivers messages, running mismatched profiles
  (publisher `best_effort`, subscriber `reliable`) demonstrates the
  silent non-connection — the reader runs it both ways and compares.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write qos_publisher.py**
- [ ] **Step 3: Write qos_subscriber.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('02-intermediate/10-ros2-architecture-dds-qos/demo/qos_publisher.py').read()); ast.parse(open('02-intermediate/10-ros2-architecture-dds-qos/demo/qos_subscriber.py').read())"`
Expected: no output.

- [ ] **Step 5: Write demo/README.md**

Must include the matched-profile and mismatched-profile run instructions
and what to observe in each case (messages flow vs. `ros2 topic echo`
showing nothing and `ros2 topic info -v` showing incompatible QoS).

- [ ] **Step 6: Commit**

```bash
git add 02-intermediate/10-ros2-architecture-dds-qos
git commit -m "Add Ch10: ROS2 architecture deep dive (DDS, QoS)"
```

---

### Task 11: Chapter 11 — Nav2 basics

**Files:**
- Create: `02-intermediate/11-nav2-basics/OVERVIEW.md`
- Create: `02-intermediate/11-nav2-basics/DEEP_DIVE.md`
- Create: `02-intermediate/11-nav2-basics/demo/README.md`
- Create: `02-intermediate/11-nav2-basics/demo/nav2_params.yaml`
- Create: `02-intermediate/11-nav2-basics/demo/nav2_sim.launch.py`
- Create: `02-intermediate/11-nav2-basics/demo/send_goal.py`

**Content requirements:**
- OVERVIEW.md: what Nav2 is (the standard ROS2 navigation stack: given a
  map and a goal pose, drive the robot there while avoiding obstacles),
  the three big pieces at a glance (localization, path planning, obstacle
  avoidance/control), why you use Nav2 instead of writing this yourself
  (it's a large, battle-tested system — full of edge cases you don't want
  to rediscover).
- DEEP_DIVE.md must cover: the Nav2 architecture as a set of ROS2 nodes
  working together — map_server (serves a pre-built map), AMCL
  (Adaptive Monte Carlo Localization — estimates robot pose on that map
  using lidar), the costmap (2D grid marking obstacles, inflated by
  robot radius), a global planner (plans a path across the whole
  costmap, e.g. NavFn/Smac), a local controller (follows that path while
  reacting to newly-seen obstacles, e.g. DWB/MPPI), and the behavior
  tree that sequences these into "navigate to pose" — this is the same
  action-based pattern from Chapter 3, now doing something real
  (`NavigateToPose` action); the lifecycle-managed node pattern Nav2
  uses (nodes start unconfigured, then configured, then active — managed
  by the `lifecycle_manager`) and why (coordinated startup ordering
  across many interdependent nodes); AMCL requiring an initial pose
  estimate (`/initialpose`) before it can localize, and what happens
  without one (particle filter has no idea where to start); common
  pitfall: costmap not clearing/inflating as expected due to a
  misconfigured `robot_radius`/`inflation_radius`, causing the robot to
  either graze obstacles or refuse paths through tight-but-passable
  spaces.
- Demo: `nav2_params.yaml` — a minimal Nav2 parameter file (small
  costmap, AMCL, planner/controller defaults) tuned for the Chapter
  7/9 diff-drive robot; `nav2_sim.launch.py` launches Gazebo (reusing
  Chapter 9's sensored robot for lidar), the Nav2 stack via Nav2's
  standard bringup launch include, and RViz2 with Nav2's default config;
  `send_goal.py` sends a `NavigateToPose` action goal programmatically
  (the Chapter 3 action-client pattern) and logs feedback (distance
  remaining) as the robot drives there.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write nav2_params.yaml**
- [ ] **Step 3: Verify YAML parses**

Run: `python3 -c "import yaml; yaml.safe_load(open('02-intermediate/11-nav2-basics/demo/nav2_params.yaml'))"`
Expected: no output.

- [ ] **Step 4: Write nav2_sim.launch.py**
- [ ] **Step 5: Write send_goal.py**
- [ ] **Step 6: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('02-intermediate/11-nav2-basics/demo/nav2_sim.launch.py').read()); ast.parse(open('02-intermediate/11-nav2-basics/demo/send_goal.py').read())"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Commit**

```bash
git add 02-intermediate/11-nav2-basics
git commit -m "Add Ch11: Nav2 basics"
```

---

### Task 12: Chapter 12 — MoveIt2 basics

**Files:**
- Create: `02-intermediate/12-moveit2-basics/OVERVIEW.md`
- Create: `02-intermediate/12-moveit2-basics/DEEP_DIVE.md`
- Create: `02-intermediate/12-moveit2-basics/demo/README.md`
- Create: `02-intermediate/12-moveit2-basics/demo/arm_with_gripper.urdf.xacro`
- Create: `02-intermediate/12-moveit2-basics/demo/moveit_planning.launch.py`
- Create: `02-intermediate/12-moveit2-basics/demo/move_to_pose.py`

**Interfaces:**
- Consumes: Chapter 5's `simple_arm.urdf.xacro` 2-link arm pattern
  (extended with a 3rd joint and a simple gripper link for a more
  MoveIt2-realistic example, not copied wholesale).

**Content requirements:**
- OVERVIEW.md: what MoveIt2 is (motion planning for arms/manipulators:
  given a target end-effector pose or joint configuration, compute a
  collision-free trajectory to get there), where it fits vs. Nav2 (Nav2
  moves the whole robot base through 2D space; MoveIt2 moves an arm's
  joints through configuration space — same underlying planning idea,
  different domain).
- DEEP_DIVE.md must cover: the MoveIt2 architecture — `move_group` node
  (the central coordinator), the planning scene (the arm's current state
  plus any known obstacles), a motion planning plugin (commonly OMPL —
  Open Motion Planning Library — sampling-based planners), forward vs.
  inverse kinematics (FK: given joint angles, where's the end-effector;
  IK: given a desired end-effector pose, what joint angles achieve it —
  MoveIt2 solves IK for you when you specify a target pose instead of
  target joint angles), the SRDF (Semantic Robot Description Format —
  layered on top of URDF, defines planning groups: which joints move
  together as "the arm", and group states, e.g. a named "home"
  configuration), the MoveGroupInterface (Python: `moveit_py` /
  `moveit_commander`-successor) as the client API used to request plans
  and execution — same "send a goal, get a result" shape as Nav2's
  action interface underneath; common pitfall: a target pose that's
  kinematically unreachable or in collision causes planning to fail with
  no obvious single cause — checking the planning scene in RViz2's
  MotionPlanning display (start/goal state coloring) is the standard way
  to diagnose why.
- Demo: extends the Chapter 5 arm with a 3rd joint and a simple 2-finger
  gripper link; `moveit_planning.launch.py` starts `move_group` with a
  minimal SRDF/config for this arm, plus RViz2 with the MotionPlanning
  display; `move_to_pose.py` uses the MoveGroupInterface to request a
  plan to a target end-effector pose and execute it, logging whether
  planning succeeded.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write arm_with_gripper.urdf.xacro**
- [ ] **Step 3: Verify XML well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('02-intermediate/12-moveit2-basics/demo/arm_with_gripper.urdf.xacro')"`
Expected: no output.

- [ ] **Step 4: Write moveit_planning.launch.py**
- [ ] **Step 5: Write move_to_pose.py**
- [ ] **Step 6: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('02-intermediate/12-moveit2-basics/demo/moveit_planning.launch.py').read()); ast.parse(open('02-intermediate/12-moveit2-basics/demo/move_to_pose.py').read())"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Commit**

```bash
git add 02-intermediate/12-moveit2-basics
git commit -m "Add Ch12: MoveIt2 basics"
```

---

### Task 13: Chapter 13 — Isaac Sim intro (Omniverse, USD, importing a robot)

**Files:**
- Create: `02-intermediate/13-isaac-sim-intro/OVERVIEW.md`
- Create: `02-intermediate/13-isaac-sim-intro/DEEP_DIVE.md`
- Create: `02-intermediate/13-isaac-sim-intro/demo/README.md`
- Create: `02-intermediate/13-isaac-sim-intro/demo/import_and_spawn.py`

**Content requirements:**
- OVERVIEW.md: what Isaac Sim is (NVIDIA's GPU-accelerated robotics
  simulator, built on Omniverse), how it differs from Gazebo (photorealistic
  rendering via RTX, GPU-accelerated physics via PhysX, built for
  synthetic data generation and large-scale/parallel simulation — trade
  higher hardware requirements for higher fidelity and scale), where it
  fits relative to everything learned so far (same robot-description and
  ROS2-bridging concepts as Gazebo, different simulator underneath).
- DEEP_DIVE.md must cover: **USD** (Universal Scene Description) — the
  file format/scene-graph Isaac Sim (and Omniverse generally) is built
  on, conceptually similar in purpose to SDF (describes a scene of
  prims/objects) but far more general (used across VFX/film industry
  too), the **stage** (the current USD scene being edited/simulated),
  **prims** (the nodes in a USD scene graph — a robot becomes a tree of
  prims), importing a URDF into Isaac Sim (the URDF Importer extension —
  converts your Chapter 5/7 URDF into USD prims with the same link/joint
  structure), the **Isaac Sim Python API** (`isaacsim.core` /
  `omni.isaac.core` depending on version) for scripting the simulator
  itself (spawning objects, stepping physics, reading sensor data) as
  distinct from ROS2 (this API controls Isaac Sim directly; the ROS2
  bridge, Chapter 14, is a separate layer on top), and the **extension**
  system (Isaac Sim's plugin architecture — most functionality, including
  the URDF importer and ROS2 bridge, is an enable/disable-able
  extension); common pitfall: a URDF importing with visually-wrong scale
  or an exploded/disconnected robot, almost always caused by unit
  mismatches (URDF is meters; some meshes are authored in
  centimeters/millimeters) or missing inertial values Isaac Sim's
  PhysX-based importer is stricter about than Gazebo was.
- Demo: `import_and_spawn.py` — an Isaac Sim Python script (run via Isaac
  Sim's bundled Python environment, `./python.sh` per Isaac Sim's own
  convention) that starts the simulator headlessly, imports Chapter 7's
  `simple_diffdrive.urdf.xacro` (converted to plain URDF via `xacro`
  first) via the URDF importer extension's API, spawns it into an empty
  stage, steps physics for a few seconds, and prints the robot's world
  pose each step — confirming the import worked and physics is applying
  to it (e.g., settling under gravity onto a ground plane) without
  requiring the full GUI.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write import_and_spawn.py**
- [ ] **Step 3: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('02-intermediate/13-isaac-sim-intro/demo/import_and_spawn.py').read())"`
Expected: no output. (The Isaac Sim-specific imports inside will not
resolve on this machine — that's expected; syntax validity is the bar
here, same caveat as rclpy/launch imports in Tier 1.)

- [ ] **Step 4: Write demo/README.md**

Must state the Isaac Sim version this targets, GPU/driver prerequisites,
and the exact `./python.sh import_and_spawn.py` invocation convention.

- [ ] **Step 5: Commit**

```bash
git add 02-intermediate/13-isaac-sim-intro
git commit -m "Add Ch13: Isaac Sim intro (Omniverse, USD, importing a robot)"
```

---

### Task 14: Chapter 14 — ROS2 <-> Isaac Sim bridge; finalize Tier 2

**Files:**
- Create: `02-intermediate/14-ros2-isaac-sim-bridge/OVERVIEW.md`
- Create: `02-intermediate/14-ros2-isaac-sim-bridge/DEEP_DIVE.md`
- Create: `02-intermediate/14-ros2-isaac-sim-bridge/demo/README.md`
- Create: `02-intermediate/14-ros2-isaac-sim-bridge/demo/ros2_bridge_sim.py`
- Create: `02-intermediate/14-ros2-isaac-sim-bridge/demo/drive_and_log_odom.py`
- Modify: `02-intermediate/README.md` (new file, tier index — same role as
  `01-beginner/README.md`)
- Modify: `README.md` (root — mark Tier 2 complete, matching how Task 7
  of the Tier 1 plan updated it)

**Content requirements:**
- OVERVIEW.md: what the ROS2 bridge extension does (publishes/subscribes
  ROS2 topics from inside a running Isaac Sim scene, conceptually the
  same role as Gazebo's `ros_gz_bridge` from Chapter 7, but implemented
  as an in-process Isaac Sim extension/OmniGraph node rather than a
  separate bridge process), what the demo shows (drive the Chapter 13
  robot via `/cmd_vel` and read `/odom`, exactly mirroring Chapter 7's
  Gazebo demo so the parallel is obvious).
- DEEP_DIVE.md must cover: the ROS2 Bridge extension
  (`isaacsim.ros2.bridge`) and how it differs architecturally from
  `ros_gz_bridge` — it runs inside the same process as the simulator via
  **OmniGraph** (Isaac Sim's visual/node-based scripting system for
  wiring simulation data to outputs, including ROS2 publishers/subscribers
  as graph nodes) rather than a separate bridging process reading two
  transport layers; the specific OmniGraph nodes used for this chapter's
  demo (`ROS2 Subscribe Twist`, `ROS2 Publish Odometry`, and an
  articulation controller node translating Twist into wheel joint
  commands); `ROS_DOMAIN_ID` and DDS considerations carrying over
  unchanged from Chapter 10 — Isaac Sim's ROS2 bridge uses the same DDS
  layer as everything else in this curriculum, not a separate protocol;
  common pitfall: forgetting to enable the ROS2 Bridge extension (it's
  off by default in a stock Isaac Sim install) leading to `/cmd_vel`
  simply never appearing in `ros2 topic list` at all — the Isaac Sim
  equivalent of Chapter 2's "silent non-communication" pitfall, same
  underlying lesson (check `ros2 topic list` first, always) applied to
  new machinery.
- Demo: `ros2_bridge_sim.py` extends Chapter 13's script to additionally
  build the OmniGraph wiring `/cmd_vel` to the robot's wheels and the
  robot's odometry to `/odom`, then runs the sim loop (GUI, not headless,
  so the reader can watch it); `drive_and_log_odom.py` is a plain ROS2
  node (rclpy, no Isaac Sim imports — run in a normal terminal, exactly
  like Chapter 7's `ros2 topic pub`/`ros2 topic echo` pattern) that
  publishes a forward-drive Twist and logs incoming Odometry.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write ros2_bridge_sim.py**
- [ ] **Step 3: Write drive_and_log_odom.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('02-intermediate/14-ros2-isaac-sim-bridge/demo/ros2_bridge_sim.py').read()); ast.parse(open('02-intermediate/14-ros2-isaac-sim-bridge/demo/drive_and_log_odom.py').read())"`
Expected: no output (`drive_and_log_odom.py` should compile cleanly with
no caveats — it only imports rclpy/geometry_msgs/nav_msgs, same as prior
chapters' Python demos).

- [ ] **Step 5: Write demo/README.md**
- [ ] **Step 6: Write 02-intermediate/README.md**

Same structure as `01-beginner/README.md`: goal statement, prerequisite
note (this tier assumes Tier 1 complete; Chapters 13-14 additionally
require Isaac Sim installed on an NVIDIA GPU per Chapter 13's
DEEP_DIVE.md), and a numbered list of all 7 chapters with one-line
descriptions.

- [ ] **Step 7: Update root README.md**

Change the Tier 2 line from "(in progress)" to "— complete" and expand
its one-line description to name all 7 chapters, matching the pattern
Task 7 of the Tier 1 plan used for Tier 1's entry.

- [ ] **Step 8: Commit**

```bash
git add 02-intermediate/14-ros2-isaac-sim-bridge 02-intermediate/README.md README.md
git commit -m "Add Ch14: ROS2-Isaac Sim bridge; complete Tier 2 (intermediate)"
```

---

## Self-Review Notes

- Spec coverage: all 7 Tier 2 chapters from the spec (TF2, simulated
  sensors, ROS2 architecture/DDS/QoS, Nav2 basics, MoveIt2 basics, Isaac
  Sim intro, ROS2<->Isaac Sim bridge) have a task.
- Language policy: no C++ demos in Tier 2 — matches spec (C++ reserved
  for Ch2, 3, 15, 26 only).
- Cross-chapter continuity: Ch9 extends Ch7's robot; Ch11 reuses Ch9's
  sensored robot for lidar-based localization; Ch12 extends Ch5's arm;
  Ch13-14 deliberately mirror Ch7's Gazebo demo structure (spawn robot,
  bridge cmd_vel/odom, drive and log) so the reader can directly compare
  Gazebo vs. Isaac Sim doing the same task — this parallel is called out
  explicitly in both chapters' OVERVIEW.md per the content requirements
  above.
- No placeholders: every task specifies exact file paths and concrete
  content outlines; verification steps are syntax/structure checks
  runnable without ROS2 or Isaac Sim installed, consistent with the
  authoring machine's constraints (documented in the Adaptation Note and
  Global Constraints above).
