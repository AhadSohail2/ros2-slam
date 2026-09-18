import os
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")
    use_slam = LaunchConfiguration("use_slam")
    slam_config = LaunchConfiguration("slam_config")
    map_yaml = LaunchConfiguration("map_yaml")
    slam_lifecycle_nodes = ["map_saver_server"]
    if os.environ.get("ROS_DISTRO") != "humble":
        slam_lifecycle_nodes.append("slam_toolbox")

    use_sim_time_arg = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true"
    )

    use_slam_arg = DeclareLaunchArgument(
        "use_slam",
        default_value="true",
        description="Run SLAM to build a map. Set false to serve a predefined map."
    )

    map_yaml_arg = DeclareLaunchArgument(
        "map_yaml",
        default_value=os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "maps",
            "small_house",
            "map.yaml"
        ),
        description="Full path to the map YAML file when use_slam:=false"
    )

    slam_config_arg = DeclareLaunchArgument(
        "slam_config",
        default_value=os.path.join(
            get_package_share_directory("bumperbot_mapping"),
            "config",
            "slam_toolbox.yaml"
        ),
        description="Full path to slam yaml file to load"
    )
    
    nav2_map_saver = Node(
        package="nav2_map_server",
        executable="map_saver_server",
        name="map_saver_server",
        output="screen",
        parameters=[
            {"save_map_timeout": 5.0},
            {"use_sim_time": use_sim_time},
            {"free_thresh_default": 0.196},
            {"occupied_thresh_default": 0.65},
        ],
        condition=IfCondition(use_slam),
    )

    slam_toolbox = Node(
        package="slam_toolbox",
        executable="sync_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[
            slam_config,
            {"use_sim_time": use_sim_time},
        ],
        condition=IfCondition(use_slam),
    )

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            {"yaml_filename": map_yaml},
            {"use_sim_time": use_sim_time},
        ],
        condition=UnlessCondition(use_slam),
    )

    slam_lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_slam",
        output="screen",
        parameters=[
            {"node_names": slam_lifecycle_nodes},
            {"use_sim_time": use_sim_time},
            {"autostart": True}
        ],
        condition=IfCondition(use_slam),
    )

    map_lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_map",
        output="screen",
        parameters=[
            {"node_names": ["map_server"]},
            {"use_sim_time": use_sim_time},
            {"autostart": True}
        ],
        condition=UnlessCondition(use_slam),
    )

    return LaunchDescription([
        use_sim_time_arg,
        use_slam_arg,
        map_yaml_arg,
        slam_config_arg,
        nav2_map_saver,
        slam_toolbox,
        map_server,
        slam_lifecycle_manager,
        map_lifecycle_manager,
    ])
