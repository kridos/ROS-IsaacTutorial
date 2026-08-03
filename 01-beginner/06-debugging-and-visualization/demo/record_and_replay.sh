#!/usr/bin/env bash
#
# record_and_replay.sh — walks through the full ros2 bag record -> play
# -> echo loop against noisy_sensor_publisher.py's /sensor/reading topic.
#
# This script is meant to be read and run step-by-step (or copy-pasted
# into a terminal), not executed unattended — recording and playback are
# separate, interactive phases you'd normally run in different terminals.
# It prints each step so you can follow along even if you just read the
# output instead of running it.

set -uo pipefail
# Deliberately NOT using -e here: if `ros2 bag record` is interrupted with
# Ctrl+C (the normal way to stop a recording), that shows up as a
# non-zero exit code, and -e would abort this script right there instead
# of continuing on to the info/play steps.

BAG_DIR="./sensor_recording"

echo "Step 1: In another terminal, run:"
echo "    python3 noisy_sensor_publisher.py"
echo

echo "Step 2: Recording ${BAG_DIR} for 10 seconds..."
# --duration or an explicit `timeout` wrapper (used here) both stop the
# recording automatically instead of requiring a manual Ctrl+C, which
# makes this script runnable non-interactively for a fixed capture window.
rm -rf "${BAG_DIR}"
timeout 10s ros2 bag record /sensor/reading -o "${BAG_DIR}"

echo
echo "Step 3: Inspecting the recording..."
ros2 bag info "${BAG_DIR}"

echo
echo "Step 4: Replaying it. In another terminal, run:"
echo "    ros2 topic echo /sensor/reading"
echo "Then in this terminal:"
echo "    ros2 bag play ${BAG_DIR}"
echo
echo "You should see the same sequence of values on /sensor/reading that"
echo "was originally published, replayed at the same relative timing."
