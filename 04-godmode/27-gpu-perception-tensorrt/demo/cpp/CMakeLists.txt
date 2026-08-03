cmake_minimum_required(VERSION 3.8)
project(tensorrt_inference_demo)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(CUDAToolkit REQUIRED)

# TensorRT ships no CMake config package by default on most installs —
# find it manually via its known header/library names rather than
# find_package(TensorRT), which would fail on a typical install.
find_path(TENSORRT_INCLUDE_DIR NvInfer.h REQUIRED)
find_library(TENSORRT_LIBRARY nvinfer REQUIRED)

add_executable(tensorrt_inference_node src/tensorrt_inference_node.cpp)
ament_target_dependencies(tensorrt_inference_node rclcpp sensor_msgs std_msgs)
target_include_directories(tensorrt_inference_node PRIVATE ${TENSORRT_INCLUDE_DIR})
target_link_libraries(tensorrt_inference_node ${TENSORRT_LIBRARY} CUDA::cudart)

install(TARGETS
  tensorrt_inference_node
  DESTINATION lib/${PROJECT_NAME})

ament_package()
