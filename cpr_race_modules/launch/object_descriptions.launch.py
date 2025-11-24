import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetParameter
from launch.substitutions import LaunchConfiguration, Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node


def generate_launch_description():
    # Get package directory
    pkg_gazebo_race_modules = get_package_share_directory('gazebo_race_modules')

    # Declare arguments
    track_type_arg = DeclareLaunchArgument('track_type', default_value='road')
    barrier_type_arg = DeclareLaunchArgument('barrier_type', default_value='racing')
    complexity_arg = DeclareLaunchArgument('complexity', default_value='simple')
    size_arg = DeclareLaunchArgument('size', default_value='small')

    # Process URDF files with xacro
    ground_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            pkg_gazebo_race_modules, 'urdf',
            ['ground_', LaunchConfiguration('complexity'), '.urdf.xacro']
        ])
    ])

    edge_corner_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            pkg_gazebo_race_modules, 'urdf',
            [LaunchConfiguration('size'), '_', LaunchConfiguration('barrier_type'),
             '_edge_corner_', LaunchConfiguration('complexity'), '.urdf.xacro']
        ])
    ])

    edge_straight_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            pkg_gazebo_race_modules, 'urdf',
            [LaunchConfiguration('size'), '_', LaunchConfiguration('barrier_type'),
             '_edge_straight_', LaunchConfiguration('complexity'), '.urdf.xacro']
        ])
    ])

    corner_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            pkg_gazebo_race_modules, 'urdf',
            [LaunchConfiguration('size'), '_', LaunchConfiguration('track_type'),
             '_corner_', LaunchConfiguration('complexity'), '.urdf.xacro']
        ])
    ])

    straight_description = Command([
        FindExecutable(name='xacro'), ' ',
        PathJoinSubstitution([
            pkg_gazebo_race_modules, 'urdf',
            [LaunchConfiguration('size'), '_', LaunchConfiguration('track_type'),
             '_straight_', LaunchConfiguration('complexity'), '.urdf.xacro']
        ])
    ])

    # Set parameters
    set_ground_desc = SetParameter(name='ground_description', value=ground_description)
    set_edge_corner_desc = SetParameter(name='edge_corner_description', value=edge_corner_description)
    set_edge_straight_desc = SetParameter(name='edge_straight_description', value=edge_straight_description)
    set_corner_desc = SetParameter(name='corner_description', value=corner_description)
    set_straight_desc = SetParameter(name='straight_description', value=straight_description)

    return LaunchDescription([
        track_type_arg,
        barrier_type_arg,
        complexity_arg,
        size_arg,
        set_ground_desc,
        set_edge_corner_desc,
        set_edge_straight_desc,
        set_corner_desc,
        set_straight_desc
    ])
