#!/usr/bin/env python3
"""A talker (see Chapter 2) whose publish rate and message text are
runtime-configurable parameters instead of hardcoded values."""

import sys

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ConfigurableTalker(Node):
    def __init__(self):
        super().__init__("configurable_talker")

        # Every parameter must be declared with a default before it can
        # be read — this is what makes it show up in `ros2 param list`
        # even if nobody overrides it, and what lets ROS2 reject a typo'd
        # parameter name at set-time instead of ignoring it silently.
        self.declare_parameter("publish_rate_hz", 1.0)
        self.declare_parameter("message_text", "Hello, ROS2!")

        # Read parameters once at startup. get_parameter_value() returns a
        # variant-like object; .double_value / .string_value pick out the
        # field matching the type we declared above.
        rate_hz = self.get_parameter("publish_rate_hz").get_parameter_value().double_value
        self._message_text = self.get_parameter("message_text").get_parameter_value().string_value

        self._publisher = self.create_publisher(String, "chatter", 10)
        self._count = 0

        # Timer period is 1/rate seconds — declared and read above instead
        # of hardcoded like Chapter 2's talker.
        period_sec = 1.0 / rate_hz
        self._timer = self.create_timer(period_sec, self._publish)

        self.get_logger().info(
            f"Starting with publish_rate_hz={rate_hz}, message_text='{self._message_text}'"
        )

    def _publish(self):
        msg = String()
        msg.data = f"{self._message_text} count={self._count}"
        self._publisher.publish(msg)
        self.get_logger().info(f"Publishing: '{msg.data}'")
        self._count += 1


def main():
    # Passing sys.argv (instead of no args) is what lets rclpy parse
    # --ros-args --params-file / -p overrides supplied by the launch file
    # — without this, command-line parameter overrides are silently
    # ignored and only the values in this file's declare_parameter()
    # defaults would ever apply.
    rclpy.init(args=sys.argv)
    node = ConfigurableTalker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
