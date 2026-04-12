import rclpy
import sys
import tty
import termios
import select
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool


class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.start_pub = self.create_publisher(Bool, '/start_trajectory', 10)
        self.speed = 1.0
        self.turn = 1.0
        self.settings = termios.tcgetattr(sys.stdin)
        self.get_logger().info('Управление:')
        self.get_logger().info('W/S - движение вперед/назад')
        self.get_logger().info('A/D - поворот влево/вправо')
        self.get_logger().info('Q/E - увеличение/уменьшение скорости')
        self.get_logger().info('T - запуск движения по эллипсу')
        self.get_logger().info('Ctrl+C - выход')

    def get_key(self):
        # Чтение нажатия клавиши без необходимости нажимать Enter
        tty.setraw(sys.stdin.fileno())
        r, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if r else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        twist = Twist()
        while rclpy.ok():
            key = self.get_key()
            if key == 'w':
                twist.linear.x = self.speed
                twist.angular.z = 0.0
            elif key == 's':
                twist.linear.x = -self.speed
                twist.angular.z = 0.0
            elif key == 'a':
                twist.linear.x = 0.0
                twist.angular.z = self.turn
            elif key == 'd':
                twist.linear.x = 0.0
                twist.angular.z = -self.turn
            elif key == 'q':
                self.speed += 0.2
                self.turn += 0.2
                self.get_logger().info(f'Скорость увеличена: {self.speed:.1f}')
                continue
            elif key == 'e':
                self.speed = max(0.2, self.speed - 0.2)
                self.turn = max(0.2, self.turn - 0.2)
                self.get_logger().info(f'Скорость уменьшена: {self.speed:.1f}')
                continue
            elif key == 't':
                self.start_pub.publish(Bool(data=True))
                self.get_logger().info('>>> Запуск движения по эллипсу')
                continue
            elif key == '\x03':  # Ctrl+C
                break
            else:
                twist.linear.x = 0.0
                twist.angular.z = 0.0
            self.cmd_pub.publish(twist)

    def destroy_node(self):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()