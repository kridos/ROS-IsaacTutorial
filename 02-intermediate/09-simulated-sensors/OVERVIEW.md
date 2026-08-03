# Chapter 9: Simulated Sensors — Camera, Lidar, IMU

## What this is

Real robots perceive the world through sensors: cameras (images), lidar
(distance scans), IMUs (orientation and acceleration). Gazebo can
simulate all three, generating realistic-shaped ROS2 sensor messages from
a virtual world — so you can write and test perception code before any
sensor hardware exists or is available to you.

## Why it matters

Nav2 (Chapter 11) needs lidar data to localize and avoid obstacles.
Later, Isaac ROS (Chapter 15) and synthetic data generation (Chapter 16)
build heavily on simulated perception. Getting comfortable with what
simulated sensor data looks like, and how it's wired up, is a prerequisite
for nearly everything perception-related later in this curriculum.

## Where this fits

Directly extends Chapter 7's diff-drive robot with sensor links and
Gazebo sensor plugins, bridged the same way Chapter 7 bridged `/cmd_vel`
and `/odom` — same mechanism, more topics.

## What the demo shows

The Chapter 7 robot, now carrying a forward-facing camera, a 2D lidar,
and an IMU, all publishing to ROS2. A subscriber node prints a one-line
summary of each sensor's data as it arrives, so you can see real
(simulated) sensor output flowing without writing any perception logic
yet — that comes later.
