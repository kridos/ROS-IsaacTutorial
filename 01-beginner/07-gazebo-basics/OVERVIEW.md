# Chapter 7: Gazebo Basics

## What this is

Gazebo (specifically Gazebo Harmonic, the current version, sometimes
called "gz" to distinguish it from the older "classic Gazebo") is a
physics simulator: it simulates gravity, collisions, friction, and motor
forces acting on the robot model you built in Chapter 5. Instead of
imagining how your robot would move, you can watch it actually move
(virtually) before ever touching hardware.

## Why it matters

Simulation is where you'll spend most of your development time throughout
the rest of this curriculum, and in robotics generally — it's faster,
safer, and cheaper to iterate on a navigation algorithm or a control loop
in simulation than on physical hardware, and it's how NVIDIA Isaac Sim
(Chapter 13 onward) fits into the picture too, at a different fidelity
and scale.

## Where this fits

This is where Chapters 2 (topics), 4 (launch files), and 5 (URDF) come
together: you'll extend Chapter 5's arm-building knowledge to build a
wheeled robot, launch multiple processes together the way Chapter 4
taught, and drive the robot by publishing to a topic the way Chapter 2
taught — the same tools, now producing something that visibly moves in a
physics world.

## What the demo shows

A simple differential-drive robot spawned into an empty Gazebo world,
bridged to ROS2 so you can drive it by publishing `Twist` messages to
`/cmd_vel` and watch its `/odom` topic report back its estimated
position and velocity.
