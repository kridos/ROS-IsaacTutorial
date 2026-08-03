#!/usr/bin/env python3
"""A single centralized node that knows both robots' namespaces and
sends each a different Twist command, then logs both robots' odometry
side by side — the simple, centralized coordination pattern described in
DEEP_DIVE.md, and a check that the two robots are truly independently
addressable (not cross-talking) after namespacing."""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class FleetCoordinator(Node):
    def __init__(self):
        super().__init__("fleet_coordinator")

        # Publishers/subscribers built with fully-namespaced topic names
        # here, since this coordinator node itself lives outside either
        # robot's namespace and needs to address both explicitly.
        self._cmd_vel_pubs = {
            "robot1": self.create_publisher(Twist, "/robot1/cmd_vel", 10),
            "robot2": self.create_publisher(Twist, "/robot2/cmd_vel", 10),
        }
        self._latest_odom = {"robot1": None, "robot2": None}
        self.create_subscription(Odometry, "/robot1/odom", lambda m: self._on_odom("robot1", m), 10)
        self.create_subscription(Odometry, "/robot2/odom", lambda m: self._on_odom("robot2", m), 10)

        self._drive_timer = self.create_timer(0.1, self._drive_robots)
        self._log_timer = self.create_timer(1.0, self._log_positions)

    def _drive_robots(self):
        # Different commands per robot — robot1 drives straight, robot2
        # turns in place — deliberately different so it's obvious in the
        # logged odometry that each robot is responding to its own
        # command, not either robot's or a shared/confused one.
        forward = Twist()
        forward.linear.x = 0.2
        self._cmd_vel_pubs["robot1"].publish(forward)

        turn = Twist()
        turn.angular.z = 0.5
        self._cmd_vel_pubs["robot2"].publish(turn)

    def _on_odom(self, robot_name: str, msg: Odometry):
        self._latest_odom[robot_name] = msg.pose.pose

    def _log_positions(self):
        for robot_name, pose in self._latest_odom.items():
            if pose is None:
                self.get_logger().info(f"{robot_name}: no odometry received yet")
            else:
                self.get_logger().info(
                    f"{robot_name}: x={pose.position.x:.3f}, y={pose.position.y:.3f}"
                )


def main():
    rclpy.init()
    node = FleetCoordinator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
