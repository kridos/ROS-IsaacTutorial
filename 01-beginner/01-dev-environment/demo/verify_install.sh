#!/usr/bin/env bash
#
# verify_install.sh — sanity-checks a ROS2 install and workspace.
#
# Each check is independent and reports PASS/FAIL on its own line, rather
# than aborting the whole script on the first failure (`set -e` would do
# that) — the point of this script is to show you EVERYTHING that's wrong
# at once, not stop at the first problem.

# Colors for PASS/FAIL output. Defined as plain ANSI escape codes instead
# of pulling in a library — this is the entire "dependency" this script
# needs.
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color — resets terminal formatting after each line

pass() {
  echo -e "${GREEN}[PASS]${NC} $1"
}

fail() {
  echo -e "${RED}[FAIL]${NC} $1"
}

echo "=== ROS2 install verification ==="

# Check 1: is the `ros2` CLI on PATH at all?
# `command -v` is the portable way to check if a command exists without
# actually running it (more portable than `which`, which isn't POSIX).
if command -v ros2 >/dev/null 2>&1; then
  pass "'ros2' command found on PATH"
else
  fail "'ros2' command not found — did you source /opt/ros/<distro>/setup.bash?"
  # No point running the rest of the checks if ros2 itself is missing —
  # they'd all fail with the same root cause and just add noise.
  echo "Stopping here: fix the above and re-run this script."
  exit 1
fi

# Check 2: is ROS_DISTRO set? This env var is exported by the setup.bash
# script and tells you (and other tools) which ROS2 distro is active.
if [ -n "${ROS_DISTRO:-}" ]; then
  pass "ROS_DISTRO is set to '${ROS_DISTRO}'"
else
  fail "ROS_DISTRO is not set — setup.bash may not have been sourced correctly"
fi

# Check 3: can ros2 actually talk to the package index? A working install
# should list at least a few hundred packages (ros-<distro>-desktop alone
# ships hundreds). A suspiciously low count usually means a partial or
# corrupted install rather than a missing PATH entry (which Check 1 would
# already have caught).
PKG_COUNT=$(ros2 pkg list 2>/dev/null | wc -l)
if [ "$PKG_COUNT" -gt 50 ]; then
  pass "ros2 pkg list found ${PKG_COUNT} packages"
else
  fail "ros2 pkg list only found ${PKG_COUNT} packages (expected 50+) — install may be incomplete"
fi

# Check 4: is ROS_DOMAIN_ID set? Not strictly required (it defaults to 0),
# but Chapter 1's DEEP_DIVE.md recommends setting it explicitly to avoid
# collisions with other ROS2 users on the same network — this check just
# reminds you if you skipped that step.
if [ -n "${ROS_DOMAIN_ID:-}" ]; then
  pass "ROS_DOMAIN_ID is set to '${ROS_DOMAIN_ID}'"
else
  echo "[NOTE] ROS_DOMAIN_ID is not set (defaults to 0) — fine alone, risky on a shared network"
fi

echo "=== Done ==="
