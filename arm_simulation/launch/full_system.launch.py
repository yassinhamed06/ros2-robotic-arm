from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

import os


def generate_launch_description():

    hardware = LaunchConfiguration('hardware')

    simulation_path = os.path.join(
        get_package_share_directory('arm_simulation'),
        'launch',
        'simulation.launch.py'
    )

    return LaunchDescription([

        DeclareLaunchArgument(
            'hardware',
            default_value='false'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(simulation_path)
        ),

        Node(
            package='arm_control',
            executable='serial_bridge',
            name='serial_bridge',
            output='screen',
            condition=IfCondition(hardware)
        ),

        Node(
            package='arm_control',
            executable='control_gui',
            name='control_gui',
            output='screen'
        )

    ])
