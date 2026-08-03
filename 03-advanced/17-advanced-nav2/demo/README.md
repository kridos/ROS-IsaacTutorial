# Demo: Advanced Nav2 — Custom Behavior Tree

## Prerequisites

Same as Chapter 11, plus its map already generated:

```bash
python3 ../../../02-intermediate/11-nav2-basics/demo/generate_empty_map.py
```

(Run once — writes `empty_map.pgm`/`.yaml` into Chapter 11's demo
directory, which this chapter's launch file reads from directly.)

Also requires `pyyaml` (`pip install pyyaml`, likely already present —
used by `nav2_custom_bt.launch.py` to merge params files).

## How to run

```bash
ros2 launch nav2_custom_bt.launch.py
```

Same startup as Chapter 11's demo, but `bt_navigator` loads
`custom_bt.xml` instead of Nav2's stock tree — confirm this took effect:

```bash
ros2 param get /bt_navigator default_nav_to_pose_bt_xml
```

Expected: prints a path ending in `.../17-advanced-nav2/demo/custom_bt.xml`.

## Give AMCL an initial pose

Same as Chapter 11 — use RViz2's "2D Pose Estimate" tool first.

## Send a goal and watch the timing

```bash
python3 wait_and_retry_node.py 1.5 1.5
```

Expected, if the path is clear: normal navigation, feedback logged every
tick with steadily-decreasing distance, same shape as Chapter 11.

## See the custom recovery in action

Send a goal that requires navigating through a spot you've temporarily
blocked (e.g. add a `<model>` obstacle box to the empty world's SDF, or
in RViz2 use "Publish Point" tools if your Nav2 config supports manual
costmap marking) so the controller reports failure and `RecoveryNode`
triggers.

Expected: after a `FollowPath` failure, `wait_and_retry_node.py`'s log
shows a roughly 5-6 second gap between feedback updates with
`distance_remaining` unchanged (the `Wait wait_duration="5.0"` step from
`custom_bt.xml`), followed by feedback resuming as the robot backs up and
retries — noticeably slower-cycling than Nav2's stock recovery, which is
exactly the tuning difference `custom_bt.xml`'s header comment describes.

## Compare directly against the stock tree

Run Chapter 11's `nav2_sim.launch.py` (stock tree) against the same
blocked-path scenario and compare the feedback timing in
`send_goal.py`'s log vs. this chapter's `wait_and_retry_node.py` log —
the stock tree's recovery should cycle noticeably faster between attempts.
