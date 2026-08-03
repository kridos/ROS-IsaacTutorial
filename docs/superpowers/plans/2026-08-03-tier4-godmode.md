# Tier 4 (God Mode) Curriculum Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Adaptation note:** Same as Tier 1/2/3 plans — this builds tutorial
> content, not a tested library. "Tests" mean syntax/structure checks
> runnable without Isaac Sim/Isaac Lab/GR00T/TensorRT installed (this
> authoring machine has none of them), plus documented expected output
> in each `demo/README.md`. Where a dependency is genuinely
> pip-installable and lightweight (as MuJoCo was in Tier 3), prefer
> actually installing it in an isolated venv/conda env (never the global
> Python) and running the demo for real — do this only when the
> dependency is actually light enough to be practical; do not attempt it
> for GPU-bound frameworks (Isaac Lab, GR00T, TensorRT) that have no
> realistic path to running on this machine.

**Goal:** Build all 6 chapters of Tier 4 (God Mode): Isaac Lab
fundamentals, training a policy, sim-to-real transfer, Isaac GR00T,
GPU-accelerated custom perception (TensorRT), and a capstone project
integrating navigation, manipulation, perception, and simulation from
across the whole curriculum.

**Architecture:** One directory per chapter under `04-godmode/`,
numbered `23-...` through `28-...`, continuing Tier 1/2/3's numbering
(as amended when the Kubernetes chapter was inserted into Tier 3). Same
`OVERVIEW.md` / `DEEP_DIVE.md` / `demo/` shape.

**Tech Stack:** Isaac Lab (built on Isaac Sim + PhysX, GPU-parallelized
RL environments), Isaac GR00T (NVIDIA's humanoid foundation model
stack), TensorRT (C++ + Python), and a capstone tying together Nav2
(Ch11/17), MoveIt2 (Ch12/18), Isaac ROS perception (Ch15), and Isaac Sim
(Ch13/14).

## Global Constraints

- Directory layout, file naming, doc-depth rules: identical to Tier
  1/2/3 Global Constraints.
- Chapter numbering: 23-28, matching the amended spec at
  `docs/superpowers/specs/2026-08-02-ros2-isaac-curriculum-design.md`.
- Chapter 26 (GPU perception w/ TensorRT) is Python + C++ per the spec's
  language policy — the only Tier 4 chapter with a C++ demo.
- Every task ends with a git commit.

---

### Task 23: Chapter 23 — Isaac Lab fundamentals (RL environments)

**Files:**
- Create: `04-godmode/23-isaac-lab-fundamentals/OVERVIEW.md`
- Create: `04-godmode/23-isaac-lab-fundamentals/DEEP_DIVE.md`
- Create: `04-godmode/23-isaac-lab-fundamentals/demo/README.md`
- Create: `04-godmode/23-isaac-lab-fundamentals/demo/cartpole_env_demo.py`

**Content requirements:**
- OVERVIEW.md: what Isaac Lab is (NVIDIA's RL framework built on Isaac
  Sim/PhysX, successor to Isaac Gym) — GPU-parallelized simulation
  running thousands of environment instances simultaneously on one GPU,
  positioned as the same "simulation needs to be fast enough to train
  on" problem Chapter 20's MuJoCo discussion raised, solved here via
  GPU parallelism instead of MuJoCo's CPU speed.
- DEEP_DIVE.md must cover: the **vectorized environment** concept — Isaac
  Lab doesn't run one simulation and step it repeatedly (Chapter 20's
  MuJoCo pattern); it runs N identical environments in parallel on the
  GPU, all stepped together in one call, returning batched
  observations/rewards/dones as tensors (shape `[num_envs, ...]`) rather
  than single values — this is the core mechanical difference from every
  earlier chapter's simulation code; the **Gym-style RL environment
  interface** (`reset()`, `step(action)` returning
  `observation, reward, terminated, truncated, info`) that Isaac Lab
  environments implement, standard across the RL ecosystem (not
  Isaac-specific) so RL algorithms/libraries written against this
  interface work with Isaac Lab environments largely unchanged;
  **ManagerBasedEnv** / task configuration (Isaac Lab structures an
  environment's observation space, action space, reward terms, and
  termination conditions as separate configurable "manager" components
  rather than one monolithic environment class — useful because it lets
  you swap one piece, e.g. the reward function, without rewriting the
  whole environment); common pitfall: writing RL environment code as if
  `num_envs=1` (indexing tensors as scalars, using Python control flow
  per-environment) breaks or silently misbehaves at any `num_envs > 1` —
  Isaac Lab code needs to be written in a vectorized (tensor-batched)
  style from the start, not retrofitted for parallelism later.
- Demo: `cartpole_env_demo.py` — loads Isaac Lab's built-in CartPole
  environment (a standard, simple RL benchmark task — balance a pole on
  a cart by applying force) with a small `num_envs` (e.g. 4, small enough
  to reason about individually), runs it with random actions for a fixed
  number of steps, and prints the batched observation/reward tensors'
  shapes and a couple of sample values each step — making the vectorized
  batch-of-environments shape concrete rather than abstract.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write cartpole_env_demo.py**
- [ ] **Step 3: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('04-godmode/23-isaac-lab-fundamentals/demo/cartpole_env_demo.py').read())"`
Expected: no output.

- [ ] **Step 4: Write demo/README.md**
- [ ] **Step 5: Commit**

```bash
git add 04-godmode/23-isaac-lab-fundamentals
git commit -m "Add Ch23: Isaac Lab fundamentals (RL environments)"
```

---

### Task 24: Chapter 24 — Training a locomotion/manipulation policy in Isaac Lab

**Files:**
- Create: `04-godmode/24-training-a-policy/OVERVIEW.md`
- Create: `04-godmode/24-training-a-policy/DEEP_DIVE.md`
- Create: `04-godmode/24-training-a-policy/demo/README.md`
- Create: `04-godmode/24-training-a-policy/demo/train_cartpole_ppo.py`
- Create: `04-godmode/24-training-a-policy/demo/play_trained_policy.py`

**Content requirements:**
- OVERVIEW.md: what "training a policy" means concretely (using
  Chapter 23's environment plus an RL algorithm to learn a
  neural-network controller that maximizes reward through many episodes
  of trial and error), continuing the CartPole task from Chapter 23 into
  an actual trained result rather than random actions.
- DEEP_DIVE.md must cover: **PPO** (Proximal Policy Optimization) at a
  conceptual level — a widely-used RL algorithm that alternates
  collecting experience (running the current policy in the environment,
  Chapter 23's vectorized step loop) with updating the policy's neural
  network weights to favor actions that led to higher reward, using a
  "proximal"/clipped update rule specifically to avoid the policy
  changing so drastically in one update that training becomes unstable
  — enough to understand what the training loop is doing without a full
  derivation; **RL library integration** (Isaac Lab ships integration
  with existing RL libraries — rsl_rl, stable-baselines3, or similar,
  depending on version — rather than reimplementing PPO itself, matching
  the broader theme of building on established tools rather than
  reinventing them, echoing Nav2/MoveIt2's role in earlier chapters);
  reading training progress (reward curves climbing over training
  iterations as the核心 signal that learning is happening — via
  TensorBoard or the training script's own console output); the
  train/evaluate split (`train_*.py` runs training and saves a
  checkpoint; a separate `play_*.py`-style script loads that checkpoint
  and runs the trained policy without further learning, to actually
  observe what was learned); common pitfall: reward function design
  mistakes causing "reward hacking" — a policy that maximizes the
  literal reward signal in some unintended, degenerate way (a classic RL
  problem, not Isaac-Lab-specific) rather than actually solving the
  intended task, and how a climbing reward curve alone doesn't
  guarantee genuinely good behavior — worth watching the trained
  policy's actual behavior (Chapter 24's `play_trained_policy.py`), not
  just the training curve.
- Demo: `train_cartpole_ppo.py` runs a short PPO training session
  (deliberately short — enough iterations to see the reward curve start
  climbing, not a full convergence run that would take much longer than
  reasonable for a learning demo) against Chapter 23's CartPole
  environment, saving a checkpoint; `play_trained_policy.py` loads that
  checkpoint and runs the trained policy for a fixed number of episodes,
  printing per-episode total reward so the reader can compare against
  Chapter 23's random-action baseline.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write train_cartpole_ppo.py**
- [ ] **Step 3: Write play_trained_policy.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('04-godmode/24-training-a-policy/demo/train_cartpole_ppo.py').read()); ast.parse(open('04-godmode/24-training-a-policy/demo/play_trained_policy.py').read())"`
Expected: no output.

- [ ] **Step 5: Write demo/README.md**
- [ ] **Step 6: Commit**

```bash
git add 04-godmode/24-training-a-policy
git commit -m "Add Ch24: Training a policy in Isaac Lab (PPO)"
```

---

### Task 25: Chapter 25 — Sim-to-real transfer techniques

**Files:**
- Create: `04-godmode/25-sim-to-real-transfer/OVERVIEW.md`
- Create: `04-godmode/25-sim-to-real-transfer/DEEP_DIVE.md`
- Create: `04-godmode/25-sim-to-real-transfer/demo/README.md`
- Create: `04-godmode/25-sim-to-real-transfer/demo/domain_randomized_env_config.py`
- Create: `04-godmode/25-sim-to-real-transfer/demo/deploy_policy_ros2_node.py`

**Content requirements:**
- OVERVIEW.md: the **reality gap** — a policy trained purely in
  simulation (Chapter 24) usually performs worse, or fails outright, on
  the real robot, because simulation is never a perfect physical match
  (friction, sensor noise, actuator dynamics, latency all differ) — this
  chapter covers the standard techniques for closing that gap.
- DEEP_DIVE.md must cover: **domain randomization for dynamics** (not
  just Chapter 16's visual randomization for perception — randomizing
  *physical* simulation parameters during training: friction
  coefficients, mass, motor strength, sensor noise/latency, so the
  trained policy is robust to not knowing the real values exactly rather
  than overfitting to simulation's exact physics — the RL-training
  analogue of Chapter 16's "quantity without diversity" pitfall, now
  applied to physics parameters instead of visuals); **system
  identification** (measuring your real robot's actual physical
  parameters — motor response curves, real friction — so simulation can
  be calibrated closer to reality rather than relying on domain
  randomization's brute-force robustness alone; the two techniques are
  complementary, not either/or); **observation/action space matching**
  (the trained policy's inputs and outputs must exactly match what the
  real robot can actually sense and command — a policy trained assuming
  perfect, noiseless joint position feedback will struggle if the real
  robot's encoders are noisier or lower-rate than simulation assumed);
  **deploying a trained policy as a ROS2 node** (wrapping the trained
  neural network — same checkpoint format from Chapter 24 — inside a
  plain rclpy node that subscribes to real sensor topics, runs inference
  each control cycle, and publishes commands, tying the RL-trained
  policy back into the ROS2 node/topic model every other chapter has
  used); common pitfall: control frequency mismatch — a policy trained
  at simulation's control rate (e.g. 50 Hz) deployed at a different rate
  on real hardware (a different loop rate, or one with variable timing
  due to real-world jitter) can behave very differently than in training,
  since the policy implicitly learned a relationship between actions and
  their effects at a specific timestep — matching training and
  deployment control rates as closely as possible is a frequently
  overlooked requirement, not an optional tuning detail.
- Demo: `domain_randomized_env_config.py` — extends Chapter 24's
  CartPole training setup with dynamics randomization (randomized pole
  mass and cart friction each episode, illustrating the technique
  concretely on a task simple enough to reason about); a plain rclpy
  node, `deploy_policy_ros2_node.py`, loading a trained-policy checkpoint
  (Chapter 24's output) and running inference against
  simulated/placeholder sensor input published on a ROS2 topic, publishing
  a resulting command topic — demonstrating the "wrap the policy as a
  ROS2 node" deployment pattern end to end, independent of Isaac Sim
  being involved at inference time (the ROS2 node itself has no Isaac
  Sim import, mirroring Chapter 20's MuJoCo demo's "no ROS2 dependency at
  the simulation layer" but inverted — no simulation dependency at the
  deployed-node layer).

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write domain_randomized_env_config.py**
- [ ] **Step 3: Write deploy_policy_ros2_node.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('04-godmode/25-sim-to-real-transfer/demo/domain_randomized_env_config.py').read()); ast.parse(open('04-godmode/25-sim-to-real-transfer/demo/deploy_policy_ros2_node.py').read())"`
Expected: no output.

- [ ] **Step 5: Write demo/README.md**
- [ ] **Step 6: Commit**

```bash
git add 04-godmode/25-sim-to-real-transfer
git commit -m "Add Ch25: Sim-to-real transfer techniques"
```

---

### Task 26: Chapter 26 — Isaac GR00T foundation models

**Files:**
- Create: `04-godmode/26-isaac-groot/OVERVIEW.md`
- Create: `04-godmode/26-isaac-groot/DEEP_DIVE.md`
- Create: `04-godmode/26-isaac-groot/demo/README.md`
- Create: `04-godmode/26-isaac-groot/demo/groot_inference_demo.py`

**Content requirements:**
- OVERVIEW.md: what Isaac GR00T is (NVIDIA's foundation model stack for
  humanoid/general robot manipulation — a large, pre-trained
  vision-language-action model that can be fine-tuned for specific
  robots/tasks, rather than training a task-specific policy entirely
  from scratch the way Chapters 23-24 did), positioned as the "god mode"
  end of the curriculum's spectrum: from Chapter 24's from-scratch
  narrow-task RL policy to a large pre-trained model adaptable across
  tasks and embodiments.
- DEEP_DIVE.md must cover: the **foundation model** concept for
  robotics — trained on large, diverse datasets (real + synthetic,
  connecting back to Chapter 16's synthetic data generation as one
  source such models are trained on) across many robots/tasks, so a
  single pre-trained model has broad, transferable capability, and
  fine-tuning it for a new specific task/robot needs far less
  task-specific data than training from scratch (Chapter 24's approach)
  — the same "foundation model then fine-tune" pattern from large
  language models, applied to robot control; GR00T's **vision-language-
  action** structure at a high level (takes in visual observations and
  potentially language instructions, outputs robot actions — bridging
  perception, Chapter 15, and language-level task specification, an
  active research direction distinct from most of this curriculum's
  hand-coded task logic); **fine-tuning workflow** (starting from a
  released GR00T checkpoint, fine-tuning on a smaller robot/task-specific
  dataset — conceptually parallel to Chapter 24's checkpoint
  save/load pattern, but starting from a large pre-trained checkpoint
  instead of random initialization); common pitfall: treating a
  foundation model as a drop-in replacement requiring zero
  robot-specific work — embodiment differences (a different robot's
  exact joint layout, camera placement, action space) still typically
  need some fine-tuning or adaptation layer, not just prompting a
  pretrained model and expecting it to work unmodified on a
  never-seen-before robot.
- Demo: `groot_inference_demo.py` — loads a GR00T checkpoint (exact
  loading API/checkpoint source per NVIDIA's current GR00T release —
  this script documents the pattern: load model, construct an
  observation matching its expected input format from a camera image
  plus a text instruction, run one inference step, print the resulting
  action output's shape/values) — a minimal, single-inference-step
  script establishing the input/output shape of working with GR00T,
  deliberately not a full fine-tuning pipeline (out of scope for a single
  demo chapter, noted explicitly in the script/README).

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write groot_inference_demo.py**
- [ ] **Step 3: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('04-godmode/26-isaac-groot/demo/groot_inference_demo.py').read())"`
Expected: no output.

- [ ] **Step 4: Write demo/README.md**
- [ ] **Step 5: Commit**

```bash
git add 04-godmode/26-isaac-groot
git commit -m "Add Ch26: Isaac GR00T foundation models"
```

---

### Task 27: Chapter 27 — GPU-accelerated custom perception (TensorRT)

**Files:**
- Create: `04-godmode/27-gpu-perception-tensorrt/OVERVIEW.md`
- Create: `04-godmode/27-gpu-perception-tensorrt/DEEP_DIVE.md`
- Create: `04-godmode/27-gpu-perception-tensorrt/demo/README.md`
- Create: `04-godmode/27-gpu-perception-tensorrt/demo/python/build_engine.py`
- Create: `04-godmode/27-gpu-perception-tensorrt/demo/python/run_inference.py`
- Create: `04-godmode/27-gpu-perception-tensorrt/demo/cpp/src/tensorrt_inference_node.cpp`
- Create: `04-godmode/27-gpu-perception-tensorrt/demo/cpp/CMakeLists.txt`
- Create: `04-godmode/27-gpu-perception-tensorrt/demo/cpp/package.xml`

**Content requirements:**
- OVERVIEW.md: what TensorRT is (NVIDIA's inference optimization
  library/runtime — takes a trained neural network and compiles it into
  a highly optimized, hardware-specific execution plan for fast
  inference), why building your own TensorRT-accelerated node matters
  beyond using Isaac ROS's pre-built ones (Chapter 15) — custom
  perception models (a model you trained yourself, not one of Isaac
  ROS's built-in pipelines) still benefit from the same optimized
  inference path.
- DEEP_DIVE.md must cover: the **build vs. runtime** split — an
  **engine** (TensorRT's compiled, optimized representation of a network,
  specific to the exact GPU/TensorRT version it was built on — not
  portable across different GPUs the way the original trained model
  file is) is built once (often slow, minutes) from a trained model
  (commonly via ONNX as an intermediate exchange format), then loaded
  and run repeatedly at inference time (fast, the whole point); **ONNX**
  (Open Neural Network Exchange) as the common bridge format — a model
  trained in PyTorch/TensorFlow is typically exported to ONNX first,
  then TensorRT builds an engine from that ONNX file, rather than
  TensorRT consuming framework-specific model files directly;
  **precision modes** (FP32 full precision, FP16 half precision, INT8
  quantized — each trading numerical precision for speed/memory, with
  FP16 commonly a "free" speedup with negligible accuracy loss on modern
  GPUs, and INT8 needing a calibration step against representative data
  to preserve accuracy); wrapping a TensorRT engine in a ROS2 node
  (allocate GPU input/output buffers once at startup, then per-message:
  copy input data to GPU, run inference, copy result back, publish) —
  connecting this chapter's low-level TensorRT work back to the
  NITROS/zero-copy discussion from Chapter 15 (a hand-written node like
  this one doesn't get NITROS's zero-copy transport automatically; that
  requires implementing the NITROS-compatible interface specifically,
  noted as a known limitation of a simple hand-written node rather than
  something to solve in this demo); common pitfall: rebuilding an engine
  file on a different GPU model/TensorRT version than it was built for —
  engines are not portable the way ONNX files are, and loading a
  mismatched engine typically fails outright or, worse, behaves
  incorrectly rather than failing clearly, so always rebuild the engine
  on (or matching) the target deployment hardware rather than copying a
  pre-built engine file between different GPUs.
- Demo: `build_engine.py` (Python) takes a small ONNX model (a trivial
  placeholder classifier is fine — the point is the build process, not
  the model's usefulness) and builds a TensorRT engine file from it,
  demonstrating the build step and FP16 precision mode; `run_inference.py`
  (Python) loads that engine and runs inference on a sample input,
  printing the output and measured inference latency;
  `tensorrt_inference_node.cpp` (C++, this chapter's language-policy C++
  demo, since production perception inference nodes are exactly the
  case where C++ matters) wraps the same engine in a ROS2 node
  subscribing to an image topic and publishing an inference result
  topic, following the buffer-allocation pattern DEEP_DIVE.md describes.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write build_engine.py**
- [ ] **Step 3: Write run_inference.py**
- [ ] **Step 4: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('04-godmode/27-gpu-perception-tensorrt/demo/python/build_engine.py').read()); ast.parse(open('04-godmode/27-gpu-perception-tensorrt/demo/python/run_inference.py').read())"`
Expected: no output.

- [ ] **Step 5: Write tensorrt_inference_node.cpp, CMakeLists.txt, package.xml**
- [ ] **Step 6: Verify package.xml is well-formed XML**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('04-godmode/27-gpu-perception-tensorrt/demo/cpp/package.xml')"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Commit**

```bash
git add 04-godmode/27-gpu-perception-tensorrt
git commit -m "Add Ch27: GPU-accelerated custom perception (TensorRT)"
```

---

### Task 28: Chapter 28 — Capstone: autonomous mobile manipulator; finalize Tier 4

**Files:**
- Create: `04-godmode/28-capstone-mobile-manipulator/OVERVIEW.md`
- Create: `04-godmode/28-capstone-mobile-manipulator/DEEP_DIVE.md`
- Create: `04-godmode/28-capstone-mobile-manipulator/demo/README.md`
- Create: `04-godmode/28-capstone-mobile-manipulator/demo/mobile_manipulator.urdf.xacro`
- Create: `04-godmode/28-capstone-mobile-manipulator/demo/capstone_sim.launch.py`
- Create: `04-godmode/28-capstone-mobile-manipulator/demo/mission_coordinator.py`
- Create: `04-godmode/04-godmode/README.md` — NOTE: corrected below to `04-godmode/README.md`
- Modify: `README.md` (root — mark Tier 4 complete)

**Content requirements:**
- OVERVIEW.md: the capstone integrates the curriculum's major threads
  into one task: a mobile robot (Chapter 7's diff-drive base) with an
  arm mounted on it (Chapter 12's arm) that navigates to a location
  (Nav2, Chapter 11/17), perceives a target object (simulated
  perception, Chapters 9/15's concepts), and picks it up (MoveIt2,
  Chapter 12/18) — framed explicitly as "everything else in this
  curriculum, composed into one mission" rather than teaching new
  concepts.
- DEEP_DIVE.md must cover: **mobile manipulation architecture** — how a
  combined mobile base + arm robot's URDF differs from either alone (the
  arm's base link becomes a child of the mobile base's chassis rather
  than a fixed world frame, so the whole arm's kinematic chain moves with
  robot navigation — a direct, concrete consequence of TF's tree
  structure from Chapter 8, now with a moving root for the arm's subtree);
  running Nav2 and MoveIt2 **simultaneously against the same robot**
  (each needs its own costmap/planning-scene view of the world, and
  they must agree on where the robot's arm is when the base is
  navigating with the arm in a stowed vs. extended configuration, since
  an extended arm changes the robot's effective footprint for
  navigation's obstacle-avoidance purposes — a real integration detail
  neither Chapter 11 nor Chapter 12 needed to consider alone); the
  **mission coordinator** pattern (a top-level node sequencing
  "navigate to pickup location" (Nav2 action) -> "detect and localize
  target object" (simplified/simulated perception step) -> "pick it up"
  (MoveIt2 pick sequence, Chapter 18's pattern) -> "navigate to drop-off
  location" -> "place it" (Chapter 18's place sequence) — itself a small
  behavior tree or straightforward state machine, tying back to Chapter
  17's behavior tree concepts at the mission level rather than Nav2's
  internal navigation level); common pitfall: forgetting to stow the arm
  before navigating, or coordinate the arm's currently-extended pose with
  Nav2's costmap footprint — since Nav2's costmap (Chapter 11) doesn't
  automatically know about the arm's real-time pose unless explicitly
  told, an extended arm can clip an obstacle Nav2's planner didn't know
  to avoid; this is the culminating instance of a "component works fine
  in isolation, but integration requires explicit coordination" lesson
  that's been building since Chapter 19's multi-robot namespacing and
  Chapter 21/22's networking pitfalls.
- Demo: `mobile_manipulator.urdf.xacro` — combines Chapter 7's diff-drive
  chassis with Chapter 12's 3-joint arm mounted on top (arm's base_link
  becomes a fixed-joint child of the chassis, not a separate root);
  `capstone_sim.launch.py` starts Gazebo, spawns the combined robot,
  bridges topics, and brings up both Nav2 (Chapter 11 pattern) and
  MoveIt2 (Chapter 12 pattern) against it simultaneously;
  `mission_coordinator.py` runs the full pickup-and-deliver mission
  described above, logging each stage, using a hardcoded/simulated
  "target object detected at this pose" step in place of a full
  perception pipeline (explicitly noted as a simplification — real
  object detection is Chapters 15/16/27's territory, not re-implemented
  here) so the capstone's own complexity stays focused on integration
  rather than re-deriving perception.

- [ ] **Step 1: Write OVERVIEW.md and DEEP_DIVE.md**
- [ ] **Step 2: Write mobile_manipulator.urdf.xacro**
- [ ] **Step 3: Verify XML well-formed**

Run: `python3 -c "import xml.dom.minidom as m; m.parse('04-godmode/28-capstone-mobile-manipulator/demo/mobile_manipulator.urdf.xacro')"`
Expected: no output.

- [ ] **Step 4: Write capstone_sim.launch.py**
- [ ] **Step 5: Write mission_coordinator.py**
- [ ] **Step 6: Verify Python syntax**

Run: `python3 -c "import ast; ast.parse(open('04-godmode/28-capstone-mobile-manipulator/demo/capstone_sim.launch.py').read()); ast.parse(open('04-godmode/28-capstone-mobile-manipulator/demo/mission_coordinator.py').read())"`
Expected: no output.

- [ ] **Step 7: Write demo/README.md**
- [ ] **Step 8: Write 04-godmode/README.md**

Same structure as prior tier READMEs: goal statement, prerequisites
(Tier 3 complete; Chapters 23-26 need Isaac Sim/Isaac Lab/GR00T on an
NVIDIA GPU; Chapter 27 needs TensorRT; Chapter 28's capstone needs
everything Tiers 1-3 needed for Gazebo/Nav2/MoveIt2), numbered list of
all 6 chapters with one-line descriptions, and a closing note that
Chapter 28 is the curriculum's final chapter.

- [ ] **Step 9: Update root README.md**

Change the Tier 4 line from "(in progress)" to "— complete", link to
`04-godmode/README.md`, matching the Tier 1/2/3 pattern. Add a short
closing line noting the curriculum (all 28 chapters) is now complete.

- [ ] **Step 10: Commit**

```bash
git add 04-godmode/28-capstone-mobile-manipulator 04-godmode/README.md README.md
git commit -m "Add Ch28: Capstone (mobile manipulator); complete Tier 4 (god mode) and the curriculum"
```

---

## Self-Review Notes

- Spec coverage: all 6 Tier 4 chapters from the amended spec (Isaac Lab
  fundamentals, training a policy, sim-to-real transfer, Isaac GR00T,
  GPU perception w/ TensorRT, capstone) have a task.
- Language policy: only Chapter 27 (TensorRT) has a C++ demo, matching
  the spec's language policy (C++ reserved for Ch2, 3, 15, 27 — the
  chapter originally specified as 26 in the initial spec draft is now
  27 after the Kubernetes chapter insertion shifted Tier 4 numbering by
  one; this plan uses the corrected numbers 23-28 throughout).
- Cross-chapter continuity: Ch24 extends Ch23's CartPole env; Ch25
  extends Ch24's training setup and deploys via a plain ROS2 node (no
  simulator dependency at deploy time, deliberately mirroring but
  inverting Ch20's MuJoCo "no ROS2 dependency" framing); Ch27 connects
  back to Ch15's NITROS discussion explicitly; Ch28 integrates Ch7
  (chassis), Ch8 (TF tree with moving root), Ch11/17 (Nav2), Ch12/18
  (MoveIt2), and notes Ch15/16/27 as where real perception would plug in
  rather than re-deriving it.
- Fixed a typo in the original file list draft (duplicated
  `04-godmode/04-godmode/README.md` path) — corrected to
  `04-godmode/README.md` in Task 28's Step 8, matching Tier 1/2/3's
  `NN-tier/README.md` convention.
- No placeholders: every task specifies exact file paths and concrete
  content outlines; verification steps are syntax/structure checks
  runnable without Isaac Sim/Isaac Lab/GR00T/TensorRT installed,
  consistent with prior tiers' Adaptation Notes — with an explicit note
  to actually run/verify anything genuinely lightweight (as Tier 3 did
  for MuJoCo), in an isolated venv per the user's stated preference.
