#!/usr/bin/env python3
"""Publishes a Float64 with injected Gaussian noise on /sensor/reading at
10 Hz — a stand-in for a real noisy sensor (e.g. an IMU or distance
sensor), just so there's something worth plotting and recording."""

import math
import random

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class NoisySensorPublisher(Node):
    def __init__(self):
        super().__init__("noisy_sensor_publisher")
        self._publisher = self.create_publisher(Float64, "sensor/reading", 10)

        # Simulated "true" signal: a slow sine wave, so the plot in
        # rqt_plot shows a recognizable shape instead of pure noise —
        # makes it obvious, when watching the plot, which variation is
        # signal and which is injected noise.
        self._t = 0.0
        self._dt = 0.1  # seconds, matches the 10 Hz timer below

        self._timer = self.create_timer(self._dt, self._publish)

    def _publish(self):
        true_value = math.sin(self._t)  # the "real" underlying signal
        noise = random.gauss(mu=0.0, sigma=0.1)  # simulated sensor noise

        msg = Float64()
        msg.data = true_value + noise
        self._publisher.publish(msg)

        self._t += self._dt


def main():
    rclpy.init()
    node = NoisySensorPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
