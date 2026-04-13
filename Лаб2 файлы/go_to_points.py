# Программа автономной навигации по точкам с обходом препятствий.
# Используется Nav2 (AMCL + Planner), работающий в ROS 2 Jazzy.

import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import time

class PointsFollower(Node):
    def __init__(self):
        super().__init__('points_follower')
        self.navigator = BasicNavigator()

    def create_pose(self, x, y, yaw):
        """Создает цель для Nav2 в формате PoseStamped"""
        pose = PoseStamped()
        pose.header.frame_id = 'map'
        pose.header.stamp = self.navigator.get_clock().now().to_msg()
        pose.pose.position.x = x
        pose.pose.position.y = y
        # простая ориентация по yaw
        pose.pose.orientation.z = 0.0
        pose.pose.orientation.w = 1.0
        return pose

def main():
    rclpy.init()
    node = PointsFollower()
    
    # Ждем пока Nav2 полностью запустится
    node.navigator.waitUntilNav2Active()
    node.get_logger().info("Nav2 активен. Стартуем маршрут.")

    # Точки маршрута (взяты из мира 12х12)
    route = [
        (3.0, 3.5, 0.0),   # Комната 1, у стола
        (-4.0, 3.0, 0.0),  # Комната 2, у дивана
        (0.0, -2.0, 0.0),  # Коридор, объезд препятствия
    ]

    for i, (x, y, yaw) in enumerate(route):
        goal = node.create_pose(x, y, yaw)
        node.get_logger().info(f"Отправляю цель {i+1}: x={x}, y={y}")
        node.navigator.goToPose(goal)

        while not node.navigator.isTaskComplete():
            feedback = node.navigator.getFeedback()
            time.sleep(0.5)
        
        result = node.navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            node.get_logger().info(f"Цель {i+1} достигнута")
        else:
            node.get_logger().warn(f"Цель {i+1} НЕ достигнута")

    node.get_logger().info("Маршрут завершен")
    rclpy.shutdown()

if __name__ == '__main__':
    main()
