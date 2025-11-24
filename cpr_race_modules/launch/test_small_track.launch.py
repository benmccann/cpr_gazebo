import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get package directory
    pkg_gazebo_race_modules = get_package_share_directory('gazebo_race_modules')

    # Declare arguments
    track_type_arg = DeclareLaunchArgument('track_type', default_value='road')
    barrier_type_arg = DeclareLaunchArgument('barrier_type', default_value='racing')
    complexity_arg = DeclareLaunchArgument('complexity', default_value='simple')
    size_arg = DeclareLaunchArgument('size', default_value='small')

    # Include spawn_world
    spawn_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_gazebo_race_modules,
                'launch',
                'spawn_world.launch.py'
            ])
        ])
    )

    # Include object_descriptions with all args passed through
    object_descriptions = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_gazebo_race_modules,
                'launch',
                'object_descriptions.launch.py'
            ])
        ]),
        launch_arguments={
            'track_type': LaunchConfiguration('track_type'),
            'barrier_type': LaunchConfiguration('barrier_type'),
            'complexity': LaunchConfiguration('complexity'),
            'size': LaunchConfiguration('size')
        }.items()
    )

    # Spawn track pieces (straights and corners)
    track_spawns = [
        # Straight pieces
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight1', '-param', 'straight_description', '-x', '0', '-y', '0', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight2', '-param', 'straight_description', '-x', '1', '-y', '0', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight3', '-param', 'straight_description', '-x', '2', '-y', '1', '-z', '0', '-Y', '1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight4', '-param', 'straight_description', '-x', '2', '-y', '2', '-z', '0', '-Y', '1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight5', '-param', 'straight_description', '-x', '0', '-y', '2', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight6', '-param', 'straight_description', '-x', '-1', '-y', '2', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight7', '-param', 'straight_description', '-x', '-2', '-y', '1', '-z', '0', '-Y', '1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'straight8', '-param', 'straight_description', '-x', '-1', '-y', '0', '-z', '0', '-Y', '0'], output='screen'),

        # Corner pieces
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'corner1', '-param', 'corner_description', '-x', '2', '-y', '0', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'corner2', '-param', 'corner_description', '-x', '2', '-y', '3', '-z', '0', '-Y', '-1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'corner3', '-param', 'corner_description', '-x', '1', '-y', '3', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'corner4', '-param', 'corner_description', '-x', '1', '-y', '2', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'corner5', '-param', 'corner_description', '-x', '-2', '-y', '2', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'corner6', '-param', 'corner_description', '-x', '-2', '-y', '0', '-z', '0', '-Y', '1.5707'], output='screen'),

        # Edge straight pieces
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight1', '-param', 'edge_straight_description', '-x', '0', '-y', '0', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight2', '-param', 'edge_straight_description', '-x', '1', '-y', '0', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight3', '-param', 'edge_straight_description', '-x', '2', '-y', '1', '-z', '0', '-Y', '1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight4', '-param', 'edge_straight_description', '-x', '2', '-y', '2', '-z', '0', '-Y', '1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight5', '-param', 'edge_straight_description', '-x', '0', '-y', '2', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight6', '-param', 'edge_straight_description', '-x', '-1', '-y', '2', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight7', '-param', 'edge_straight_description', '-x', '-2', '-y', '1', '-z', '0', '-Y', '1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_straight8', '-param', 'edge_straight_description', '-x', '-1', '-y', '0', '-z', '0', '-Y', '0'], output='screen'),

        # Edge corner pieces
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_corner1', '-param', 'edge_corner_description', '-x', '2', '-y', '0', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_corner2', '-param', 'edge_corner_description', '-x', '2', '-y', '3', '-z', '0', '-Y', '-1.5707'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_corner3', '-param', 'edge_corner_description', '-x', '1', '-y', '3', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_corner4', '-param', 'edge_corner_description', '-x', '1', '-y', '2', '-z', '0', '-Y', '3.14159'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_corner5', '-param', 'edge_corner_description', '-x', '-2', '-y', '2', '-z', '0', '-Y', '0'], output='screen'),
        ExecuteProcess(cmd=['ros2', 'run', 'ros_gz_sim', 'create', '-name', 'edge_corner6', '-param', 'edge_corner_description', '-x', '-2', '-y', '0', '-z', '0', '-Y', '1.5707'], output='screen'),
    ]

    return LaunchDescription([
        track_type_arg,
        barrier_type_arg,
        complexity_arg,
        size_arg,
        spawn_world,
        object_descriptions,
    ] + track_spawns)
