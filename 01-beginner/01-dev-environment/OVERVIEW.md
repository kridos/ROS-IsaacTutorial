# Chapter 1: Dev Environment

## What this is

ROS2 (Robot Operating System 2) isn't an operating system — it's a
collection of libraries and tools for writing robot software: passing
messages between programs, describing robots, running simulations, and
more. Before you can use any of it, you need it installed and your
terminal configured to find it.

This chapter installs ROS2, sets up a **workspace** (a folder where your
own robot code lives) and a **package** (the basic unit ROS2 code is
organized into — think of it like a project/module), and verifies
everything works.

## Why it matters

Every single later chapter assumes ROS2 is installed and your workspace
exists. Getting this right once, and understanding *why* each step
matters, saves you from mysterious "command not found" and "package not
found" errors for the rest of the curriculum — errors that are almost
always an environment problem, not a code problem.

## Where this fits

This is the very first chapter. Nothing before it. Chapter 2 (ROS2 core
concepts) assumes the workspace built here exists and `ros2` commands work
in your terminal.

## What the demo shows

`demo/verify_install.sh` is a script that checks your ROS2 install: is the
`ros2` command available, is `ROS_DISTRO` set, can it list installed
packages. Run it after following the DEEP_DIVE.md install steps to confirm
you're ready to move on.
