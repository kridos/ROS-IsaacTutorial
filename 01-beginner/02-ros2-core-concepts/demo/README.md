# Demo: Talker / Listener

## Python version (no build step needed)

Open two terminals. In each, first source ROS2:

```bash
source /opt/ros/jazzy/setup.bash
```

Terminal 1:

```bash
python3 python/talker.py
```

Terminal 2:

```bash
python3 python/listener.py
```

## C++ version (build with colcon)

Copy (or symlink) the `cpp/` folder into your workspace's `src/`, then
build:

```bash
cp -r cpp ~/ros2_ws/src/ros2_core_concepts_cpp
cd ~/ros2_ws
colcon build --packages-select ros2_core_concepts_cpp
source install/setup.bash
```

Terminal 1:

```bash
ros2 run ros2_core_concepts_cpp talker
```

Terminal 2:

```bash
ros2 run ros2_core_concepts_cpp listener
```

You can also mix languages — run the Python talker against the C++
listener, or vice versa. They agree on the topic name (`/chatter`) and
message type (`std_msgs/msg/String`), so it doesn't matter which
language published or subscribed.

## Expected output

Talker terminal, once per second:

```
[INFO] [talker]: Publishing: 'Hello, ROS2! count=0'
[INFO] [talker]: Publishing: 'Hello, ROS2! count=1'
...
```

Listener terminal, once per second:

```
[INFO] [listener]: I heard: "Hello, ROS2! count=0"
[INFO] [listener]: I heard: "Hello, ROS2! count=1"
...
```

## Try it yourself

While both are running, open a third terminal and inspect the graph:

```bash
ros2 node list        # should show /talker and /listener
ros2 topic list        # should show /chatter
ros2 topic echo /chatter
ros2 topic hz /chatter  # should report ~1.0 Hz
```
