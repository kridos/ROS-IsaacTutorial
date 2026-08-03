# Chapter 15: Isaac ROS — GPU Perception, NITROS, VSLAM

## What this is

**Isaac ROS** is NVIDIA's collection of GPU-accelerated ROS2 perception
packages — visual SLAM, AprilTag detection, object detection, and more —
built to run efficiently on Jetson and RTX hardware, doing perception
work on the GPU instead of leaning on the CPU the way a typical ROS2
package would.

## Why it matters

A real robot's camera or lidar produces data far faster than a
CPU-bound perception pipeline can usually process in real time,
especially on embedded hardware (a Jetson onboard a robot, not a
workstation). Isaac ROS exists specifically to make real-time perception
on that kind of hardware achievable, and it's the standard NVIDIA
recommends for production robots built around their platform.

## Where this fits

Builds on Chapter 9's simulated sensors (camera data, specifically) and
Chapter 8's TF2 (VSLAM output is a pose and a transform). Positioned as
a GPU-accelerated alternative/complement to Chapter 11's Nav2 stack —
AMCL localizes against lidar and a pre-built map; VSLAM localizes from
camera images without needing a pre-built map at all.

## What the demo shows

Two independent pieces: a Python node listening to Isaac ROS Visual
SLAM's pose output and confirming the corresponding TF transform exists
(tying back to Chapter 8), and a C++ node logging AprilTag detections —
chosen as this chapter's C++ demo because production perception-consuming
code is exactly the case where C++ is the real-world default.
