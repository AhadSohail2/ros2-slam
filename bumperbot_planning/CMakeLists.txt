cmake_minimum_required(VERSION 3.8)
project(bumperbot_planning)


find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

include_directories(include)

add_executable(dijkstra_planner src/dijkstra_planner.cpp)
ament_target_dependencies(dijkstra_planner rclcpp nav_msgs geometry_msgs tf2_ros)

install(TARGETS
  dijkstra_planner
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
