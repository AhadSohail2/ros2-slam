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

    gazebo = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bumperbot_description"),
            "launch",
            "gazebo.launch.py"
        ),
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
            "use_sim_time": "True"
        }.items()
    )

    safety_stop = Node(
        package="bumperbot_utils",
        executable="safety_stop",
        output="screen",
        parameters=[{"use_sim_time": True}]
    )

    slam = IncludeLaunchDescription(
        os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "launch",
            "slam.launch.py"
        ),
        launch_arguments={
            "use_sim_time": "true",
            "use_slam": use_slam,
            "map_yaml": map_yaml,
        }.items(),
    )

    rviz_slam = Node(
        package="rviz2",
        executable="rviz2",
        arguments=["-d", os.path.join(
                get_package_share_directory("bumperbot_mapping"),
                "rviz",
                "slam.rviz"
            )
        ],
        output="screen",
        parameters=[{"use_sim_time": True}],
    )
    
    return LaunchDescription([
        use_slam_arg,
        map_yaml_arg,
        gazebo,
        controller,
        joystick,
        safety_stop,
        slam,
        rviz_slam
    ])
