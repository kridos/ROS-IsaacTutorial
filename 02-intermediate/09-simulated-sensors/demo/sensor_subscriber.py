#!/usr/bin/env python3
"""Subscribes to /camera/image_raw, /scan, and /imu, logging a one-line
summary of each message as it arrives — a first look at real (simulated)
sensor data without any perception logic yet."""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan, Imu


class SensorSubscriber(Node):
    def __init__(self):
        super().__init__("sensor_subscriber")
        self.create_subscription(Image, "camera/image_raw", self._on_image, 10)
        self.create_subscription(LaserScan, "scan", self._on_scan, 10)
        self.create_subscription(Imu, "imu", self._on_imu, 10)

    def _on_image(self, msg: Image):
        # We don't decode pixel data here (that's Isaac ROS / perception
        # territory, Chapter 15+) — just confirm frames are arriving with
        # the expected dimensions and encoding.
        self.get_logger().info(
            f"[camera] {msg.width}x{msg.height} encoding={msg.encoding} "
            f"frame_id={msg.header.frame_id}"
        )

    def _on_scan(self, msg: LaserScan):
        # Filter out inf/nan readings (no obstacle detected at that angle)
        # before computing min/max, otherwise "min range" would trivially
        # be a nonsensical value for empty space in every direction.
        valid_ranges = [r for r in msg.ranges if msg.range_min <= r <= msg.range_max]
        if valid_ranges:
            self.get_logger().info(
                f"[lidar] {len(msg.ranges)} samples, "
                f"min={min(valid_ranges):.2f}m max={max(valid_ranges):.2f}m"
            )
        else:
            self.get_logger().info(f"[lidar] {len(msg.ranges)} samples, no obstacles in range")

    def _on_imu(self, msg: Imu):
        q = msg.orientation
        self.get_logger().info(
            f"[imu] orientation quaternion=({q.x:.2f}, {q.y:.2f}, {q.z:.2f}, {q.w:.2f}) "
            f"accel_z={msg.linear_acceleration.z:.2f}"
        )


def main():
    rclpy.init()
    node = SensorSubscriber()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
