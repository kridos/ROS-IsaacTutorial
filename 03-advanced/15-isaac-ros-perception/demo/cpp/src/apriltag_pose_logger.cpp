// Subscribes to isaac_ros_apriltag's detection topic and logs each
// detected tag's ID and pose. Written in C++ specifically because
// production perception-consuming nodes are the case where this
// curriculum's language policy calls for C++ over Python (see the
// project spec) — this is the kind of node that would run continuously
// on a real robot, where C++'s lower overhead matters most.

#include <memory>

#include "rclcpp/rclcpp.hpp"
#include "isaac_ros_apriltag_interfaces/msg/april_tag_detection_array.hpp"

using AprilTagDetectionArray = isaac_ros_apriltag_interfaces::msg::AprilTagDetectionArray;

class AprilTagPoseLogger : public rclcpp::Node
{
public:
  AprilTagPoseLogger() : Node("apriltag_pose_logger")
  {
    subscription_ = this->create_subscription<AprilTagDetectionArray>(
      "tag_detections", 10,
      std::bind(&AprilTagPoseLogger::on_detections, this, std::placeholders::_1));
    RCLCPP_INFO(this->get_logger(), "apriltag_pose_logger ready, listening on tag_detections");
  }

private:
  void on_detections(const AprilTagDetectionArray::SharedPtr msg)
  {
    if (msg->detections.empty()) {
      // Not logged at INFO level every frame — with no tags visible this
      // would spam the terminal at the camera's full frame rate for no
      // useful information, unlike a genuine per-detection log line.
      return;
    }

    for (const auto & detection : msg->detections) {
      const auto & position = detection.pose.pose.pose.position;
      RCLCPP_INFO(
        this->get_logger(),
        "Tag id=%d detected at (%.3f, %.3f, %.3f)",
        detection.id, position.x, position.y, position.z);
    }
  }

  rclcpp::Subscription<AprilTagDetectionArray>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<AprilTagPoseLogger>());
  rclcpp::shutdown();
  return 0;
}
