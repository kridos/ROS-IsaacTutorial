# Demo: Services & Actions

## Service demo (Python)

Terminal 1:

```bash
python3 python/add_two_ints_server.py
```

Terminal 2:

```bash
python3 python/add_two_ints_client.py 5 7
```

Expected client output: `Result: 5 + 7 = 12`. Run the client again with
different numbers — the server keeps running and handles each request
independently.

## Service demo (C++)

```bash
cp -r cpp ~/ros2_ws/src/services_and_actions_cpp
cd ~/ros2_ws
colcon build --packages-select services_and_actions_cpp
source install/setup.bash
```

Terminal 1: `ros2 run services_and_actions_cpp add_two_ints_server`
Terminal 2: `ros2 run services_and_actions_cpp add_two_ints_client 5 7`

## Action demo (Python only — see DEEP_DIVE.md for why)

Terminal 1:

```bash
python3 python/fibonacci_action_server.py
```

Terminal 2:

```bash
python3 python/fibonacci_action_client.py 8
```

Expected: the server terminal logs feedback every ~0.5s
(`Feedback: [0, 1, 1]`, `Feedback: [0, 1, 1, 2]`, ...), the client terminal
logs the same feedback as it arrives, and finally both print the full
8-number sequence as the result.

To see cancellation in action, start a goal with a large order (e.g. 20)
and press Ctrl+C on the client partway through — the server logs
`Goal canceled` and returns whatever partial sequence it had computed.

## Try it from the CLI (no client code at all)

```bash
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 10, b: 32}"
ros2 action send_goal /fibonacci example_interfaces/action/Fibonacci "{order: 6}" --feedback
```
