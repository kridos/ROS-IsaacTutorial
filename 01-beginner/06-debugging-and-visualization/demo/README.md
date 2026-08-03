# Demo: Debugging & Visualization Tools

## Setup

Terminal 1:

```bash
python3 noisy_sensor_publisher.py
```

## rqt_graph — see the graph

Terminal 2:

```bash
ros2 run rqt_graph rqt_graph
```

Expected: a box labeled `/noisy_sensor_publisher` with an arrow to a
topic `/sensor/reading`.

## rqt_plot — watch the signal live

```bash
ros2 run rqt_plot rqt_plot /sensor/reading/data
```

Expected: a live scrolling sine wave with visible noise jitter around it.

## rqt_console — filtered logs

```bash
ros2 run rqt_console rqt_console
```

Expected: log rows from `/noisy_sensor_publisher` (there won't be many —
this node doesn't log much — but you should see its startup message; try
it again in Chapter 7 once more nodes are logging at once, where the
filtering becomes more obviously useful).

## Record and replay

```bash
bash record_and_replay.sh
```

Walks through recording 10 seconds of `/sensor/reading` to
`./sensor_recording/`, printing the recording's info, then tells you how
to replay it and confirm with `ros2 topic echo`. Follow the printed
instructions (record and playback happen in separate terminals).

Expected: `ros2 bag info ./sensor_recording` reports one topic
(`/sensor/reading`), roughly 100 messages (10 seconds at 10 Hz), type
`std_msgs/msg/Float64`. Replaying and echoing shows the same sequence of
values you'd have seen live.
