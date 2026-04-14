#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import AppendEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    # Пути к пакетам
    turtlebot3_gazebo_dir = get_package_share_directory('turtlebot3_gazebo')
    launch_file_dir = os.path.join(turtlebot3_gazebo_dir, 'launch')
    ros_gz_sim_dir = get_package_share_directory('ros_gz_sim')

    # Параметры
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Начальная позиция робота (коридор — центр карты)
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')

    # Путь к нашему миру
    world = os.path.join(
        os.path.expanduser('~'),
        'ros2_ws', 'src', 'lab2_world', 'worlds', 'lab2_world.sdf'
    )

    # Запуск Gazebo сервера (физика)
    gzserver_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': ['-r -s -v2 ', world],
            'on_exit_shutdown': 'true'
        }.items()
    )

    # Запуск Gazebo клиента (визуализация)
    gzclient_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_dir, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={
            'gz_args': '-g -v2 ',
            'on_exit_shutdown': 'true'
        }.items()
    )

    # Публикация описания робота (URDF -> /robot_description, /tf)
    robot_state_publisher_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'robot_state_publisher.launch.py')
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items()
    )

    # Спавн робота + мост Gazebo <-> ROS 2 (включая TwistStamped)
    spawn_turtlebot_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(launch_file_dir, 'spawn_turtlebot3.launch.py')
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose
        }.items()
    )

    # Добавляем путь к моделям TurtleBot3
    set_env_vars_resources = AppendEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(turtlebot3_gazebo_dir, 'models')
    )

    ld = LaunchDescription()

    ld.add_action(set_env_vars_resources)
    ld.add_action(gzserver_cmd)
    ld.add_action(gzclient_cmd)
    ld.add_action(robot_state_publisher_cmd)
    ld.add_action(spawn_turtlebot_cmd)

    return ld
