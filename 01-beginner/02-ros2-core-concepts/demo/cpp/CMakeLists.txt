cmake_minimum_required(VERSION 3.8)
project(ros2_core_concepts_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ament_cmake is the CMake build system ROS2 packages use; find_package
# here pulls in rclcpp (the C++ client library) and std_msgs (for
# std_msgs::msg::String), matching the <depend> tags in package.xml.
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(talker src/talker.cpp)
ament_target_dependencies(talker rclcpp std_msgs)

add_executable(listener src/listener.cpp)
ament_target_dependencies(listener rclcpp std_msgs)

# install(TARGETS ...) puts the built binaries where `ros2 run` expects
# to find them after `colcon build` — without this, the executables would
# only exist in the build/ directory, not the install/ directory colcon
# adds to PATH.
install(TARGETS
  talker
  listener
  DESTINATION lib/${PROJECT_NAME})

ament_package()
