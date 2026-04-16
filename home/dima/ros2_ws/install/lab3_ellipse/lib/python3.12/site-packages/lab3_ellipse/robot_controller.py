#!/usr/bin/env python3
"""
Главный файл — автоматная модель управления роботом.
Состояния:
  1. MANUAL   — ручное управление (W/A/S/D)
  2. ELLIPSE  — автоматическое движение по эллипсу
  3. WALL     — движение вдоль стены (PID)

Клавиши:
  W/A/S/D     — движение вручную
  Q/E         — поворот влево/вправо
  1           — режим MANUAL
  2           — режим ELLIPSE (начать эллипс с текущей позиции)
  3           — режим WALL (движение вдоль стены)
  Space       — стоп
  Ctrl+C      — выход
"""

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import math
import sys
import tty
import termios
import threading

from lab3_ellipse.ellipse_motion import EllipseMotion
from lab3_ellipse.wall_follower import WallFollower


# Состояния автомата
STATE_MANUAL  = 1
STATE_ELLIPSE = 2
STATE_WALL    = 3

STATE_NAMES = {
    STATE_MANUAL:  'РУЧНОЕ УПРАВЛЕНИЕ',
    STATE_ELLIPSE: 'ДВИЖЕНИЕ ПО ЭЛЛИПСУ',
    STATE_WALL:    'ДВИЖЕНИЕ ВДОЛЬ СТЕНЫ',
}


def get_key(settings):
    """Читает одну клавишу без Enter."""
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')

        # --- Параметры ---
        self.declare_parameter('a', 1.0)          # полуось эллипса X
        self.declare_parameter('b', 0.5)          # полуось эллипса Y
        self.declare_parameter('speed', 0.5)     # линейная скорость
        self.declare_parameter('wall_dist', 0.5)  # дистанция до стены

        self.a          = self.get_parameter('a').value
        self.b          = self.get_parameter('b').value
        self.speed      = self.get_parameter('speed').value
        self.wall_dist  = self.get_parameter('wall_dist').value

        # --- Состояние автомата ---
        self.state = STATE_MANUAL

        # --- Текущая поза робота ---
        self.cur_x   = 0.0
        self.cur_y   = 0.0
        self.cur_yaw = 0.0

        # --- Данные лидара ---
        self.scan_data = None

        # --- Модули ---
        self.ellipse = EllipseMotion(self.a, self.b, self.speed)
        self.wall    = WallFollower(self.wall_dist, self.speed)
        self.wall.set_node(self)

        # --- Publisher ---
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)

        # --- Subscribers ---
        self.create_subscription(Odometry,   '/odom', self.odom_callback,  10)
        self.create_subscription(LaserScan,  '/scan', self.scan_callback,  10)

        # --- Таймер управления 20 Гц ---
        self.timer = self.create_timer(0.05, self.control_loop)

        # --- Ручное управление ---
        self.manual_v     = 0.0
        self.manual_omega = 0.0

        # --- Печатаем подсказку ---
        self.print_help()

        # --- Поток чтения клавиш ---
        self.settings = termios.tcgetattr(sys.stdin)
        self.key_thread = threading.Thread(target=self.key_loop, daemon=True)
        self.key_thread.start()

    # =========================================================
    #  CALLBACKS
    # =========================================================

    def odom_callback(self, msg):
        self.cur_x = msg.pose.pose.position.x
        self.cur_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.cur_yaw = math.atan2(siny, cosy)

    def scan_callback(self, msg):
        self.scan_data = msg

    # =========================================================
    #  ГЛАВНЫЙ ЦИКЛ УПРАВЛЕНИЯ
    # =========================================================

    def control_loop(self):
        v     = 0.0
        omega = 0.0

        if self.state == STATE_MANUAL:
            v     = self.manual_v
            omega = self.manual_omega

        elif self.state == STATE_ELLIPSE:
            v, omega, done = self.ellipse.compute(
                self.cur_x, self.cur_y, self.cur_yaw)
            if done:
                self.get_logger().info('Эллипс завершён! Переключаюсь в MANUAL.')
                self.state = STATE_MANUAL
                v = 0.0
                omega = 0.0

        elif self.state == STATE_WALL:
            if self.scan_data is not None:
                v, omega = self.wall.compute(self.scan_data)
            else:
                v = 0.0
                omega = 0.0

        self.publish_cmd(v, omega)

    # =========================================================
    #  ПУБЛИКАЦИЯ КОМАНДЫ
    # =========================================================

    def publish_cmd(self, v, omega):
        msg = TwistStamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        msg.twist.linear.x  = float(v)
        msg.twist.angular.z = float(omega)
        self.pub.publish(msg)

    def stop(self):
        self.publish_cmd(0.0, 0.0)

    # =========================================================
    #  КЛАВИАТУРА
    # =========================================================

    def key_loop(self):
        self.get_logger().info('Поток клавиатуры запущен.')
        while rclpy.ok():
            key = get_key(self.settings)

            # --- Смена состояний ---
            if key == '1':
                self.state = STATE_MANUAL
                self.manual_v = 0.0
                self.manual_omega = 0.0
                self.stop()
                self.get_logger().info(f'Режим: {STATE_NAMES[self.state]}')

            elif key == '2':
                # Запускаем эллипс с текущей позиции
                self.ellipse.start(self.cur_x, self.cur_y, self.cur_yaw)
                self.state = STATE_ELLIPSE
                self.get_logger().info(
                    f'Режим: {STATE_NAMES[self.state]} | '
                    f'Старт: ({self.cur_x:.2f}, {self.cur_y:.2f}) '
                    f'yaw={math.degrees(self.cur_yaw):.1f}°')

            elif key == '3':
                self.wall.reset()
                self.state = STATE_WALL
                self.get_logger().info(f'Режим: {STATE_NAMES[self.state]}')

            # --- Ручное управление ---
            elif key == 'w':
                self.manual_v = min(self.manual_v + 0.05, self.speed)
            elif key == 's':
                self.manual_v = max(self.manual_v - 0.05, -self.speed)
            elif key == 'a':
                self.manual_omega = min(self.manual_omega + 0.1, 1.5)
            elif key == 'd':
                self.manual_omega = max(self.manual_omega - 0.1, -1.5)
            elif key == 'q':
                self.manual_omega = min(self.manual_omega + 0.2, 1.5)
            elif key == 'e':
                self.manual_omega = max(self.manual_omega - 0.2, -1.5)
            elif key == ' ':
                self.manual_v = 0.0
                self.manual_omega = 0.0
                self.stop()
                self.get_logger().info('СТОП')

            # --- Выход ---
            elif key == '\x03':  # Ctrl+C
                self.stop()
                rclpy.shutdown()
                break

    # =========================================================
    #  ПОМОЩЬ
    # =========================================================

    def print_help(self):
        msg = """
╔══════════════════════════════════════════════╗
║         УПРАВЛЕНИЕ РОБОТОМ  TurtleBot3       ║
╠══════════════════════════════════════════════╣
║  W / S     — вперёд / назад                 ║
║  A / D     — поворот влево / вправо         ║
║  Q / E     — резкий поворот влево / вправо  ║
║  SPACE     — стоп                           ║
║─────────────────────────────────────────────║
║  1         — РУЧНОЕ УПРАВЛЕНИЕ              ║
║  2         — ДВИЖЕНИЕ ПО ЭЛЛИПСУ            ║
║  3         — ДВИЖЕНИЕ ВДОЛЬ СТЕНЫ (PID)     ║
║─────────────────────────────────────────────║
║  Ctrl+C    — выход                          ║
╚══════════════════════════════════════════════╝
"""
        print(msg)


def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.stop()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
