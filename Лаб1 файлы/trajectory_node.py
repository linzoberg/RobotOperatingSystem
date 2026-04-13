import rclpy
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from std_msgs.msg import Bool
from turtlesim.srv import TeleportAbsolute


class TrajectoryNode(Node):
    def __init__(self):
        super().__init__('trajectory_node')
        self.vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.pose_sub = self.create_subscription(Pose, '/turtle1/pose', self.pose_callback, 10)
        self.start_sub = self.create_subscription(Bool, '/start_trajectory', self.start_callback, 10)
        # Клиент сервиса телепортации
        self.teleport_client = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')
        # Параметры варианта №2 - Эллипс
        self.a = 3.5  # полуось по X
        self.b = 2.5  # полуось по Y
        self.cx = 5.5  # центр по X
        self.cy = 5.5  # центр по Y
        self.pose = None
        self.is_running = False
        self.t = 0.0  # параметр для движения по эллипсу
        self.timer = self.create_timer(0.05, self.control_loop)  # 20 Гц
        self.get_logger().info(f'Узел trajectory_node запущен. Эллипс: a={self.a}, b={self.b}')
        self.get_logger().info('Ожидание нажатия клавиши T...')

    def pose_callback(self, msg):
        self.pose = msg

    def start_callback(self, msg):
        if msg.data and not self.is_running:
            self.teleport_to_start()
            self.t = 0.0
            self.is_running = True
            self.get_logger().info('Начало движения по эллипсовидной траектории')

    def teleport_to_start(self):
        # Телепортация робота в начальную точку эллипса
        if not self.teleport_client.wait_for_service(timeout_sec=2.0):
            self.get_logger().error('Сервис телепортации недоступен!')
            return
        req = TeleportAbsolute.Request()
        req.x = self.cx + self.a
        req.y = self.cy
        req.theta = math.pi / 2.0  # начальная ориентация по касательной
        self.teleport_client.call_async(req)

    def control_loop(self):
        if not self.is_running or self.pose is None:
            return
        # Вычисление целевой точки на эллипсе
        target_x = self.cx + self.a * math.cos(self.t)
        target_y = self.cy + self.b * math.sin(self.t)
        # Ошибки
        dx = target_x - self.pose.x
        dy = target_y - self.pose.y
        distance = math.hypot(dx, dy)
        target_angle = math.atan2(dy, dx)
        angle_error = target_angle - self.pose.theta
        # Нормализация угла в диапазон [-pi, pi]
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi
        # П-регулятор
        cmd = Twist()
        cmd.linear.x = min(2.0 * distance, 2.0)  # ограничиваем максимальную скорость
        cmd.angular.z = 6.0 * angle_error
        self.vel_pub.publish(cmd)
        # Переход к следующей точке
        if distance < 0.12:
            self.t += 0.045
        # Завершение движения после полного оборота
        if self.t >= 2 * math.pi:
            self.is_running = False
            self.vel_pub.publish(Twist())  # остановка
            self.get_logger().info('Движение по эллипсу завершено')


def main(args=None):
    rclpy.init(args=args)
    node = TrajectoryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()