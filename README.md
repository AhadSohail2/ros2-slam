# BumperBot SLAM

ROS 2 workspace for running SLAM on BumperBot with [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox).

## Packages

| Package | Role |
| --- | --- |
| `bumperbot_bringup` | Top-level launch files for sim and real robot |
| `bumperbot_mapping` | SLAM launch, slam_toolbox config, RViz |
| `bumperbot_description` | URDF/Xacro, meshes, Gazebo worlds |
| `bumperbot_controller` | Diff-drive controllers, joystick teleop, twist mux |
| `bumperbot_utils` | Safety stop near obstacles |
| `bumperbot_firmware` | Real-robot hardware interface and IMU driver |

## Dependencies

- ROS 2 Jazzy
- `slam_toolbox`
- `nav2_map_server`, `nav2_lifecycle_manager`
- `ros2_control` / `ros2_controllers`
- `twist_mux`, `joy`, `joy_teleop`
- Gazebo (simulation)
- `rplidar_ros` (real robot)

## Build

```bash
cd ~/bumperbot_ws
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Run SLAM (simulation)

```bash
source ~/bumperbot_ws/install/setup.bash
ros2 launch bumperbot_bringup simulated_robot.launch.py
```

This starts Gazebo, controllers, joystick teleop, safety stop, slam_toolbox, and RViz.

Drive the robot with a joystick (or publish to `cmd_vel`) to build the map.

## Run SLAM (real robot)

```bash
source ~/bumperbot_ws/install/setup.bash
ros2 launch bumperbot_bringup real_robot.launch.py
```

Starts hardware interface, RPLidar, controllers, MPU6050 IMU, joystick teleop, safety stop, and slam_toolbox.

## SLAM only

If the robot stack is already running:

```bash
ros2 launch bumperbot_mapping slam.launch.py use_sim_time:=true   # sim
ros2 launch bumperbot_mapping slam.launch.py use_sim_time:=false  # real
```

## Save a map

```bash
ros2 run nav2_map_server map_saver_cli -f ~/maps/my_map
```

## Configuration

- SLAM parameters: `bumperbot_mapping/config/slam_toolbox.yaml`
- Controllers: `bumperbot_controller/config/bumperbot_controllers.yaml`
- Lidar (real): `bumperbot_bringup/config/rplidar_a1.yaml`

Key slam_toolbox frames/topics:

- `odom_frame`: `odom`
- `map_frame`: `map`
- `base_frame`: `base_footprint`
- `scan_topic`: `/scan`

## License

Apache 2.0
# ros2-slam
