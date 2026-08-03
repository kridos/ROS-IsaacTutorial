# Practice: Services & Actions

1. **New service.** Write a `multiply_two_ints` service server/client
   pair, copying the `add_two_ints` pattern. Confirm it works via `ros2
   service call` before writing the client code.

2. **Reject bad input.** Modify `add_two_ints_server.py` to reject (via
   whatever mechanism a plain service allows — consider what a service
   *can't* do here that an action's goal-acceptance callback can) any
   request where `a` or `b` is negative. Notice the limitation: a plain
   service has no clean "reject the request" mechanism the way an action
   does — that's a real design signal, not just a coding exercise.

3. **Cancel handling.** Modify `fibonacci_action_client.py` to send a
   cancel request partway through (after receiving 3 feedback messages)
   instead of running to completion. Confirm the server logs `Goal
   canceled` and returns the partial sequence.

4. **A blocking-call bug, on purpose.** Write a node with a subscription
   callback that calls a service *synchronously* (not via `call_async` +
   `spin_until_future_complete`) from inside that callback, targeting a
   service hosted by the same node. Run it and observe the deadlock
   DEEP_DIVE.md describes — then fix it using the async pattern.

5. **Stretch:** build a small action server that "moves" a simulated
   1D position from 0 to a goal value over N feedback steps (no real
   robot needed — just a number incrementing on a timer inside the
   execute callback), as a warm-up for Chapter 11's `NavigateToPose`.
