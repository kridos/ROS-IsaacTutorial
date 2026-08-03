# Tier 1 (Beginner) Curriculum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Adaptation note:** This plan builds tutorial content (markdown + demo
> scripts), not a tested library. "Tests" below mean: run the demo exactly
> as documented and confirm it produces the stated observable output
> (terminal log lines, `ros2 topic echo` output, RViz/Gazebo showing the
> expected state). There are no unit-test files. Each task's content
> requirements are specified as an outline, not verbatim prose — the
> implementer writes the actual explanatory text following that outline
> and the tone/format rules in Global Constraints.

**Goal:** Build all 7 chapters of Tier 1 (Beginner) of the ROS2/Isaac
robotics curriculum: dev environment through Gazebo basics, each with
OVERVIEW.md, DEEP_DIVE.md, and a working commented demo.

**Architecture:** One directory per chapter under `01-beginner/`, numbered
`01-...` through `07-...`. Each is self-contained: a reader who has done
prior chapters in order can complete it using only its own files plus
software installed in Chapter 1.

**Tech Stack:** ROS2 (Jazzy or latest LTS — pin exact version in Chapter 1),
Python 3 (rclpy), C++ (rclcpp) for Chapters 2–3 only, Gazebo (Harmonic or
latest matching the ROS2 distro), colcon, Ubuntu 22.04/24.04.

## Global Constraints

- Directory layout: `01-beginner/NN-topic-slug/{OVERVIEW.md,DEEP_DIVE.md,demo/}`
  per the spec at `docs/superpowers/specs/2026-08-02-ros2-isaac-curriculum-design.md`.
- OVERVIEW.md: 5–10 min read. What it is, why it matters, where it fits vs.
  neighboring chapters, what the demo shows. No deep API detail.
- DEEP_DIVE.md: full technical mechanics in plain language — architecture,
  data flow, key APIs/config, common pitfalls. Assume zero prior robotics
  knowledge but a competent programmer.
- demo/ code: heavily commented, comments explain *why* not just *what*.
  Smallest example that clearly demonstrates the concept. Must include a
  "How to run" + "Expected output" section either in a demo/README.md or
  as a header comment in the main file — be consistent across chapters
  (use `demo/README.md` for every chapter, decided here for consistency).
- Python demos use `rclpy`; C++ demos (Ch 2, 3 only) use `rclcpp` and a
  proper `package.xml` / `CMakeLists.txt` so they build with `colcon build`.
- Root `README.md` and `01-beginner/README.md` are created/updated as part
  of Task 1 and finalized in Task 8.
- Every task ends with a git commit.

---

### Task 1: Repo scaffold + Chapter 1 (Dev environment)

**Files:**
- Create: `README.md` (root curriculum map — tiers, prerequisites, how to
  use the repo; links to `01-beginner/README.md` and stubs for the other
  three tiers noting they are "coming next")
- Create: `01-beginner/README.md` (tier index: lists chapters 1–7, one
  line each, what to know before starting the tier)
- Create: `01-beginner/01-dev-environment/OVERVIEW.md`
- Create: `01-beginner/01-dev-environment/DEEP_DIVE.md`
- Create: `01-beginner/01-dev-environment/demo/README.md`
- Create: `01-beginner/01-dev-environment/demo/verify_install.sh`

**Content requirements:**
- OVERVIEW.md: what ROS2 is (one paragraph), why a proper dev environment
  matters, what "workspace" and "package" mean at a high level, what the
  demo does (a script that checks the install and prints a summary).
- DEEP_DIVE.md must cover: Ubuntu version requirements, installing ROS2
  (apt method) for the LTS distro chosen in Tech Stack, environment
  setup (`source /opt/ros/<distro>/setup.bash`, why `.bashrc` sourcing
  matters), creating a colcon workspace (`~/ros2_ws/src`), installing
  `colcon`, `rosdep init`/`update`, common install pitfalls (locale
  issues, missing `python3-colcon-common-extensions`, ROS_DOMAIN_ID
  collisions on shared networks).
- `verify_install.sh`: a bash script, heavily commented, that checks
  `ros2 --version` runs, prints the ROS_DISTRO env var, runs
  `ros2 pkg list | wc -l` to show packages are indexed, and prints a
  colored PASS/FAIL summary line per check.

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p 01-beginner/01-dev-environment/demo
```

- [ ] **Step 2: Write root README.md, 01-beginner/README.md, OVERVIEW.md, DEEP_DIVE.md**

Follow the content requirements above. Root README links to
`01-beginner/README.md`; notes tiers 2–4 are in progress.

- [ ] **Step 3: Write demo/verify_install.sh and demo/README.md**

Script must be `chmod +x`'d and use `set -euo pipefail` is NOT appropriate
here (individual checks should fail gracefully and report PASS/FAIL rather
than aborting) — use per-check `if command -v ros2 >/dev/null 2>&1; then`
style guards instead.

- [ ] **Step 4: Verify the demo runs**

Run: `bash 01-beginner/01-dev-environment/demo/verify_install.sh`
Expected: script executes without syntax errors and prints PASS/FAIL lines
for each check (PASS/FAIL depends on whether ROS2 is actually installed on
this machine — a clean syntax run with no bash errors is the acceptance
bar here, not a fully-installed ROS2 on the authoring machine).

Run: `bash -n 01-beginner/01-dev-environment/demo/verify_install.sh`
Expected: no output (syntax OK).

- [ ] **Step 5: Commit**

```bash
git add README.md 01-beginner/README.md 01-beginner/01-dev-environment
git commit -m "Add curriculum root README and Ch1: dev environment setup"
```

---

### Task 2: Chapter 2 — ROS2 core concepts (nodes, topics, pub/sub)

**Files:**
- Create: `01-beginner/02-ros2-core-concepts/OVERVIEW.md`
- Create: `01-beginner/02-ros2-core-concepts/DEEP_DIVE.md`
- Create: `01-beginner/02-ros2-core-concepts/demo/README.md`
- Create: `01-beginner/02-ros2-core-concepts/demo/python/talker.py`
- Create: `01-beginner/02-ros2-core-concepts/demo/python/listener.py`
- Create: `01-beginner/02-ros2-core-concepts/demo/cpp/src/talker.cpp`
- Create: `01-beginner/02-ros2-core-concepts/demo/cpp/src/listener.cpp`
- Create: `01-beginner/02-ros2-core-concepts/demo/cpp/CMakeLists.txt`
- Create: `01-beginner/02-ros2-core-concepts/demo/cpp/package.xml`

**Interfaces:**
- Produces: a `talker`/`listener` pattern on topic `/chatter` using
  `std_msgs/msg/String`, reused conceptually (not code) by Chapter 3's
  services demo for consistency of naming style.

**Content requirements:**
- OVERVIEW.md: what a node is, what a topic is, publish/subscribe model,
  why decoupling matters for robots (e.g. a camera node doesn't need to
  know who's listening).
- DEEP_DIVE.md: ROS2 graph, `rclpy`/`rclcpp` node lifecycle basics,
  message types and `.msg` definitions, topic name conventions,
  `ros2 node list` / `ros2 topic list` / `ros2 topic echo` / `ros2 topic
  hz` for introspection, publisher/subscriber QoS defaults (forward
  reference — full QoS in Chapter 10), common pitfall: mismatched message
  types or topic name typos causing silent non-communication.
- Python demo: `talker.py` publishes a `String` counting message on
  `/chatter` at 1 Hz; `listener.py` subscribes and logs it. Both must be
  runnable standalone with `python3 talker.py` (use `rclpy.init()` /
  spin / shutdown pattern), no colcon package required for the Python
  version — keep it copy-paste runnable for a beginner.
- C++ demo: same talker/listener pair, buildable via `colcon build` as a
  package named `ros2_core_concepts_cpp`.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**

- [ ] **Step 2: Write Python talker.py and listener.py**

Include comments explaining `rclpy.init()`, `create_publisher`,
`create_timer`, `spin`, and shutdown/cleanup.

- [ ] **Step 3: Verify Python demo syntax**

Run: `python3 -m py_compile 01-beginner/02-ros2-core-concepts/demo/python/talker.py 01-beginner/02-ros2-core-concepts/demo/python/listener.py`
Expected: no output (compiles cleanly). Note: this does not require rclpy
to be installed if `rclpy` import errors are tolerated — if `py_compile`
fails specifically on `import rclpy` not being found, that's expected on a
non-ROS machine; re-run with `python3 -c "import ast; ast.parse(open('talker.py').read())"`
style parse-only check instead to confirm syntax validity independent of
rclpy availability.

- [ ] **Step 4: Write C++ talker.cpp, listener.cpp, CMakeLists.txt, package.xml**

Standard `ament_cmake` package structure, dependencies on `rclcpp` and
`std_msgs`.

- [ ] **Step 5: Write demo/README.md**

Document: how to run the Python version directly, how to build/run the
C++ version via colcon, and expected terminal output (listener printing
`I heard: "Hello, ROS2! count=N"` once per second).

- [ ] **Step 6: Commit**

```bash
git add 01-beginner/02-ros2-core-concepts
git commit -m "Add Ch2: ROS2 core concepts (nodes, topics, pub/sub)"
```

---

### Task 3: Chapter 3 — Services & Actions

**Files:**
- Create: `01-beginner/03-services-and-actions/OVERVIEW.md`
- Create: `01-beginner/03-services-and-actions/DEEP_DIVE.md`
- Create: `01-beginner/03-services-and-actions/demo/README.md`
- Create: `01-beginner/03-services-and-actions/demo/python/add_two_ints_server.py`
- Create: `01-beginner/03-services-and-actions/demo/python/add_two_ints_client.py`
- Create: `01-beginner/03-services-and-actions/demo/python/fibonacci_action_server.py`
- Create: `01-beginner/03-services-and-actions/demo/python/fibonacci_action_client.py`
- Create: `01-beginner/03-services-and-actions/demo/cpp/src/add_two_ints_server.cpp`
- Create: `01-beginner/03-services-and-actions/demo/cpp/src/add_two_ints_client.cpp`
- Create: `01-beginner/03-services-and-actions/demo/cpp/CMakeLists.txt`
- Create: `01-beginner/03-services-and-actions/demo/cpp/package.xml`

**Interfaces:**
- Consumes: naming/style conventions from Chapter 2's talker/listener.
- Produces: request/response pattern (`example_interfaces/srv/AddTwoInts`)
  and long-running goal/feedback/result pattern
  (`example_interfaces/action/Fibonacci`) that Chapter 12 (MoveIt2) and
  Chapter 17 (advanced Nav2) reference conceptually as "this is the same
  action pattern Nav2/MoveIt2 use under the hood."

**Content requirements:**
- OVERVIEW.md: when to use a topic vs. a service vs. an action (one-shot
  request/response vs. long-running with feedback/cancel), everyday
  robot examples for each (service: "what's the battery level right
  now", action: "navigate to this waypoint").
- DEEP_DIVE.md: service `.srv` structure (request/response), action
  `.action` structure (goal/feedback/result), synchronous vs async
  client calls, action server goal acceptance/cancellation/preemption
  basics, `ros2 service call` / `ros2 action send_goal` CLI usage, common
  pitfall: blocking the executor by calling a service synchronously from
  inside a callback (deadlock) and how to avoid it.
- Python: services use built-in `example_interfaces/srv/AddTwoInts`;
  action uses built-in `example_interfaces/action/Fibonacci` — both avoid
  needing custom interface packages so the demo stays copy-paste runnable.
- C++: only the services demo (add_two_ints) is required in C++, per
  Global Constraints language policy — action C++ demo is not required
  for this chapter (kept to Python; DEEP_DIVE.md notes C++ actions exist
  and are structurally similar).

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**

- [ ] **Step 2: Write Python service server/client**

- [ ] **Step 3: Write Python action server/client**

- [ ] **Step 4: Verify Python demo syntax**

Run: `python3 -m py_compile 01-beginner/03-services-and-actions/demo/python/*.py`
(or per-file if globbing doesn't expand in the shell used)
Expected: compiles cleanly, or fails only on `rclpy` import per the same
caveat as Task 2 Step 3.

- [ ] **Step 5: Write C++ add_two_ints server/client, CMakeLists.txt, package.xml**

- [ ] **Step 6: Write demo/README.md**

Document run instructions and expected output for all four demos
(service server+client, action server+client).

- [ ] **Step 7: Commit**

```bash
git add 01-beginner/03-services-and-actions
git commit -m "Add Ch3: Services and Actions"
```

---

### Task 4: Chapter 4 — Parameters & Launch files

**Files:**
- Create: `01-beginner/04-parameters-and-launch/OVERVIEW.md`
- Create: `01-beginner/04-parameters-and-launch/DEEP_DIVE.md`
- Create: `01-beginner/04-parameters-and-launch/demo/README.md`
- Create: `01-beginner/04-parameters-and-launch/demo/configurable_talker.py`
- Create: `01-beginner/04-parameters-and-launch/demo/talker_config.yaml`
- Create: `01-beginner/04-parameters-and-launch/demo/talker.launch.py`

**Content requirements:**
- OVERVIEW.md: what parameters are for (runtime-configurable node
  behavior without code changes), what launch files are for (starting
  and wiring up multiple nodes at once), why this matters once you have
  more than one node.
- DEEP_DIVE.md: declaring parameters (`declare_parameter`), reading them
  at startup vs. dynamic reconfiguration with a parameter callback, YAML
  parameter files, Python launch file structure (`LaunchDescription`,
  `Node` action, `DeclareLaunchArgument`, passing params from a YAML
  file), `ros2 param list/get/set` CLI, common pitfall: parameter type
  must match the declared default's type or it throws.
- Demo: `configurable_talker.py` extends Chapter 2's talker with a
  `publish_rate_hz` and `message_text` parameter; `talker_config.yaml`
  sets non-default values; `talker.launch.py` launches the node with
  that YAML file plus a launch argument to override `publish_rate_hz`
  from the command line.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**

- [ ] **Step 2: Write configurable_talker.py and talker_config.yaml**

- [ ] **Step 3: Write talker.launch.py**

- [ ] **Step 4: Verify syntax**

Run: `python3 -m py_compile 01-beginner/04-parameters-and-launch/demo/configurable_talker.py 01-beginner/04-parameters-and-launch/demo/talker.launch.py`
Expected: compiles cleanly (or rclpy/launch import caveat as before).

Run: `python3 -c "import yaml, sys; yaml.safe_load(open('01-beginner/04-parameters-and-launch/demo/talker_config.yaml'))"`
Expected: no output — YAML parses.

- [ ] **Step 5: Write demo/README.md**

- [ ] **Step 6: Commit**

```bash
git add 01-beginner/04-parameters-and-launch
git commit -m "Add Ch4: Parameters and Launch files"
```

---

### Task 5: Chapter 5 — Robot description (URDF/Xacro)

**Files:**
- Create: `01-beginner/05-urdf-xacro/OVERVIEW.md`
- Create: `01-beginner/05-urdf-xacro/DEEP_DIVE.md`
- Create: `01-beginner/05-urdf-xacro/demo/README.md`
- Create: `01-beginner/05-urdf-xacro/demo/simple_arm.urdf.xacro`
- Create: `01-beginner/05-urdf-xacro/demo/display.launch.py`
- Create: `01-beginner/05-urdf-xacro/demo/rviz_config.rviz`

**Content requirements:**
- OVERVIEW.md: what URDF is (a robot's physical description: links and
  joints), why Xacro exists (macros/variables so URDF isn't copy-pasted
  by hand), what the demo shows (a simple 2-link arm visualized in
  RViz2 with joint_state_publisher_gui sliders).
- DEEP_DIVE.md: `<link>` (visual/collision/inertial), `<joint>` types
  (fixed, revolute, continuous, prismatic) and their `<axis>`/`<limit>`,
  the `robot_state_publisher` node and how it turns joint states + URDF
  into TF frames (forward reference to Chapter 8), Xacro macros/
  properties/math, converting xacro to URDF with `xacro` CLI, common
  pitfall: mismatched or missing joint parent/child causing a
  disconnected robot tree.
- Demo: `simple_arm.urdf.xacro` — a 2-revolute-joint arm (base → link1 →
  link2) using Xacro properties for link lengths; `display.launch.py`
  launches `robot_state_publisher`, `joint_state_publisher_gui`, and
  `rviz2` with the provided config so the reader can move sliders and
  see the arm move.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**

- [ ] **Step 2: Write simple_arm.urdf.xacro**

- [ ] **Step 3: Verify xacro/XML is well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('01-beginner/05-urdf-xacro/demo/simple_arm.urdf.xacro')"`
Expected: no output — file is well-formed XML.

- [ ] **Step 4: Write display.launch.py**

- [ ] **Step 5: Write rviz_config.rviz (minimal: RobotModel + TF displays)**

- [ ] **Step 6: Write demo/README.md**

- [ ] **Step 7: Commit**

```bash
git add 01-beginner/05-urdf-xacro
git commit -m "Add Ch5: Robot description (URDF/Xacro)"
```

---

### Task 6: Chapter 6 — Debugging & visualization tools (RViz2, rqt, ros2 bag)

**Files:**
- Create: `01-beginner/06-debugging-and-visualization/OVERVIEW.md`
- Create: `01-beginner/06-debugging-and-visualization/DEEP_DIVE.md`
- Create: `01-beginner/06-debugging-and-visualization/demo/README.md`
- Create: `01-beginner/06-debugging-and-visualization/demo/noisy_sensor_publisher.py`
- Create: `01-beginner/06-debugging-and-visualization/demo/record_and_replay.sh`

**Content requirements:**
- OVERVIEW.md: RViz2 (3D visualization), rqt (introspection GUI tools:
  rqt_graph, rqt_console, rqt_plot), `ros2 bag` (record/replay topic
  data) — why these three together are how you actually debug a running
  robot instead of reading logs blindly.
- DEEP_DIVE.md: `rqt_graph` for visualizing the node/topic graph,
  `rqt_console` for filtering log levels, `rqt_plot` for plotting numeric
  topic fields live, `ros2 bag record`/`play`/`info`, replaying recorded
  data through the same nodes for offline debugging, common pitfall:
  forgetting `--use-sim-time` consistency when replaying bags against
  nodes expecting simulated time.
- Demo: `noisy_sensor_publisher.py` publishes a `Float64` with injected
  Gaussian noise on `/sensor/reading` at 10 Hz (so there's something
  worth plotting/recording); `record_and_replay.sh` shows the full
  `ros2 bag record` → stop → `ros2 bag play` → `ros2 topic echo` loop.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**

- [ ] **Step 2: Write noisy_sensor_publisher.py**

- [ ] **Step 3: Verify syntax**

Run: `python3 -c "import ast; ast.parse(open('01-beginner/06-debugging-and-visualization/demo/noisy_sensor_publisher.py').read())"`
Expected: no output.

- [ ] **Step 4: Write record_and_replay.sh**

Run: `bash -n 01-beginner/06-debugging-and-visualization/demo/record_and_replay.sh`
Expected: no output (syntax OK).

- [ ] **Step 5: Write demo/README.md**

- [ ] **Step 6: Commit**

```bash
git add 01-beginner/06-debugging-and-visualization
git commit -m "Add Ch6: Debugging and visualization tools"
```

---

### Task 7: Chapter 7 — Gazebo basics

**Files:**
- Create: `01-beginner/07-gazebo-basics/OVERVIEW.md`
- Create: `01-beginner/07-gazebo-basics/DEEP_DIVE.md`
- Create: `01-beginner/07-gazebo-basics/demo/README.md`
- Create: `01-beginner/07-gazebo-basics/demo/simple_diffdrive.urdf.xacro`
- Create: `01-beginner/07-gazebo-basics/demo/gazebo_sim.launch.py`
- Create: `01-beginner/07-gazebo-basics/demo/empty_world.sdf`

**Content requirements:**
- OVERVIEW.md: what Gazebo is, how it relates to ROS2 (`ros_gz_bridge` /
  `gz_ros2_control`), what the demo shows: a simple differential-drive
  robot spawned in an empty world, drivable via `/cmd_vel`.
- DEEP_DIVE.md: Gazebo Harmonic architecture (gz-sim, SDF worlds vs
  URDF robots), the ROS2↔Gazebo bridge (topic-by-topic bridging,
  `ros_gz_bridge` YAML config), gz plugins for diff-drive control,
  spawning a robot into a running world (`ros_gz_sim create`), common
  pitfall: physics engine step size / real-time factor mismatches
  causing sluggish or unstable sim, and the ROS_DOMAIN_ID/bridge topic
  name mismatch trap.
- Demo: extends Chapter 5's URDF pattern with a diff-drive plugin and
  two wheel joints; `gazebo_sim.launch.py` starts Gazebo with
  `empty_world.sdf`, spawns the robot, and starts the `ros_gz_bridge`
  for `/cmd_vel` and `/odom`. Reader can drive it with
  `ros2 topic pub /cmd_vel geometry_msgs/msg/Twist ...` or
  `teleop_twist_keyboard`.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**

- [ ] **Step 2: Write simple_diffdrive.urdf.xacro**

- [ ] **Step 3: Verify XML well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('01-beginner/07-gazebo-basics/demo/simple_diffdrive.urdf.xacro')"`
Expected: no output.

- [ ] **Step 4: Write empty_world.sdf**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('01-beginner/07-gazebo-basics/demo/empty_world.sdf')"`
Expected: no output.

- [ ] **Step 5: Write gazebo_sim.launch.py**

- [ ] **Step 6: Write demo/README.md**

Include the `ros2 topic pub` one-liner to drive the robot and what to
expect to see (robot moving forward/turning in the Gazebo GUI, `/odom`
values changing when echoed).

- [ ] **Step 7: Update 01-beginner/README.md and root README.md**

Mark Tier 1 complete, list all 7 chapters with one-line descriptions.

- [ ] **Step 8: Commit**

```bash
git add 01-beginner/07-gazebo-basics 01-beginner/README.md README.md
git commit -m "Add Ch7: Gazebo basics; complete Tier 1 (beginner)"
```

---

## Self-Review Notes

- Spec coverage: all 7 Tier-1 chapters from the spec have a task; root and
  tier README requirements covered in Tasks 1 and 7.
- Language policy: C++ demos present for Ch2 (talker/listener) and Ch3
  (services only, per spec's chapter list — spec lists C++ for "Services
  & Actions" broadly; this plan narrows Ch3's C++ to services and
  documents why in Task 3, since a full C++ action demo adds significant
  boilerplate for a beginner chapter without a proportional teaching
  gain — DEEP_DIVE.md covers the C++ action API conceptually instead).
- Type/naming consistency: topic `/chatter`, message `std_msgs/msg/String`
  reused Ch2→demo README; `example_interfaces` used in Ch3 to avoid
  custom `.srv`/`.action` packages, consistent with keeping Tier 1
  copy-paste runnable.
- No placeholders: every task specifies exact file paths and concrete
  content outlines; verification steps are syntax/structure checks
  runnable without a full ROS2 install, since the authoring machine may
  not have ROS2 installed.
