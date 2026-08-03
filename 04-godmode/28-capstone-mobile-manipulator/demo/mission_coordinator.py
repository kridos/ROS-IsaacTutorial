#!/usr/bin/env python3
"""Runs the full navigate -> detect -> pick -> navigate -> place mission
from DEEP_DIVE.md, sequencing Nav2 (Chapter 11/17's NavigateToPose
action) and MoveIt2 (Chapter 12/18's MoveGroupInterface + pick/place
pattern) against the combined mobile manipulator, with an explicit
stow-the-arm-before-navigating step enforced at every transition.

Object detection is a hardcoded/simulated pose, not a real perception
pipeline — see DEEP_DIVE.md for why (Chapters 15/16/27 are where real
object detection belongs; re-deriving it here would dilute this
chapter's actual point, which is integration).
"""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, Pose
from moveit.planning import MoveItPy

# Hardcoded mission waypoints and a simulated object pose — a real
# mission would get the pickup/dropoff locations from a task planner and
# the object pose from an actual perception pipeline (Chapters 15/16/27).
PICKUP_NAV_GOAL = (1.5, 0.0)
DROPOFF_NAV_GOAL = (1.5, 1.0)
SIMULATED_OBJECT_POSE = (0.35, 0.0, 0.28)  # relative to base_link, matches Ch18's GRASP_POSITION
PLACE_POSE = (0.20, 0.25, 0.28)             # matches Ch18's PLACE_POSITION
RETREAT_HEIGHT = 0.15
STOW_JOINT_STATE = "home"  # named group_state from Chapter 12's arm_with_gripper.srdf


class MissionCoordinator(Node):
    def __init__(self):
        super().__init__("mission_coordinator")
        self._nav_client = ActionClient(self, NavigateToPose, "navigate_to_pose")
        self._arm_robot = MoveItPy(node_name="mission_coordinator_moveit")
        self._arm = self._arm_robot.get_planning_component("arm")

    def run_mission(self):
        self.get_logger().info("=== Mission start ===")

        self._stow_arm()
        self._navigate_to(*PICKUP_NAV_GOAL, stage_name="navigate-to-pickup")

        object_pose = self._detect_object()
        self._pick(object_pose)

        # Stow again BEFORE navigating with the object in hand — this is
        # the DEEP_DIVE.md pitfall being actively avoided: an extended
        # arm changes the robot's effective footprint for Nav2's
        # obstacle-avoidance costmap, which was configured (Chapter 11's
        # nav2_params.yaml) assuming a stowed-arm footprint.
        self._stow_arm()
        self._navigate_to(*DROPOFF_NAV_GOAL, stage_name="navigate-to-dropoff")

        self._place(PLACE_POSE)
        self._stow_arm()

        self.get_logger().info("=== Mission complete ===")

    def _stow_arm(self):
        self.get_logger().info("[stow] Moving arm to 'home' configuration before any navigation")
        self._arm.set_start_state_to_current_state()
        self._arm.set_goal_state(configuration_name=STOW_JOINT_STATE)
        plan_result = self._arm.plan()
        if plan_result:
            self._arm_robot.execute(plan_result.trajectory, controllers=[])
        else:
            self.get_logger().error("[stow] Planning to home configuration FAILED — aborting mission")
            raise RuntimeError("Failed to stow arm")

    def _navigate_to(self, x: float, y: float, stage_name: str):
        self.get_logger().info(f"[{stage_name}] Navigating to ({x}, {y})")
        self._nav_client.wait_for_server()

        goal_msg = NavigateToPose.Goal()
        goal_msg.pose = PoseStamped()
        goal_msg.pose.header.frame_id = "map"
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.orientation.w = 1.0

        send_goal_future = self._nav_client.send_goal_async(goal_msg)
        rclpy.spin_until_future_complete(self, send_goal_future)
        goal_handle = send_goal_future.result()
        if not goal_handle.accepted:
            raise RuntimeError(f"[{stage_name}] Navigation goal rejected")

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        self.get_logger().info(f"[{stage_name}] Navigation finished")

    def _detect_object(self):
        # Simulated perception step — see module docstring. A real
        # implementation would subscribe to a perception pipeline's
        # detection topic (Chapter 15's isaac_ros_apriltag pattern, or a
        # custom TensorRT-based detector from Chapter 27) instead of
        # returning a hardcoded constant.
        self.get_logger().info(f"[detect] Simulated detection: object at {SIMULATED_OBJECT_POSE}")
        return SIMULATED_OBJECT_POSE

    def _pick(self, position):
        # Chapter 18's pick sequence, condensed — see that chapter for
        # the full step-by-step version with per-stage Cartesian-path
        # fraction checks; abbreviated here to keep this file's focus on
        # mission-level sequencing rather than re-explaining Chapter 18.
        self.get_logger().info(f"[pick] Picking up object at {position}")
        self._move_to_pose(position[0], position[1], position[2] + RETREAT_HEIGHT, "pre-grasp")
        self._cartesian_to(position, "grasp approach")
        self._arm_robot.get_planning_scene_monitor().read_write().apply_attached_collision_object(
            object_id="target_block", link_name="gripper"
        )
        self.get_logger().info("[pick] Attached target_block to gripper")
        self._cartesian_to(
            (position[0], position[1], position[2] + RETREAT_HEIGHT), "post-grasp retreat"
        )

    def _place(self, position):
        self.get_logger().info(f"[place] Placing object at {position}")
        self._move_to_pose(position[0], position[1], position[2] + RETREAT_HEIGHT, "pre-place")
        self._cartesian_to(position, "place approach")
        self._arm_robot.get_planning_scene_monitor().read_write().remove_attached_collision_object(
            object_id="target_block"
        )
        self.get_logger().info("[place] Detached target_block from gripper")
        self._cartesian_to(
            (position[0], position[1], position[2] + RETREAT_HEIGHT), "post-place retreat"
        )

    def _move_to_pose(self, x, y, z, stage_name):
        pose_stamped = PoseStamped()
        pose_stamped.header.frame_id = "base_link"
        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = x, y, z
        pose.orientation.w = 1.0
        pose_stamped.pose = pose

        self._arm.set_start_state_to_current_state()
        self._arm.set_goal_state(pose_stamped_msg=pose_stamped, pose_link="gripper")
        plan_result = self._arm.plan()
        if not plan_result:
            raise RuntimeError(f"[{stage_name}] Planning FAILED")
        self._arm_robot.execute(plan_result.trajectory, controllers=[])

    def _cartesian_to(self, position, stage_name):
        pose = Pose()
        pose.position.x, pose.position.y, pose.position.z = position
        pose.orientation.w = 1.0
        trajectory, fraction = self._arm.get_active_group().compute_cartesian_path(
            waypoints=[pose], eef_step=0.01, avoid_collisions=True
        )
        if fraction < 0.95:
            raise RuntimeError(f"[{stage_name}] Cartesian path only {fraction * 100:.0f}% complete")
        self._arm_robot.execute(trajectory)


def main():
    rclpy.init()
    coordinator = MissionCoordinator()
    coordinator.run_mission()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
