#!/usr/bin/env python3
"""
Нода навигации TurtleBot3 Waffle по заданным координатам.
Робот последовательно перемещается в указанные точки,
обходя препятствия с помощью Nav2.
"""

import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped
import math
import time


def create_pose(navigator, x, y, yaw=0.0):
    """Создаёт PoseStamped сообщение с заданными координатами."""
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0
    # Конвертируем угол yaw в кватернион
    pose.pose.orientation.z = math.sin(yaw / 2.0)
    pose.pose.orientation.w = math.cos(yaw / 2.0)
    return pose


def main():
    rclpy.init()

    navigator = BasicNavigator()

    # --- Устанавливаем начальную позицию робота (для AMCL) ---
    # Робот стартует в центре коридора (0, 0)
    initial_pose = create_pose(navigator, 0.0, 0.0, 0.0)
    navigator.setInitialPose(initial_pose)

    # Ждём пока Nav2 полностью активируется
    navigator.get_logger().info('Ожидание активации Nav2...')
    navigator.waitUntilNav2Active()
    navigator.get_logger().info('Nav2 активирован!')

    # --- Список целевых точек ---
    # Робот поедет по маршруту через разные комнаты
    # На пути будут препятствия (мебель), которые он объедет
    waypoints = [
        # Точка 1: Кабинет (правый нижний угол)
        {'x': 3.0, 'y': -3.0, 'yaw': -1.57, 'name': 'Кабинет'},
        # Точка 2: Коридор (центр)
        {'x': 0.0, 'y': 0.0, 'yaw': 0.0, 'name': 'Коридор'},
        # Точка 3: Правая часть коридора (мимо мебели)
        {'x': 4.0, 'y': 0.0, 'yaw': 0.0, 'name': 'Правый коридор'},
        # Точка 4: Возврат в центр
        {'x': 0.0, 'y': 0.0, 'yaw': 0.0, 'name': 'Коридор (старт)'},
    ]
    # --- Последовательная навигация по точкам ---
    for i, wp in enumerate(waypoints):
        navigator.get_logger().info(
            f'[{i+1}/{len(waypoints)}] Еду в: {wp["name"]} '
            f'(x={wp["x"]}, y={wp["y"]})'
        )

        goal_pose = create_pose(navigator, wp['x'], wp['y'], wp['yaw'])
        navigator.goToPose(goal_pose)

        # Ждём пока робот доедет
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                # Показываем оставшееся расстояние
                distance = feedback.distance_remaining
                navigator.get_logger().info(
                    f'  Осталось: {distance:.2f} м'
                )
            time.sleep(1)

        # Проверяем результат
        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            navigator.get_logger().info(
                f'✅ Точка "{wp["name"]}" достигнута!'
            )
        elif result == TaskResult.CANCELED:
            navigator.get_logger().warn(
                f'⚠️ Навигация к "{wp["name"]}" отменена'
            )
        elif result == TaskResult.FAILED:
            navigator.get_logger().error(
                f'❌ Не удалось доехать до "{wp["name"]}"'
            )

        # Пауза между точками
        time.sleep(2)

    navigator.get_logger().info('🏁 Маршрут завершён!')
    navigator.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
