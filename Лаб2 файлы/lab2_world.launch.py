import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_worlds = get_package_share_directory('my_lab2_worlds')
    world = os.path.join(pkg_worlds, 'worlds', 'lab2_gulyaev.sdf')

    # Берем модель из переменной окружения
    model = os.environ.get('TURTLEBOT3_MODEL', 'waffle_pi')
    urdf_path = os.path.join(get_package_share_directory('turtlebot3_description'), 'urdf', f'turtlebot3_{model}.urdf')
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        # Gazebo Sim
        Node(package='ros_gz_sim', executable='gz_sim', output='screen',
             arguments=['-r', '-v4', world], parameters=[{'use_sim_time': True}]),
        # Появление робота
        Node(package='ros_gz_sim', executable='create', output='screen',
             arguments=['-name', model, '-string', robot_desc, '-x', '0', '-y', '-4.5', '-z', '0.1']),
        # robot_state_publisher
        Node(package='robot_state_publisher', executable='robot_state_publisher', output='screen',
             parameters=[{'robot_description': robot_desc, 'use_sim_time': True}]),
        # МОСТ ROS2 <-> Gazebo
        Node(package='ros_gz_bridge', executable='parameter_bridge', output='screen',
             arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
                '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
             ], parameters=[{'use_sim_time': True}]),
    ])
