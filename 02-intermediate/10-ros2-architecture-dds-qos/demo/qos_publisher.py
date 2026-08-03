#!/usr/bin/env python3
"""Publishes a counting string on /qos_demo, with a QoS reliability
policy chosen from the command line — used together with
qos_subscriber.py to demonstrate matched vs. mismatched QoS.

Usage: python3 qos_publisher.py [reliable|best_effort]  (default: reliable)
"""

import sys

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from std_msgs.msg import String


def build_qos(profile_name: str) -> QoSProfile:
    reliability = (
        ReliabilityPolicy.RELIABLE
        if profile_name == "reliable"
        else ReliabilityPolicy.BEST_EFFORT
    )
    # KEEP_LAST with a small depth for both profiles here — this demo is
    # specifically about Reliability compatibility, so History is held
    # constant rather than varied too, to keep the one-variable-at-a-time
    # comparison clean.
    return QoSProfile(
        reliability=reliability,
        history=HistoryPolicy.KEEP_LAST,
        depth=10,
    )


class QosPublisher(Node):
    def __init__(self, profile_name: str):
        super().__init__("qos_publisher")
        qos = build_qos(profile_name)
        self._publisher = self.create_publisher(String, "qos_demo", qos)
        self._count = 0
        self._timer = self.create_timer(1.0, self._publish)
        self.get_logger().info(f"Publishing with reliability={profile_name}")

    def _publish(self):
        msg = String()
        msg.data = f"count={self._count}"
        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: '{msg.data}'")
        self._count += 1


def main():
    profile_name = sys.argv[1] if len(sys.argv) > 1 else "reliable"
    if profile_name not in ("reliable", "best_effort"):
        print("Usage: qos_publisher.py [reliable|best_effort]")
        sys.exit(1)

    rclpy.init()
    node = QosPublisher(profile_name)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
