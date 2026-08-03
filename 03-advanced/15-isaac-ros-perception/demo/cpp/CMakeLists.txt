cmake_minimum_required(VERSION 3.8)
project(isaac_ros_perception_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(isaac_ros_apriltag_interfaces REQUIRED)

add_executable(apriltag_pose_logger src/apriltag_pose_logger.cpp)
ament_target_dependencies(apriltag_pose_logger rclcpp isaac_ros_apriltag_interfaces)

install(TARGETS
  apriltag_pose_logger
  DESTINATION lib/${PROJECT_NAME})

ament_package()
