# Tier 3 (Advanced) Curriculum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Adaptation note:** Same as Tier 1/2 plans — this builds tutorial
> content, not a tested library. "Tests" mean syntax/structure checks
> runnable without ROS2/Isaac Sim/Docker/Kubernetes installed (this
> authoring machine has none of them), plus documented expected output
> in each `demo/README.md`.

**Goal:** Build all 7 chapters of Tier 3 (Advanced): Isaac ROS GPU
perception, synthetic data generation, advanced Nav2, advanced MoveIt2,
multi-robot systems, MuJoCo, containerized robotics (Docker), and
orchestrating robot fleets with Kubernetes.

**Architecture:** One directory per chapter under `03-advanced/`,
numbered `15-...` through `21-...`, continuing Tier 1/2's numbering.
Same `OVERVIEW.md` / `DEEP_DIVE.md` / `demo/` shape.

**Tech Stack:** Isaac ROS (NITROS, VSLAM), Isaac Sim Replicator, Nav2
(behavior trees, custom planners), MoveIt2 (pick-and-place), ROS2
namespacing for multi-robot, MuJoCo (Python bindings, MJCF), Docker,
Kubernetes (kubectl, a local cluster via kind/minikube).

## Global Constraints

- Directory layout, file naming, doc-depth rules: identical to Tier 1/2
  Global Constraints.
- Chapter numbering continues from Tier 2 (15-21), matching
  `docs/superpowers/specs/2026-08-02-ros2-isaac-curriculum-design.md`
  (as amended to add the Kubernetes chapter).
- Chapter 15 (Isaac ROS) is Python + C++ per the spec's language policy
  (production perception nodes are predominantly C++/NITROS) — the only
  Tier 3 chapter with a C++ demo.
- Every task ends with a git commit.

---

### Task 15: Chapter 15 — Isaac ROS (GPU perception, NITROS, VSLAM)

**Files:**
- Create: `03-advanced/15-isaac-ros-perception/OVERVIEW.md`
- Create: `03-advanced/15-isaac-ros-perception/DEEP_DIVE.md`
- Create: `03-advanced/15-isaac-ros-perception/demo/README.md`
- Create: `03-advanced/15-isaac-ros-perception/demo/python/vslam_pose_listener.py`
- Create: `03-advanced/15-isaac-ros-perception/demo/cpp/src/apriltag_pose_logger.cpp`
- Create: `03-advanced/15-isaac-ros-perception/demo/cpp/CMakeLists.txt`
- Create: `03-advanced/15-isaac-ros-perception/demo/cpp/package.xml`
- Create: `03-advanced/15-isaac-ros-perception/demo/isaac_ros_perception.launch.py`

**Content requirements:**
- OVERVIEW.md: what Isaac ROS is (a collection of GPU-accelerated ROS2
  perception packages from NVIDIA — VSLAM, AprilTag detection, object
  detection, and more, all designed to run on Jetson/RTX hardware with
  minimal CPU involvement), why GPU-accelerated perception matters (CPU
  perception pipelines can't keep up with high-rate camera/lidar data on
  embedded hardware — this is what makes real-time perception on a
  physical robot feasible).
- DEEP_DIVE.md must cover: **NITROS** (NVIDIA Isaac Transport for ROS) —
  Isaac ROS's zero-copy GPU memory transport between nodes, avoiding the
  GPU-to-CPU-to-GPU memory copies a normal ROS2 topic would incur when
  passing image/tensor data between GPU-accelerated nodes on the same
  machine, and why this matters (memory copies are often the actual
  bottleneck in a GPU perception pipeline, not the compute); **Isaac ROS
  Visual SLAM** (`isaac_ros_visual_slam`) — GPU-accelerated visual
  odometry/SLAM from stereo camera input, publishing a pose estimate and
  TF (tying back to Chapter 8), positioned as a GPU-accelerated
  alternative to the kind of lidar-based localization Nav2's AMCL
  (Chapter 11) does; **AprilTag detection** (`isaac_ros_apriltag`) — GPU
  fiducial marker detection, commonly used for ground-truth
  pose-in-the-loop testing and simple localization; the
  Docker-container-based Isaac ROS development workflow (Isaac ROS
  packages are distributed and developed inside a provided dev container
  with the right CUDA/TensorRT versions pre-installed, rather than a
  plain apt install, because of tight version coupling to specific
  JetPack/CUDA versions) — this is a deliberate forward-reference to
  Chapter 21's general Docker content, introduced here narrowly because
  Isaac ROS specifically requires it; common pitfall: running Isaac ROS
  packages outside the provided dev container/without matching
  CUDA/TensorRT versions being the single most common Isaac ROS setup
  failure, distinct from ordinary ROS2 package version mismatches.
- Demo: `vslam_pose_listener.py` (Python) subscribes to Isaac ROS Visual
  SLAM's output pose topic and logs it, alongside a TF lookup (Chapter 8
  pattern) confirming the `map -> base_link` (or equivalent) transform
  VSLAM publishes; `apriltag_pose_logger.cpp` (C++) subscribes to
  `isaac_ros_apriltag`'s detection topic and logs each detected tag's ID
  and pose — chosen as the C++ demo specifically because production
  perception-consuming nodes are the case where the language policy
  calls for C++ (per Global Constraints).

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write vslam_pose_listener.py**
- [ ] **Step 3: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/15-isaac-ros-perception/demo/python/vslam_pose_listener.py').read())"`
Expected: no output.

- [ ] **Step 4: Write apriltag_pose_logger.cpp, CMakeLists.txt, package.xml**
- [ ] **Step 5: Verify package.xml is well-formed XML**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('03-advanced/15-isaac-ros-perception/demo/cpp/package.xml')"`
Expected: no output.

- [ ] **Step 6: Write isaac_ros_perception.launch.py**
- [ ] **Step 7: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/15-isaac-ros-perception/demo/isaac_ros_perception.launch.py').read())"`
Expected: no output.

- [ ] **Step 8: Write demo/README.md**

Must state this requires the Isaac ROS dev container workflow and an
NVIDIA Jetson or RTX GPU, and give the exact dev-container launch
command pattern.

- [ ] **Step 9: Commit**

```bash
git add 03-advanced/15-isaac-ros-perception
git commit -m "Add Ch15: Isaac ROS (GPU perception, NITROS, VSLAM)"
```

---

### Task 16: Chapter 16 — Synthetic data generation (Isaac Sim Replicator)

**Files:**
- Create: `03-advanced/16-synthetic-data-replicator/OVERVIEW.md`
- Create: `03-advanced/16-synthetic-data-replicator/DEEP_DIVE.md`
- Create: `03-advanced/16-synthetic-data-replicator/demo/README.md`
- Create: `03-advanced/16-synthetic-data-replicator/demo/generate_dataset.py`

**Content requirements:**
- OVERVIEW.md: what synthetic data generation is (rendering many
  labeled training images from a simulated scene instead of manually
  collecting and labeling real photos), why it matters (training a
  perception model — object detection, segmentation — needs thousands of
  labeled examples; generating them in Isaac Sim is far cheaper than
  manual photography+labeling, and simulation gives you perfect
  ground-truth labels for free).
- DEEP_DIVE.md must cover: **Replicator** (Isaac Sim's synthetic data
  generation toolkit) — domain randomization (randomizing lighting,
  textures, object poses, camera angles across renders so a model
  trained on the data generalizes instead of overfitting to one exact
  scene), the annotator system (RGB, depth, semantic segmentation,
  bounding boxes, instance segmentation — each an "annotator" you attach
  to a camera/render product to get that specific labeled output
  alongside the RGB image), writers (`BasicWriter` and format-specific
  writers like COCO or KITTI, which take annotator output and write it
  to disk in a standard dataset format downstream training code expects);
  the render-and-capture loop structure (set up a scene, randomize
  parameters, trigger a render, capture annotator outputs, repeat N
  times); common pitfall: forgetting to randomize enough variables (only
  randomizing object position but not lighting/texture, for instance)
  producing a dataset that looks large in image count but is actually
  low-diversity, leading to a model that overfits despite having
  "thousands" of training images — quantity isn't the same as diversity.
- Demo: `generate_dataset.py` — an Isaac Sim script that places the
  Chapter 5 arm (or a simple primitive object, whichever keeps the demo
  fast) in a scene, randomizes its pose and the lighting across N
  iterations, and uses Replicator's `BasicWriter` to save RGB images plus
  bounding-box annotations to a local output folder, printing a summary
  count of images written.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write generate_dataset.py**
- [ ] **Step 3: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/16-synthetic-data-replicator/demo/generate_dataset.py').read())"`
Expected: no output.

- [ ] **Step 4: Write demo/README.md**
- [ ] **Step 5: Commit**

```bash
git add 03-advanced/16-synthetic-data-replicator
git commit -m "Add Ch16: Synthetic data generation (Isaac Sim Replicator)"
```

---

### Task 17: Chapter 17 — Advanced Nav2 (custom planners, behavior trees)

**Files:**
- Create: `03-advanced/17-advanced-nav2/OVERVIEW.md`
- Create: `03-advanced/17-advanced-nav2/DEEP_DIVE.md`
- Create: `03-advanced/17-advanced-nav2/demo/README.md`
- Create: `03-advanced/17-advanced-nav2/demo/custom_bt.xml`
- Create: `03-advanced/17-advanced-nav2/demo/wait_and_retry_node.py`
- Create: `03-advanced/17-advanced-nav2/demo/nav2_custom_bt.launch.py`

**Content requirements:**
- OVERVIEW.md: revisits Chapter 11's behavior tree mention, now going
  deep on it — what customizing Nav2's behavior tree buys you (different
  recovery strategies, custom conditions/actions specific to your robot
  or task) beyond the default XML Chapter 11 used implicitly.
- DEEP_DIVE.md must cover: behavior tree fundamentals as used by Nav2's
  `bt_navigator` — the core node types (Sequence: run children in order,
  fail if any fails; Fallback/Selector: try children in order, succeed on
  the first success; Decorator: wraps one child, e.g. RateController or
  RecoveryNode; Condition and Action leaf nodes), reading Nav2's default
  `navigate_to_pose_w_replanning_and_recovery.xml` as a worked example
  (what each branch does — compute path, follow path, and the recovery
  branch triggered on failure: clear costmaps, spin, wait, backup), how
  to write a **custom BT node** as a ROS2 plugin (a C++ or Python class
  implementing the BT.CPP node interface, registered via a plugin
  description so `bt_navigator` can load it by name from an XML tree),
  and swapping in a custom XML tree via the `default_nav_to_pose_bt_xml`
  parameter; common pitfall: a custom BT XML referencing a node type
  name that doesn't match what was registered in the plugin list —
  fails at `bt_navigator` startup with an unhelpful "node not found"
  style error, the BT equivalent of Chapter 2's topic-name-typo class of
  bug.
- Demo: `wait_and_retry_node.py` — hold on, BT.CPP plugins are C++-only
  in current Nav2 versions; adjust demo to a C++-free, still-concrete
  alternative: `custom_bt.xml` defines a tree using Nav2's **existing**
  built-in nodes in a non-default arrangement (e.g., a Fallback that
  tries a normal NavigateToPose approach, and on failure runs an
  explicit `Wait` + `BackUp` + retry sequence with a distinct, more
  patient recovery pattern than the stock tree) — this teaches BT
  composition concretely without requiring a new compiled plugin;
  `wait_and_retry_node.py` becomes a plain rclpy script that sends a
  goal (Chapter 11 pattern) to a Nav2 instance running with this custom
  tree loaded, and logs which branch appears to have executed based on
  feedback/timing, so the reader can observe the custom tree's behavior
  end to end; `nav2_custom_bt.launch.py` extends Chapter 11's
  `nav2_sim.launch.py` pattern, pointing `bt_navigator` at
  `custom_bt.xml` via the params override.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write custom_bt.xml**
- [ ] **Step 3: Verify XML well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('03-advanced/17-advanced-nav2/demo/custom_bt.xml')"`
Expected: no output.

- [ ] **Step 4: Write wait_and_retry_node.py**
- [ ] **Step 5: Write nav2_custom_bt.launch.py**
- [ ] **Step 6: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/17-advanced-nav2/demo/wait_and_retry_node.py').read()); ast.parse(open('03-advanced/17-advanced-nav2/demo/nav2_custom_bt.launch.py').read())"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Commit**

```bash
git add 03-advanced/17-advanced-nav2
git commit -m "Add Ch17: Advanced Nav2 (custom behavior trees)"
```

---

### Task 18: Chapter 18 — Advanced MoveIt2 (pick-and-place pipelines)

**Files:**
- Create: `03-advanced/18-advanced-moveit2-pick-place/OVERVIEW.md`
- Create: `03-advanced/18-advanced-moveit2-pick-place/DEEP_DIVE.md`
- Create: `03-advanced/18-advanced-moveit2-pick-place/demo/README.md`
- Create: `03-advanced/18-advanced-moveit2-pick-place/demo/pick_and_place.py`
- Create: `03-advanced/18-advanced-moveit2-pick-place/demo/planning_scene_setup.py`

**Content requirements:**
- OVERVIEW.md: what a full pick-and-place pipeline adds beyond Chapter
  12's single-pose planning — approach/grasp/retreat waypoints, gripper
  actuation timing, and planning around a known obstacle (the object
  being picked, and whatever it's sitting on).
- DEEP_DIVE.md must cover: the **Planning Scene Interface** (adding
  collision objects — e.g. a table and a target block — to MoveIt2's
  world model, referenced in Chapter 12's DEEP_DIVE.md but not used
  there; used properly here), **Cartesian path planning**
  (`compute_cartesian_path` — plans a sequence of waypoints the
  end-effector moves through in a straight line, as opposed to Chapter
  12's single free-form pose-to-pose plan — needed for a controlled
  straight-line approach/retreat during grasping rather than an
  arbitrary path that might approach the object from an unexpected
  angle), **attaching/detaching objects** (once grasped, the object
  becomes logically part of the end-effector for collision-checking
  purposes during the retreat/place motion — MoveIt2's
  `attach_object`/`detach_object` calls), the overall pick-and-place
  sequence (move to pre-grasp pose -> Cartesian approach -> close
  gripper -> attach object -> Cartesian retreat -> move to pre-place
  pose -> Cartesian approach -> open gripper -> detach object ->
  Cartesian retreat); common pitfall: forgetting to attach the grasped
  object before planning the retreat/transport motion, causing MoveIt2 to
  plan as if the gripper were empty and potentially generate a
  trajectory that would actually collide the (unmodeled, still-attached)
  object with something in the scene.
- Demo: `planning_scene_setup.py` adds a table (box) and a target block
  (small box) as collision objects to the Chapter 12 arm's planning
  scene; `pick_and_place.py` runs the full sequence above using
  `MoveGroupInterface` (Chapter 12 pattern) plus Cartesian path planning
  and attach/detach calls, logging each stage as it completes.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write planning_scene_setup.py**
- [ ] **Step 3: Write pick_and_place.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/18-advanced-moveit2-pick-place/demo/planning_scene_setup.py').read()); ast.parse(open('03-advanced/18-advanced-moveit2-pick-place/demo/pick_and_place.py').read())"`
Expected: no output.

- [ ] **Step 5: Write demo/README.md**
- [ ] **Step 6: Commit**

```bash
git add 03-advanced/18-advanced-moveit2-pick-place
git commit -m "Add Ch18: Advanced MoveIt2 (pick-and-place pipelines)"
```

---

### Task 19: Chapter 19 — Multi-robot systems

**Files:**
- Create: `03-advanced/19-multi-robot-systems/OVERVIEW.md`
- Create: `03-advanced/19-multi-robot-systems/DEEP_DIVE.md`
- Create: `03-advanced/19-multi-robot-systems/demo/README.md`
- Create: `03-advanced/19-multi-robot-systems/demo/multi_robot_sim.launch.py`
- Create: `03-advanced/19-multi-robot-systems/demo/fleet_coordinator.py`

**Content requirements:**
- OVERVIEW.md: what changes when there's more than one robot — topic
  namespacing so robots don't collide on the same topic names (Chapter
  2's `/cmd_vel` becomes ambiguous with two robots), and coordination
  (avoiding two robots colliding with each other, dividing up tasks).
- DEEP_DIVE.md must cover: **namespacing** — launching multiple
  instances of the same node/robot description under different ROS2
  namespaces (`/robot1/cmd_vel`, `/robot2/cmd_vel`, etc. — the
  `namespace=` argument to launch_ros's `Node`/`PushRosNamespace`,
  revisiting Chapter 2's topic-naming DEEP_DIVE.md, where the
  leading-slash-vs-relative distinction now actually matters); TF
  namespacing specifically (each robot needs its own `tf` tree rooted at
  its own `<namespace>/base_link` etc., since two robots both publishing
  `base_link` on a shared `/tf` would collide — either fully separate TF
  trees per robot namespace, or a shared `map` frame with per-robot
  subtrees, depending on whether the robots need to reason about each
  other's position); multi-robot Nav2 (each robot runs its own full Nav2
  stack in its own namespace against a shared map, per Nav2's documented
  multi-robot pattern); a simple coordination pattern (a
  `fleet_coordinator` node that knows about both robots' namespaces and
  assigns each a different goal, rather than a peer-to-peer negotiation
  scheme — kept simple deliberately, since full multi-robot task
  allocation is its own deep field); common pitfall: forgetting to
  namespace TF specifically (namespacing topics but not realizing TF
  needs the same treatment) causing both robots' `robot_state_publisher`
  instances to publish conflicting `base_link` transforms on the same
  shared `/tf` topic.
- Demo: `multi_robot_sim.launch.py` spawns two instances of the Chapter 7
  diff-drive robot into the same Gazebo world, each under its own
  namespace (`robot1`, `robot2`) with separately-namespaced bridges;
  `fleet_coordinator.py` sends each robot a different `Twist` command
  (simple choreography, not full Nav2, to keep the demo's moving parts
  manageable) and logs both robots' odometry side by side, confirming
  they're independently addressable and not cross-talking.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write multi_robot_sim.launch.py**
- [ ] **Step 3: Write fleet_coordinator.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/19-multi-robot-systems/demo/multi_robot_sim.launch.py').read()); ast.parse(open('03-advanced/19-multi-robot-systems/demo/fleet_coordinator.py').read())"`
Expected: no output.

- [ ] **Step 5: Write demo/README.md**
- [ ] **Step 6: Commit**

```bash
git add 03-advanced/19-multi-robot-systems
git commit -m "Add Ch19: Multi-robot systems"
```

---

### Task 20: Chapter 20 — MuJoCo

**Files:**
- Create: `03-advanced/20-mujoco/OVERVIEW.md`
- Create: `03-advanced/20-mujoco/DEEP_DIVE.md`
- Create: `03-advanced/20-mujoco/demo/README.md`
- Create: `03-advanced/20-mujoco/demo/simple_arm.xml`
- Create: `03-advanced/20-mujoco/demo/run_sim.py`

**Content requirements:**
- OVERVIEW.md: what MuJoCo is (a fast, accurate physics engine
  originally built for robotics/biomechanics research and RL, now
  open-source and maintained by DeepMind/Google) and why it's mentioned
  alongside Gazebo/Isaac Sim — extremely fast contact/dynamics
  simulation, widely used as the physics backend for RL research
  (relevant heading into Chapter 22's Isaac Lab, which itself is built on
  a different but conceptually similar GPU physics engine, PhysX) even
  though it isn't ROS2-native the way Gazebo and Isaac Sim's bridges are.
- DEEP_DIVE.md must cover: **MJCF** (MuJoCo's own XML scene format —
  conceptually similar in purpose to URDF/SDF but MuJoCo-specific, not
  interchangeable with them directly, though URDF-to-MJCF conversion
  tools exist), the Python bindings (`mujoco` package — `mj_step()` for
  advancing physics, `mj_forward()` for computing derived quantities
  without advancing time, direct array access to positions/velocities
  `data.qpos`/`data.qvel` rather than a message-passing API — a notably
  different, lower-level programming style than ROS2's node/topic model),
  why MuJoCo is popular specifically for RL (its speed lets you run
  thousands of parallel simulated environments for policy training far
  faster than real-time, which is what actually makes RL training
  tractable — the same underlying need Isaac Lab, Chapter 22, addresses
  with GPU-parallelized PhysX instead), and the lack of a first-party
  ROS2 bridge (unlike Gazebo/Isaac Sim, connecting MuJoCo to ROS2
  requires a community bridge package or writing your own thin
  publishing layer — worth knowing as a practical limitation before
  reaching for MuJoCo in a ROS2-centric project); common pitfall:
  expecting MuJoCo's simulation loop to work like Gazebo/Isaac Sim's
  (subscribe to `/cmd_vel`, physics runs automatically) — MuJoCo's
  Python API is a library you call `mj_step()` on yourself inside your
  own loop, there's no implicit "running simulation" the way a
  ROS2-integrated simulator provides out of the box.
- Demo: `simple_arm.xml` — an MJCF version of the Chapter 5/12 2-3 joint
  arm concept (translated to MuJoCo's format, not literally converted
  from the URDF file); `run_sim.py` loads it with the `mujoco` Python
  package, steps physics in a loop applying a simple sinusoidal joint
  torque, and prints joint positions each step — demonstrating the
  direct `mj_step()`/`data.qpos` programming style described in
  DEEP_DIVE.md, with no ROS2 involved at all (consistent with the
  "no first-party ROS2 bridge" point above).

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write simple_arm.xml**
- [ ] **Step 3: Verify XML well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('03-advanced/20-mujoco/demo/simple_arm.xml')"`
Expected: no output.

- [ ] **Step 4: Write run_sim.py**
- [ ] **Step 5: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/20-mujoco/demo/run_sim.py').read())"`
Expected: no output.

- [ ] **Step 6: Write demo/README.md**
- [ ] **Step 7: Commit**

```bash
git add 03-advanced/20-mujoco
git commit -m "Add Ch20: MuJoCo"
```

---

### Task 21: Chapter 21 — Containerized robotics (Docker)

**Files:**
- Create: `03-advanced/21-containerized-robotics-docker/OVERVIEW.md`
- Create: `03-advanced/21-containerized-robotics-docker/DEEP_DIVE.md`
- Create: `03-advanced/21-containerized-robotics-docker/demo/README.md`
- Create: `03-advanced/21-containerized-robotics-docker/demo/Dockerfile`
- Create: `03-advanced/21-containerized-robotics-docker/demo/docker-compose.yaml`
- Create: `03-advanced/21-containerized-robotics-docker/demo/talker.py`
- Create: `03-advanced/21-containerized-robotics-docker/demo/listener.py`

**Content requirements:**
- OVERVIEW.md: what Docker containerization gives a robotics project
  (a reproducible environment — exact ROS2 distro, exact dependency
  versions — that runs identically on a dev laptop, a CI server, and a
  robot's onboard computer, instead of "works on my machine"), callback
  to Chapter 15's mention that Isaac ROS itself is distributed this way.
- DEEP_DIVE.md must cover: building a ROS2-based Docker image (a
  `FROM ros:jazzy` base, installing additional packages, copying in a
  workspace, `colcon build` inside the image), the layer caching model
  (why `COPY`/`RUN` order in a Dockerfile matters for build speed —
  put rarely-changing steps like apt installs before frequently-changing
  steps like copying your own source code, so Docker can reuse cached
  layers), running GUI ROS2 tools (RViz2, Gazebo) from inside a container
  (X11 forwarding basics — `--net=host` or explicit `DISPLAY`/`.Xauthority`
  passthrough — enough to know this is a solved-but-fiddly problem and
  where to look, not a full X11 tutorial), `docker-compose` for
  multi-container ROS2 systems (e.g. one container per major subsystem,
  matching how Chapter 19's multi-robot namespacing separates concerns,
  now separated at the container level too — all containers on ROS2's
  DDS layer still discover each other over the shared network the same
  way any two ROS2 processes would, since DDS discovery, per Chapter 10,
  doesn't care whether the two processes are in the same container);
  common pitfall: forgetting `--network host` (or equivalent
  docker-compose network config) and ending up with DDS discovery
  failing silently between containers on Docker's default bridge network,
  which isolates containers from each other's multicast traffic that DDS
  discovery relies on by default — yet another instance of the
  "everything looks fine, nothing connects" pattern from Chapters 2, 7,
  9, 10, and 14, now at the container-networking layer.
- Demo: a `Dockerfile` building a minimal ROS2 Jazyy image containing
  Chapter 2-style `talker.py`/`listener.py` copies; a
  `docker-compose.yaml` running talker in one container and listener in
  another, on a shared host-mode network so DDS discovery works between
  them, demonstrating the exact pitfall DEEP_DIVE.md describes being
  avoided correctly.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write talker.py and listener.py**

(Same Chapter 2 talker/listener pattern, copied here rather than
referenced, since this chapter's Dockerfile needs its own copy to build
from — cross-chapter file references don't work across a Docker build
context.)

- [ ] **Step 3: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('03-advanced/21-containerized-robotics-docker/demo/talker.py').read()); ast.parse(open('03-advanced/21-containerized-robotics-docker/demo/listener.py').read())"`
Expected: no output.

- [ ] **Step 4: Write Dockerfile**
- [ ] **Step 5: Write docker-compose.yaml**
- [ ] **Step 6: Verify docker-compose.yaml parses as YAML**

Run: `python3 -c "import yaml; yaml.safe_load(open('03-advanced/21-containerized-robotics-docker/demo/docker-compose.yaml'))"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Commit**

```bash
git add 03-advanced/21-containerized-robotics-docker
git commit -m "Add Ch21: Containerized robotics (Docker)"
```

---

### Task 22: Chapter 22 — Orchestrating robot fleets with Kubernetes; finalize Tier 3

**Files:**
- Create: `03-advanced/22-kubernetes-robot-fleets/OVERVIEW.md`
- Create: `03-advanced/22-kubernetes-robot-fleets/DEEP_DIVE.md`
- Create: `03-advanced/22-kubernetes-robot-fleets/demo/README.md`
- Create: `03-advanced/22-kubernetes-robot-fleets/demo/talker-deployment.yaml`
- Create: `03-advanced/22-kubernetes-robot-fleets/demo/listener-deployment.yaml`
- Create: `03-advanced/22-kubernetes-robot-fleets/demo/namespace.yaml`
- Create: `03-advanced/README.md` (new file, tier index)
- Modify: `README.md` (root — mark Tier 3 complete)

**Content requirements:**
- OVERVIEW.md: what Kubernetes adds beyond Chapter 21's single-machine
  Docker/docker-compose — running and managing many containers across
  *multiple* machines, automatically restarting failed containers,
  scheduling workloads onto available hardware — positioned specifically
  for **fleet-level** robotics use (a fleet of robots each reporting to
  or running workloads on a shared cluster, or a cluster managing
  simulation/training jobs at scale) rather than for the onboard software
  of a single robot (a single robot's own compute is usually just Docker,
  Chapter 21 — Kubernetes enters once you have many robots or many
  simulation jobs to manage as a fleet, which is why this chapter follows
  Docker rather than replacing it).
- DEEP_DIVE.md must cover: core Kubernetes vocabulary — **Pod** (one or
  more co-located containers, the smallest deployable unit, conceptually
  similar to a `docker-compose` service group but scheduled onto a
  cluster node rather than always your local machine), **Deployment**
  (declares "keep N replicas of this Pod running," handles
  restarting/rescheduling automatically if a Pod or node fails — the
  piece Chapter 21's docker-compose doesn't provide: self-healing),
  **Service** (a stable network identity for a set of Pods, since
  individual Pods come and go and get new IPs on restart), **Namespace**
  (Kubernetes' own namespace concept — distinct from but conceptually
  parallel to Chapter 19's ROS2 namespaces, used here to group this
  chapter's demo resources); why ROS2/DDS multi-machine discovery inside
  Kubernetes is a real practical hurdle (DDS's default discovery relies
  on multicast, which most Kubernetes cluster networking (CNI) setups
  don't pass through by default — forward-referencing Chapter 21's
  Docker networking pitfall at cluster scale — practical fixes include
  using a DDS discovery server/unicast configuration instead of relying
  on multicast, or a CNI plugin with multicast support; this is presented
  as "the thing to know to look up," not a full solved walkthrough, since
  it's genuinely still an area requiring careful setup); `kubectl` basics
  (`apply -f`, `get pods`, `logs`, `describe`) as the primary interaction
  tool, mirroring `ros2` CLI tools' role from earlier chapters; running a
  local cluster for learning purposes (`kind` or `minikube`) since most
  readers won't have a multi-machine cluster available; common pitfall:
  the multicast/DDS-discovery issue above being mistaken for "ROS2 is
  broken" when it's actually a cluster networking configuration gap —
  the same "check discovery/networking before assuming a ROS2 bug" lesson
  from Chapter 10 and 21, now one layer up the stack.
- Demo: `namespace.yaml` creates a `ros2-demo` namespace;
  `talker-deployment.yaml` and `listener-deployment.yaml` deploy Chapter
  21's Docker images (referencing the image built in Chapter 21's demo)
  as single-replica Deployments in that namespace, configured with
  `hostNetwork: true` (the Kubernetes equivalent of Chapter 21's
  `--network host`, and explicitly called out as such) so DDS discovery
  works between them on a local `kind`/`minikube` cluster without needing
  a full discovery-server setup — kept to the simplest configuration that
  actually works, with DEEP_DIVE.md explaining why production multi-node
  clusters need more than this.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write namespace.yaml**
- [ ] **Step 3: Write talker-deployment.yaml and listener-deployment.yaml**
- [ ] **Step 4: Verify all three YAML files parse**

Run: `python3 -c "import yaml; [yaml.safe_load(open(f)) for f in ['03-advanced/22-kubernetes-robot-fleets/demo/namespace.yaml','03-advanced/22-kubernetes-robot-fleets/demo/talker-deployment.yaml','03-advanced/22-kubernetes-robot-fleets/demo/listener-deployment.yaml']]"`
Expected: no output.

- [ ] **Step 5: Write demo/README.md**

Must include the exact `kind create cluster`, `docker build`/`kind load
docker-image`, and `kubectl apply -f` commands needed to run this demo
end to end, plus `kubectl logs` verification steps.

- [ ] **Step 6: Write 03-advanced/README.md**

Same structure as `01-beginner/README.md` / `02-intermediate/README.md`:
goal statement, prerequisites (Tier 2 complete; Chapters 15-16
additionally need Isaac Sim/Isaac ROS on an NVIDIA GPU; Chapters 21-22
need Docker and, for Ch22, a local Kubernetes tool like `kind`), numbered
list of all 7 chapters with one-line descriptions.

- [ ] **Step 7: Update root README.md**

Change the Tier 3 line from "(in progress)" to "— complete", link to
`03-advanced/README.md`, matching the Tier 1/2 pattern.

- [ ] **Step 8: Commit**

```bash
git add 03-advanced/22-kubernetes-robot-fleets 03-advanced/README.md README.md
git commit -m "Add Ch22: Kubernetes robot fleets; complete Tier 3 (advanced)"
```

---

## Self-Review Notes

- Spec coverage: all 7 Tier 3 chapters from the amended spec (Isaac ROS,
  synthetic data, advanced Nav2, advanced MoveIt2, multi-robot, MuJoCo,
  Docker, Kubernetes) have a task — 8 tasks total since Docker and
  Kubernetes are separate chapters (21 and 22) per the spec amendment
  adding Kubernetes after Docker.
- Language policy: only Chapter 15 (Isaac ROS) has a C++ demo, matching
  the spec's language policy (C++ reserved for Ch2, 3, 15, 26).
- Cross-chapter continuity: Ch17 extends Ch11's Nav2 stack; Ch18 extends
  Ch12's arm; Ch19 extends Ch7's diff-drive robot; Ch21's Docker demo
  reuses the Ch2 talker/listener pattern (copied, not referenced, for
  Docker build-context reasons — noted explicitly in Task 21); Ch22's
  Kubernetes demo reuses Ch21's Docker images directly.
- Recurring pitfall thread: the "looks fine, nothing connects" lesson
  (topic name/type mismatch in Ch2, QoS in Ch10, bridge topics in Ch7/9,
  extensions in Ch13/14) is explicitly continued into Ch21 (container
  networking/multicast) and Ch22 (cluster networking/multicast) rather
  than presented as an unrelated new problem each time — reinforces the
  curriculum's running diagnostic habit ("check networking/discovery
  first") at increasing levels of infrastructure complexity.
- No placeholders: every task specifies exact file paths and concrete
  content outlines; verification steps are syntax/structure checks
  runnable without ROS2/Isaac Sim/Docker/Kubernetes installed, consistent
  with prior tiers' Adaptation Notes.
