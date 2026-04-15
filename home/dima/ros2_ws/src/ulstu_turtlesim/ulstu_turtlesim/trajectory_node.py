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
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.pose_cb, 10)
        self.create_subscription(Bool, '/start_trajectory', self.start_cb, 10)
        
        # Клиент для телепортации
        self.teleport = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')

        self.pose = None
        self.run_flag = False
        self.t = 0.0
        
        # Эллипс
        self.a = 3.5  # полуось X
        self.b = 2.5  # полуось Y
        self.cx = 5.5 # центр поля
        self.cy = 5.5
        
        self.timer = self.create_timer(0.05, self.loop)
        self.get_logger().info(f'Эллипс готов a={self.a} b={self.b}. Нажми T')

    def pose_cb(self, msg): 
        self.pose = msg

    def start_cb(self, msg):
        if msg.data and not self.run_flag:
            # Мгновенно переносим черепаху в стартовую точку эллипса
            self.teleport.wait_for_service(timeout_sec=1.0)
            req = TeleportAbsolute.Request()
            req.x = self.cx + self.a
            req.y = self.cy
            req.theta = math.pi / 2.0  # по касательной к эллипсу
            self.teleport.call_async(req)
            
            self.t = 0.0
            self.run_flag = True
            self.get_logger().info('>>> Старт с телепортом')

    def loop(self):
        if not self.run_flag or not self.pose: 
            return
            
        tx = self.cx + self.a * math.cos(self.t)
        ty = self.cy + self.b * math.sin(self.t)
        
        dx, dy = tx - self.pose.x, ty - self.pose.y
        dist = math.hypot(dx, dy)
        
        target_angle = math.atan2(dy, dx)
        err = target_angle - self.pose.theta
        err = (err + math.pi) % (2*math.pi) - math.pi
        
        cmd = Twist()
        cmd.linear.x = min(2.0 * dist, 2.0)
        cmd.angular.z = 6.0 * err
        self.pub.publish(cmd)

        if dist < 0.1: 
            self.t += 0.05
            
        if self.t > 2 * math.pi:
            self.run_flag = False
            self.pub.publish(Twist())
            self.get_logger().info('Эллипс завершен')

def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(TrajectoryNode())
    rclpy.shutdown()

if __name__ == '__main__':
    main()
