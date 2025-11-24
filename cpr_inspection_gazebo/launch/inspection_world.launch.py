import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command, FindExecutable
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Get package directories
    pkg_cpr_inspection_gazebo = get_package_share_directory('cpr_inspection_gazebo')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Declare arguments
    platform_arg = DeclareLaunchArgument(
        'platform',
        default_value=os.environ.get('CPR_GAZEBO_PLATFORM', 'husky'),
        description='Robot platform to spawn'
    )

    robot_x_arg = DeclareLaunchArgument('robot_x', default_value='0.0')
    robot_y_arg = DeclareLaunchArgument('robot_y', default_value='0.0')
    robot_z_arg = DeclareLaunchArgument('robot_z', default_value='0.2')
    robot_yaw_arg = DeclareLaunchArgument('robot_yaw', default_value='0.0')

    world_x_arg = DeclareLaunchArgument('world_x', default_value='0.0')
    world_y_arg = DeclareLaunchArgument('world_y', default_value='0.0')
    world_z_arg = DeclareLaunchArgument('world_z', default_value='0.0')
    world_yaw_arg = DeclareLaunchArgument('world_yaw', default_value='0.0')

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time', default_value='true')
    gui_arg = DeclareLaunchArgument('gui', default_value='true')
    headless_arg = DeclareLaunchArgument('headless', default_value='false')

    world_name_arg = DeclareLaunchArgument(
        'world_name',
        default_value=os.path.join(pkg_cpr_inspection_gazebo, 'worlds', 'actually_empty_world.world'),
        description='Path to world file'
    )

    # Process inspection geometry URDF
    inspection_geom_xacro = os.path.join(pkg_cpr_inspection_gazebo, 'urdf', 'inspection_geometry.urdf.xacro')
    inspection_geom_urdf = Command([
        FindExecutable(name='xacro'), ' ', inspection_geom_xacro
    ])

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

    # Gazebo client (GUI)
    gazebo_client = ExecuteProcess(
        cmd=['gz', 'sim', '-g'],
        output='screen',
        condition=IfCondition(LaunchConfiguration('gui'))
    )

    # Spawn inspection world geometry
    spawn_inspection_geometry = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-topic', 'robot_description',
            '-name', 'inspection_geometry',
            '-x', LaunchConfiguration('world_x'),
            '-y', LaunchConfiguration('world_y'),
            '-z', LaunchConfiguration('world_z'),
            '-Y', LaunchConfiguration('world_yaw')
        ],
        output='screen'
    )

    # Include platform-specific spawn launch file
    platform_spawn = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                pkg_cpr_inspection_gazebo,
                'launch',
                ['spawn_', LaunchConfiguration('platform'), '.launch.py']
            ])
        ]),
        launch_arguments={
            'x': LaunchConfiguration('robot_x'),
            'y': LaunchConfiguration('robot_y'),
            'z': LaunchConfiguration('robot_z'),
            'yaw': LaunchConfiguration('robot_yaw')
        }.items()
    )

    return LaunchDescription([
        platform_arg,
        robot_x_arg,
        robot_y_arg,
        robot_z_arg,
        robot_yaw_arg,
        world_x_arg,
        world_y_arg,
        world_z_arg,
        world_yaw_arg,
        use_sim_time_arg,
        gui_arg,
        headless_arg,
        world_name_arg,
        gazebo_server,
        gazebo_client,
        spawn_inspection_geometry,
        platform_spawn
    ])
