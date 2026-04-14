import rclpy, sys, tty, termios, select
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.start_pub = self.create_publisher(Bool, '/start_trajectory', 10)
        self.speed, self.turn = 1.0, 1.0
        self.settings = termios.tcgetattr(sys.stdin)
        self.get_logger().info('Управление: W/S-вперед/назад A/D-влево/вправо Q/E-скор+/- T-эллипс')

    def get_key(self):
        tty.setraw(sys.stdin.fileno())
        r, _, _ = select.select([sys.stdin], [], [], 0.1)
        key = sys.stdin.read(1) if r else ''
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        twist = Twist()
        while rclpy.ok():
            key = self.get_key()
            if key == 'w': twist.linear.x, twist.angular.z = self.speed, 0.0
            elif key == 's': twist.linear.x, twist.angular.z = -self.speed, 0.0
            elif key == 'a': twist.linear.x, twist.angular.z = 0.0, self.turn
            elif key == 'd': twist.linear.x, twist.angular.z = 0.0, -self.turn
            elif key == 'q': self.speed += 0.2; self.turn += 0.2; continue
            elif key == 'e': self.speed = max(0.1,self.speed-0.2); continue
            elif key == 't': self.start_pub.publish(Bool(data=True)); self.get_logger().info('>>> Запуск эллипса'); continue
            elif key == 'x': twist = Twist()
            elif key == '\x03': break
            else: continue
            self.cmd_pub.publish(twist)

def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    try: node.run()
    finally: node.destroy_node(); rclpy.shutdown()
