import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get package directory
    pkg_cpr_empty_gazebo = get_package_share_directory('cpr_empty_gazebo')

    # Process URDF with xacro
    xacro_file = os.path.join(pkg_cpr_empty_gazebo, 'urdf', 'empty_geometry.urdf.xacro')
    robot_description = Command([
        FindExecutable(name='xacro'), ' ', xacro_file
    ])

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )

    # RViz
    rviz_config = os.path.join(pkg_cpr_empty_gazebo, 'rviz', 'world.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        robot_state_publisher,
        rviz
    ])
