import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import (
    get_package_share_directory,
    get_package_prefix
)


def generate_launch_description():

    description_dir = get_package_share_directory('arm_description')
    simulation_dir = get_package_share_directory('arm_simulation')

    urdf_file = os.path.join(
        description_dir, 'urdf', 'arm.urdf'
    )

    rviz_file = os.path.join(
        description_dir, 'rviz', 'arm.rviz'
    )

    world_file = os.path.join(
        simulation_dir, 'worlds', 'arm_world.sdf'
    )

    controllers_file = os.path.join(
        simulation_dir, 'config', 'controllers.yaml'
    )

    plugin_file = os.path.join(
        get_package_prefix('gz_ros2_control'),
        'lib',
        'libgz_ros2_control-system.so'
    )

    with open(urdf_file, 'r') as file:
        robot_description = file.read()

    robot_description = robot_description.replace(
        '__CONTROL_PLUGIN__', plugin_file
    )

    robot_description = robot_description.replace(
        '__CONTROLLERS_FILE__', controllers_file
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': ParameterValue(
                robot_description, value_type=str
            ),
            'use_sim_time': True
        }],
        output='screen'
    )

    gazebo = ExecuteProcess(
        cmd=['ign', 'gazebo', '-r', world_file],
        output='screen'
    )

    clock_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
        ],
        output='screen'
    )

    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', '/robot_description',
            '-name', 'robotic_arm'
        ],
        output='screen'
    )

    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '-c', '/controller_manager',
            '--controller-manager-timeout', '60'
        ],
        output='screen'
    )

    arm_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'arm_controller',
            '-c', '/controller_manager',
            '-p', controllers_file,
            '--controller-manager-timeout', '60'
        ],
        output='screen'
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([

        RegisterEventHandler(
            OnProcessExit(
                target_action=spawn_robot,
                on_exit=[joint_state_broadcaster]
            )
        ),

        RegisterEventHandler(
            OnProcessExit(
                target_action=joint_state_broadcaster,
                on_exit=[arm_controller]
            )
        ),

        robot_state_publisher,
        gazebo,
        clock_bridge,
        spawn_robot,
        rviz

    ])
