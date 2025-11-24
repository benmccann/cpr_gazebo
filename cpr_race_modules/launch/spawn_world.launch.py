import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get package directory
    pkg_gazebo_race_modules = get_package_share_directory('gazebo_race_modules')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Declare arguments
    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='true')
    gui_arg = DeclareLaunchArgument('gui', default_value='true')
    headless_arg = DeclareLaunchArgument('headless', default_value='false')

    world_name_arg = DeclareLaunchArgument(
        'world_name',
        default_value=os.path.join(pkg_gazebo_race_modules, 'worlds', 'actually_empty_world.world'),
        description='Path to world file'
    )

    # Gazebo server
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'])
        ]),
        launch_arguments={
            'gz_args': [LaunchConfiguration('world_name'), ' -r -s'],
            'on_exit_shutdown': 'true'
        }.items()
    )

    # Include object descriptions
    object_descriptions = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_gazebo_race_modules,
                'launch',
                'object_descriptions.launch.py'
            ])
        ])
    )

    return LaunchDescription([
        use_sim_time_arg,
        gui_arg,
        headless_arg,
        world_name_arg,
        gazebo_server,
        object_descriptions
    ])
