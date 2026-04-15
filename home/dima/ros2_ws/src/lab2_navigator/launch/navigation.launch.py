#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    map_file = os.path.join(
        os.path.expanduser('~'),
        'ros2_ws', 'src', 'lab2_world', 'maps', 'lab2_map.yaml'
    )

    nav2_params = os.path.join(
        get_package_share_directory('nav2_bringup'),
        'params', 'nav2_params.yaml'
    )

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch', 'bringup_launch.py'
            )
        ),
        launch_arguments={
            'map': map_file,
            'use_sim_time': use_sim_time,
            'params_file': nav2_params,
            'autostart': 'true',
        }.items()
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('nav2_bringup'),
                'launch', 'rviz_launch.py'
            )
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
        }.items()
    )

    ld = LaunchDescription()
    ld.add_action(nav2_launch)
    ld.add_action(rviz_launch)

    return ld
