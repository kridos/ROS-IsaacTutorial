# Chapter 3 Deep Dive: Services & Actions

## Choosing topic vs. service vs. action

| Pattern | Shape | Robot example |
|---|---|---|
| Topic | Continuous stream, 0-to-many subscribers, no reply | Camera publishing frames, wheel encoders publishing odometry |
| Service | One request, one response, synchronous-feeling | "What's the battery level right now?", "Reset the odometry to zero" |
| Action | Long-running goal, feedback while running, cancellable | "Navigate to this waypoint", "Close the gripper" |

The test that usually settles it: if the caller needs to *wait for a
result* and the operation takes non-trivial time, or needs progress
updates, it's an action. If it's near-instant and there's no meaningful
"in progress" state, it's a service. If nobody needs a reply at all and
it's ongoing data, it's a topic.

## Services: `.srv` structure

A service type is defined as a request and a response separated by `---`.
`example_interfaces/srv/AddTwoInts` (used in this chapter's demo) looks
like:

```
int64 a
int64 b
---
int64 sum
```

The server implements a callback that receives the request and returns
the response; the client sends a request and receives (or awaits) a
response. Unlike a topic, a service call is a direct request to *one*
server (whichever node currently has that service name advertised) — if
no server is up, the call fails immediately rather than silently doing
nothing the way an unsubscribed topic publish would.

## Actions: `.action` structure

An action type has three parts — goal, result, and feedback:

```
int32 order          # goal: how many Fibonacci numbers to compute
---
int32[] sequence      # result: the final sequence
---
int32[] partial_sequence  # feedback: sequence so far, sent while running
```

The action server accepts (or rejects) a goal, then runs it — periodically
publishing feedback — until it finishes, is cancelled, or is preempted by
a new goal (behavior depends on how the server is written). The client
sends a goal, can subscribe to feedback, and awaits a final result or
sends a cancel request.

This goal/feedback/result/cancel shape is exactly what Nav2's
`NavigateToPose` action and MoveIt2's `MoveGroup` action use — you're
learning the general pattern here on a toy example (Fibonacci) so it's
already familiar when you meet it doing something real in Tier 2.

## Sync vs. async clients

Calling a service synchronously (blocking until the response arrives) is
fine from a plain script, but calling it synchronously **from inside
another node's callback** can deadlock: the callback thread blocks
waiting for a response that requires the executor to process an incoming
message, but the executor thread is the one blocked in the callback. The
demo's client uses `call_async()` plus `rclpy.spin_until_future_complete()`
to avoid this — worth doing by habit even in a simple standalone client,
since the pattern generalizes to code where it does matter.

## CLI tools

- `ros2 service list` / `ros2 service call /add_two_ints
  example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"` — call a service
  directly from the terminal, no client code needed, useful for manual
  testing.
- `ros2 action list` / `ros2 action send_goal /fibonacci
  example_interfaces/action/Fibonacci "{order: 5}" --feedback` — send an
  action goal from the terminal and stream feedback as it arrives.

## Common pitfall: blocking the executor

Beyond the sync-call-inside-a-callback deadlock above, the same class of
bug shows up as "my node stopped responding to anything" whenever a
callback (timer, subscription, service) does something slow and blocking
— a long computation, a blocking network call, `time.sleep()` for more
than a moment. A single-threaded executor (the default) processes
callbacks one at a time; a callback that never returns starves every
other callback on that node, including the ones that would let it be
cancelled. Long-running work belongs in an action server (which is
designed to run across many callback invocations, not one blocking call).
