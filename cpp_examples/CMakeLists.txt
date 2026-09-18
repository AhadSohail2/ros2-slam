cmake_minimum_required(VERSION 3.8)
project(cpp_examples)

include_directories(include)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)


add_executable(lifecycle_node src/lifeCycleNode.cpp)
ament_target_dependencies(lifecycle_node rclcpp rclcpp_lifecycle)


install(TARGETS
  lifecycle_node
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
