# Practice: Advanced Nav2 (Custom Behavior Trees)

1. **Tune the patience.** Change `custom_bt.xml`'s `Wait wait_duration`
   from 5.0 to 15.0 seconds, re-run `wait_and_retry_node.py` against a
   blocked path, and confirm the timing gap in the log grows to match —
   direct evidence you're actually controlling the tree, not just
   reading about it.

2. **A third recovery strategy.** Add a `Spin` node (rotate in place) to
   `custom_bt.xml`'s recovery `Sequence`, between `Wait` and `BackUp`,
   and update `wait_and_retry_node.py`'s comments/expectations to match
   the new timing.

3. **Read the stock tree side by side.** Find Nav2's actual installed
   `navigate_to_pose_w_replanning_and_recovery.xml` on your system
   (typically under the `nav2_bt_navigator` package share directory) and
   annotate it, node by node, using DEEP_DIVE.md's vocabulary — confirm
   your annotation matches DEEP_DIVE.md's summary of its structure.

4. **Break a node name on purpose.** Introduce a typo in one of
   `custom_bt.xml`'s node tag names (e.g. `<BackUpp>` instead of
   `<BackUp>`) and confirm `bt_navigator` fails to start with the error
   DEEP_DIVE.md's common pitfall describes.

5. **Stretch:** write a *third* custom tree that gives up after only 1
   retry (aggressive, impatient) instead of this chapter's patient one,
   and compare mission completion time vs. failure rate between the two
   strategies across several blocked-path test runs — an actual
   comparison, not just a description of the trade-off.
