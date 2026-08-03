# Demo: Verify your ROS2 install

## What this does

`verify_install.sh` runs a handful of independent checks against your
ROS2 install and prints a PASS/FAIL line for each one, so you can see
everything that's wrong (if anything) in one pass instead of chasing
errors one at a time.

## How to run

```bash
bash verify_install.sh
```

(or `./verify_install.sh` if you want to rely on its executable bit and
shebang line).

## Expected output

If your install and workspace from DEEP_DIVE.md are set up correctly:

```
=== ROS2 install verification ===
[PASS] 'ros2' command found on PATH
[PASS] ROS_DISTRO is set to 'jazzy'
[PASS] ros2 pkg list found 412 packages
[PASS] ROS_DOMAIN_ID is set to '42'
=== Done ===
```

(Your package count will differ depending on exactly what's installed —
anything above ~50 is healthy.)

If you see a `[FAIL]` line, the message tells you what to fix — usually
"re-source setup.bash" or "re-run the apt install steps in DEEP_DIVE.md."
