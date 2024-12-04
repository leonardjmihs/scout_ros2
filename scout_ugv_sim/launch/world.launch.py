import os
from launch import LaunchDescription
from launch.conditions import IfCondition
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, AppendEnvironmentVariable, LogInfo
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.actions import LogInfo
from launch.substitutions import PythonExpression
import launch_ros

def generate_launch_description():
    # Package directories
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    ugv_sim_dir = get_package_share_directory('scout_ugv_sim')
    scout_description_dir = get_package_share_directory('scout_description')

    # Declare the 'world' launch argument
    declare_world_arg = DeclareLaunchArgument(
        'world',  # Name of the argument
        default_value='cylinder_world',  # Default world file (without .world extension)
        description='World to load (do not include the .world extension)'
    )

    # LaunchConfigurations for robot position
    x = LaunchConfiguration('x', default='0.0')
    y = LaunchConfiguration('y', default='0.0')
    z = LaunchConfiguration('z', default='0.1')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Define the world path using the declared argument
    world = PathJoinSubstitution([
        ugv_sim_dir, 'worlds', LaunchConfiguration('world'), TextSubstitution(text=".world")
    ])

    # Set environment variable for Gazebo model path
    set_env_vars_resources = AppendEnvironmentVariable(
        'GAZEBO_MODEL_PATH',
        scout_description_dir
    )

    # Include Gazebo server launch file with the world argument
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()  # Pass the world path
    )

    # Include Gazebo client launch file
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # Robot state publisher launch file
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ugv_sim_dir, 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Spawn Scout mini robot
    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ugv_sim_dir, 'launch', 'spawn_scout_mini.launch.py')
        ),
        launch_arguments={
            'x': x,
            'y': y,
            'z': z,
        }.items()
    )

    # Static transform publisher (map to odom)
    map_to_odom = launch_ros.actions.Node(
        name='map2odom_tf',
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom']
    )

    # Launch description
    ld = LaunchDescription()

    # Add declared arguments to the launch description first
    ld.add_action(declare_world_arg)

    # Add actions to the launch description
    ld.add_action(set_env_vars_resources)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)
    ld.add_action(map_to_odom)

    return ld
