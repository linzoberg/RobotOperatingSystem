#!/usr/bin/env python3
import math
from std_msgs.msg import Float32
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


class WallFollower:

    def __init__(self, target_dist: float, max_speed: float):
        self.target_dist = target_dist
        self.max_speed = max_speed
        self.dt = 0.05
        self._node = None
        self.pub_error = None
        self.pub_speed = None
        self.errors = []
        self.omegas = []

        # Состояния
        # DRIVE    — едем прямо до стены
        # TURN     — поворачиваем вправо на 90°
        # ALIGN    — выравниваемся по стене
        # FOLLOW   — едем вдоль стены с ПИД
        self.state = "DRIVE"

        # Для поворота на точный угол
        self.turn_start_yaw = None
        self.current_yaw    = 0.0

        # ПИД — очень мягкий
        self.kp = 0.6
        self.kd = 0.1
        self.prev_error = 0.0

    def set_node(self, node):
        self._node = node
        self.pub_error = node.create_publisher(
            Float32, '/wall_error', 10)
        self.pub_speed = node.create_publisher(
            Float32, '/wall_speed', 10)
        node.create_subscription(
            Odometry, '/odom', self._odom_cb, 10)

    def _odom_cb(self, msg):
        q = msg.pose.pose.orientation
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny, cosy)

    def reset(self):
        self.state          = "DRIVE"
        self.turn_start_yaw = None
        self.prev_error     = 0.0
        self.errors         = []
        self.omegas         = []

    def get_dist(self, scan, angle_deg):
        angle_rad = math.radians(angle_deg)
        idx = int((angle_rad - scan.angle_min) / scan.angle_increment)
        idx = max(0, min(idx, len(scan.ranges) - 1))
        r = scan.ranges[idx]
        if math.isfinite(r) and scan.range_min < r < scan.range_max:
            return r
        return 5.0

    def get_min(self, scan, start_deg, end_deg):
        vals = [self.get_dist(scan, a)
                for a in range(int(start_deg), int(end_deg)+1, 3)]
        return min(vals) if vals else 5.0

    def compute(self, scan: LaserScan):
        # Читаем датчики
        front      = self.get_min(scan, -25, 25)
        left_front = self.get_dist(scan, 45)
        left_90    = self.get_dist(scan, 90)
        left_back  = self.get_dist(scan, 135)

        v     = 0.0
        omega = 0.0
        error = 0.0

        # СОСТОЯНИЕ 1: DRIVE — едем прямо до стены
        if self.state == "DRIVE":
            if front < 0.6:
                # Нашли стену — поворачиваем вправо
                self.state          = "TURN"
                self.turn_start_yaw = self.current_yaw
                v     = 0.0
                omega = 0.0
                # self.log("Стена спереди ({:.2f}м)! Начинаю поворот".format(front))
            else:
                v     = self.max_speed
                omega = 0.0
                # self.log("DRIVE: еду прямо, front={:.2f}".format(front))

        # СОСТОЯНИЕ 2: TURN — поворот вправо на 90°
        elif self.state == "TURN":
            if self.turn_start_yaw is None:
                self.turn_start_yaw = self.current_yaw

            # Угол поворота (вправо = отрицательный)
            delta = self.turn_start_yaw - self.current_yaw
            delta = math.atan2(math.sin(delta), math.cos(delta))
            turned = math.degrees(abs(delta))

            if turned >= 88:
                self.state = "ALIGN"
                # self.log("Повернул на {}°. Выравниваюсь".format(int(turned)))
                v     = 0.0
                omega = 0.0
            else:
                v     = 0.0
                omega = -1.0
                # self.log("TURN: {}° из 90°".format(int(turned)))

        # СОСТОЯНИЕ 3: ALIGN — выравниваемся по стене
        # left_front (45°) ≈ left_back (135°) → параллельно
        elif self.state == "ALIGN":
            diff = left_front - left_back

            # Считаем что стена есть слева
            has_wall = left_90 < 2.0

            if not has_wall:
                # Стены нет — просто переходим в FOLLOW
                self.state = "FOLLOW"
                # self.log("Стены нет слева, перехожу в FOLLOW")
            elif abs(diff) < 0.04:
                # Параллельны!
                self.state      = "FOLLOW"
                self.prev_error = 0.0
                # self.log("Выровнялся! left={:.2f}".format(left_90))
            elif diff > 0:
                # Нос дальше от стены — крутим влево
                v     = 0.0
                omega = 0.35
                # self.log("ALIGN: нос от стены, влево. diff={:.3f}".format(diff))
            else:
                # Нос ближе к стене — крутим вправо
                v     = 0.0
                omega = -0.35
                # self.log("ALIGN: нос к стене, вправо. diff={:.3f}".format(diff))

        # СОСТОЯНИЕ 4: FOLLOW — едем вдоль стены
        elif self.state == "FOLLOW":

            # Стена впереди — новый поворот
            if front < 0.55:
                self.state          = "TURN"
                self.turn_start_yaw = self.current_yaw
                v     = 0.0
                omega = -1.0
                # self.log("FOLLOW: стена впереди! Поворачиваю")

            else:
                error = left_90 - self.target_dist

                # Мёртвая зона — если ошибка маленькая, едем ПРЯМО
                if abs(error) < 0.08:
                    omega = 0.0
                    v     = self.max_speed
                    # self.log("FOLLOW: прямо! left={:.2f}".format(left_90))
                else:
                    # ПИД только если отклонились сильно
                    deriv       = (error - self.prev_error) / self.dt
                    self.prev_error = error
                    omega       = self.kp * error + self.kd * deriv
                    omega       = max(-0.8, min(0.8, omega))
                    v           = self.max_speed * 0.8
                    # self.log("FOLLOW: корр. left={:.2f} err={:.3f} ω={:.2f}".format(
                        # left_90, error, omega))

                self.errors.append(error)
                self.omegas.append(omega)

        # Публикация для графиков
        if self.pub_error:
            msg      = Float32()
            msg.data = float(error)
            self.pub_error.publish(msg)
        if self.pub_speed:
            msg      = Float32()
            msg.data = float(omega)
            self.pub_speed.publish(msg)

        return v, omega

    def log(self, msg):
        if self._node:
            self._node.get_logger().info(
                msg, throttle_duration_sec=0.5)
