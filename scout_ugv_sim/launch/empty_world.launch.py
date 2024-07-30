import os
import launch
import launch_ros

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, GroupAction, IncludeLaunchDescription, AppendEnvironmentVariable
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch.substitutions import LaunchConfiguration, Command, TextSubstitution, PythonExpression
from launch_ros.actions import Node, LoadComposableNodes
from launch.conditions import IfCondition
from launch_ros.descriptions import ComposableNode
from launch.launch_description_sources import PythonLaunchDescriptionSource

ros_gz_sim = get_package_share_directory('ros_gz_sim')
ugv_sim_dir = get_package_share_directory('scout_ugv_sim')
scout_description_dir = get_package_share_directory('scout_description')

def generate_launch_description():
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    launch_file_dir = os.path.join(get_package_share_directory('scout_ugv_sim'), 'launch')

    # use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x = LaunchConfiguration('x', default='0.0')
    y = LaunchConfiguration('y', default='0.0')
    z = LaunchConfiguration('z', default='0.1')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    world = os.path.join(
        ugv_sim_dir,
        'worlds',
        # 'empty_world.world'
        'cylinder_world.world'
    )
    set_env_vars_resources = AppendEnvironmentVariable(
            'GAZEBO_MODEL_PATH',
            # os.path.join(scout_description_dir, 'meshes', 'scout_mini')
            os.path.dirname(scout_description_dir)
            )
    print(os.path.dirname(scout_description_dir))
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world}.items()
    )

    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_scout_mini.launch.py')
        ),
        launch_arguments={
            'x': x,
            'y': y, 
            'z': z,
        }.items()
    )
    map_to_odom = launch_ros.actions.Node(
        name='map2odom_tf',
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['0','0','0','0','0','0','map','odom']
        )

    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(set_env_vars_resources)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)
    ld.add_action(map_to_odom)
    return ld