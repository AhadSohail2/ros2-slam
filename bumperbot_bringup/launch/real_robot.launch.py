import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    use_slam = LaunchConfiguration("use_slam")
    map_yaml = LaunchConfiguration("map_yaml")

    use_slam_arg = DeclareLaunchArgument(
        "use_slam", default_value="true",
        description="Run SLAM; set false to load map_yaml instead."
    )
    map_yaml_arg = DeclareLaunchArgument(
        "map_yaml",
        default_value=os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "maps", "small_house", "map.yaml"
        ),
        description="Map YAML to load when use_slam:=false"
    )

    hardware_interface = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bumperbot_firmware"),
            "launch",
            "hardware_interface.launch.py"
        ),
    )

    laser_driver = Node(
            package="rplidar_ros",
            executable="rplidar_node",
            name="rplidar_node",
            parameters=[os.path.join(
                get_package_share_directory("bumperbot_bringup"),
                "config",
                "rplidar_a1.yaml"
            )],
            output="screen"
    )
    
    controller = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bumperbot_controller"),
            "launch",
            "controller.launch.py"
        ),
        launch_arguments={
            "use_simple_controller": "False",
        }.items(),
    )
    
    joystick = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bumperbot_controller"),
            "launch",
            "joystick_teleop.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "False"
        }.items()
    )

    imu_driver_node = Node(
        package="bumperbot_firmware",
        executable="mpu6050_driver.py"
    )

    safety_stop = Node(
        package="bumperbot_utils",
        executable="safety_stop",
        output="screen",
    )

    slam = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "launch",
            "slam.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "false",
            "use_slam": use_slam,
            "map_yaml": map_yaml,
        }.items(),
    )
    
    return LaunchDescription([
        use_slam_arg,
        map_yaml_arg,
        hardware_interface,
        laser_driver,
        controller,
        joystick,
        imu_driver_node,
        safety_stop,
        slam
    ])
