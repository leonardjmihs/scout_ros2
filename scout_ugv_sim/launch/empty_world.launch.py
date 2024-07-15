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
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x = LaunchConfiguration('x', default='0.0')
    y = LaunchConfiguration('y', default='0.0')
    z = LaunchConfiguration('z', default='0.5')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    world = os.path.join(
        ugv_sim_dir,
        'worlds',
        'empty_world.world'
    )
    set_env_vars_resources = AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            # os.path.join(scout_description_dir, 'meshes', 'scout_mini')
            os.path.dirname(scout_description_dir)
            )

    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r -s -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    )
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': '-g -v4 '}.items()
    )

    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ugv_sim_dir, 'launch', 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    spawn_scout_mini_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ugv_sim_dir, 'launch', 'spawn_scout_mini.launch.py')
        ),
        launch_arguments={
            'x':x,
            'y':y,
            'z':z
        }.items()
    )

    # bridge_params = os.path.join(
    #     ugv_sim_dir,
    #     'params',
    #     'turtlebot3_waffle_bridge.yaml'
    # )

    # start_gazebo_ros_bridge_cmd = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=[
    #         '--ros-args',
    #         '-p',
    #         f'config_file:={bridge_params}',
    #     ],
    #     output='screen',
    # )
    ld = LaunchDescription()

    # Add the commands to the launch description
    ld.add_action(set_env_vars_resources)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_scout_mini_cmd)

    return ld