import os
import launch
import launch_ros

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, GroupAction, IncludeLaunchDescription
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import FindExecutable, PathJoinSubstitution
from launch.substitutions import LaunchConfiguration, Command, TextSubstitution, PythonExpression
from launch_ros.actions import Node, LoadComposableNodes
from launch.conditions import IfCondition
from launch_ros.descriptions import ComposableNode
from launch.launch_description_sources import PythonLaunchDescriptionSource

ros_gz_sim = get_package_share_directory('ros_gz_sim')
ugv_sim_dir = get_package_share_directory('scout_ugv_sim')

def generate_launch_description():
    model_name = 'grogu'
    model_path = os.path.join(get_package_share_directory('scout_description'), "urdf", model_name)

    file = LaunchConfiguration('file')
    name = LaunchConfiguration('name')
    x = LaunchConfiguration('x', default='0.0')
    y = LaunchConfiguration('y', default='0.0')
    z = LaunchConfiguration('z', default='0.0')
    roll = LaunchConfiguration('R', default='0.0')
    pitch = LaunchConfiguration('P', default='0.0')
    yaw = LaunchConfiguration('Y', default='0.0')

    sdf_file = os.path.join(model_path, model_name+".sdf")
    declare_file_cmd = DeclareLaunchArgument(
        'file', default_value=sdf_file,
        description='SDF filename')

    declare_name_cmd = DeclareLaunchArgument(
        'name', default_value=TextSubstitution(text='Scout'),
        description='Name of the entity'
    )
    bridge_params = os.path.join(
        ugv_sim_dir,
        'params',
        'scout_mini_bridge.yaml'
    )

    load_sim_nodes = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
                     '-file', file,
                     '-name', name,
                     '-x', x,
                     '-y', y,
                     '-z', z,
                     '-R', roll,
                     '-P', pitch,
                     '-Y', yaw,
                     ],
    )

    start_gazebo_ros_bridge_cmd = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ],
        output='screen',
    )

    ld = launch.LaunchDescription()
    ld.add_action(declare_file_cmd)
    ld.add_action(declare_name_cmd)
    # ld.add_action(load_server_node)
    ld.add_action(load_sim_nodes)
    # ld.add_action(load_composable_nodes)turtlebot3_gazebo
    ld.add_action(start_gazebo_ros_bridge_cmd)
    return ld
    

    return launch.LaunchDescription([

    ])
