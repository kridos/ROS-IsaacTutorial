# Demo: QoS Compatibility

## Matched profiles (works normally)

Terminal 1:

```bash
python3 qos_publisher.py reliable
```

Terminal 2:

```bash
python3 qos_subscriber.py reliable
```

Expected: subscriber logs `I heard: "count=N"` once a second, same as
any normal pub/sub pair.

Try `best_effort` on both sides too — also works normally.

## Mismatched profiles (the silent-failure case)

Terminal 1:

```bash
python3 qos_publisher.py best_effort
```

Terminal 2:

```bash
python3 qos_subscriber.py reliable
```

Expected: the publisher terminal keeps logging `Publishing: 'count=N'`
as normal. The subscriber terminal shows **no** `I heard` lines at all —
not an error, not a warning, just silence. This is the QoS
incompatibility DEEP_DIVE.md describes: a `BEST_EFFORT` publisher cannot
satisfy a `RELIABLE` subscriber's guarantee.

## Diagnose it

While both are still running:

```bash
ros2 topic info /qos_demo -v
```

Expected output includes something like:

```
Publisher count: 1
Node name: qos_publisher
...
QoS profile:
  Reliability: BEST_EFFORT
...
Subscription count: 1
Node name: qos_subscriber
...
QoS profile:
  Reliability: RELIABLE
```

Seeing `BEST_EFFORT` on the publisher and `RELIABLE` on the subscriber
side by side is the confirmation — this mismatch is exactly why no
messages are getting through, even though `ros2 topic list` shows
`/qos_demo` existing normally with both a publisher and a subscriber
connected to it.

## Try the reverse direction

Publisher `reliable`, subscriber `best_effort` — expected: this
direction **works** (a `RELIABLE` publisher can satisfy a `BEST_EFFORT`
subscriber's lesser requirement), confirming the asymmetry DEEP_DIVE.md
describes.
