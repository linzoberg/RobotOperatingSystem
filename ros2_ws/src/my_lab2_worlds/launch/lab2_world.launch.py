import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    pkg = get_package_share_directory('my_lab2_worlds')
    world = os.path.join(pkg, 'worlds', 'lab2_gulyaev.sdf')

    return LaunchDescription([
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', '-v4', '--render-engine', 'ogre', world],
            output='screen'
        ),
        Node(
            package='ros_gz_bridge', executable='parameter_bridge',
            output='screen',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
                '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
                '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
                '/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V',
            ],
            parameters=[{'use_sim_time': True}]
        ),
    ])
