sudo apt update && sudo apt upgrade -y
lsb_release -a
sudo apt install locales software-properties-common curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
sudo apt update
ping -c 3 8.8.8.8
ping -c 3 google.com
sudo nano /etc/wsl.conf
# 1. Отключаем авто-генерацию кривого resolv.conf
sudo nano /etc/wsl.conf
sudo rm /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
echo "nameserver 1.1.1.1" | sudo tee -a /etc/resolv.conf
exit
sudo apt update
sudo apt install curl gnupg2 lsb-release software-properties-common -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install ros-jazzy-desktop python3-colcon-common-extensions git -y
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
source ~/.bashrc
printenv ROS_DISTRO
ros2 run turtlesim turtlesim_node
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src
git clone https://github.com/ulstu/robotics.git
cp -r robotics/practice/2025/projects/labs/ulstu_turtlesim .
rm -rf robotics
cd ~/ros2_ws
colcon build --symlink-install
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
ros2 launch ulstu_turtlesim lab1.launch.py
ros2 pkg executables ulstu_turtlesim
nano ~/ros2_ws/src/ulstu_turtlesim/ulstu_turtlesim/trajectory_node.py
pwd
ls -l
tree -L 2
nano ~/ros2_ws/src/ulstu_turtlesim/setup.py
nano ~/ros2_ws/src/ulstu_turtlesim/ulstu_turtlesim/teleop_node.py
nano ~/ros2_ws/src/ulstu_turtlesim/ulstu_turtlesim/trajectory_node.py
cd ~/ros2_ws
colcon build --symlink-install
source ~/.bashrc
ros2 pkg executables ulstu_turtlesim
ros2 run ulstu_turtlesim trajectory_node
ros2 run ulstu_turtlesim teleop_node
ros2 run ulstu_turtlesim trajectory_node
rqt_graph
ros2 run turtlesim turtlesim_node
nano ~/ros2_ws/src/ulstu_turtlesim/ulstu_turtlesim/trajectory_node.py
cd ~/ros2_ws
colcon build --symlink-install
source ~/.bashrc
ros2 run ulstu_turtlesim teleop_node
rqt_graph
ros2 run ulstu_turtlesim trajectory_node
ros2 run turtlesim turtlesim_node
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake lab2_world
cd lab2_world
mkdir worlds models
nano worlds/lab2_world.sdf
cd ~/ros2_ws
colcon build
source install/setup.bash
gz sim ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
sudo apt update && sudo apt upgrade -y
sudo apt install -y gz-harmonic ros-jazzy-ros-gz ros-jazzy-ros-gz-bridge      ros-jazzy-ros-gz-sim ros-jazzy-ros-gz-interfaces
sudo apt install -y ros-jazzy-turtlebot3* ros-jazzy-turtlebot3-msgs
gz --version
echo $ROS_DISTRO
ros2 pkg list | grep -E 'turtlebot3|gz|nav2|slam_toolbox'
gz sim -v 3 shapes.sdf
find / -name "gz" -type f 2>/dev/null
rviz2
ros2 run turtlebot3_teleop teleop_keyboard
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
which gz sim 2>/dev/null
source /opt/ros/jazzy/setup.bash
gz sim shapes.sdf
source /opt/ros/jazzy/setup.bash
gz sim shapes.sdf
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc
nano ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
gz sim ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
nano ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
gz sim ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
ros2 pkg prefix turtlebot3_gazebo
ls $(ros2 pkg prefix turtlebot3_gazebo)/share/turtlebot3_gazebo/launch/
ls $(ros2 pkg prefix turtlebot3_gazebo)/share/turtlebot3_gazebo/worlds/
ls $(ros2 pkg prefix turtlebot3_gazebo)/share/turtlebot3_gazebo/models/
echo $TURTLEBOT3_MODEL
mkdir -p ~/ros2_ws/src/lab2_world/launch
nano ~/ros2_ws/src/lab2_world/launch/lab2_world.launch.py
nano ~/ros2_ws/src/lab2_world/CMakeLists.txt
cd ~/ros2_ws
colcon build --packages-select lab2_world
source install/setup.bash
ros2 launch lab2_world lab2_world.launch.py
clear
ros2 launch lab2_world lab2_world.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
echo $ROS_DISTRO
cat /etc/os-release | grep VERSION_ID
dpkg -l | grep turtlebot3 | head -5
gz sim --version 2>/dev/null || echo "gz not found"
ls ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
ls ~/ros2_ws/src/lab2_world/launch/lab2_world.launch.py
cat ~/ros2_ws/src/lab2_world/CMakeLists.txt | grep install
echo $TURTLEBOT3_MODEL
cd ~/ros2_ws
colcon build --packages-select lab2_world
source install/setup.bash
ros2 launch lab2_world lab2_world.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
rviz
rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 run turtlebot3_teleop teleop_keyboard
mkdir -p ~/ros2_ws/src/lab2_world/maps
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/lab2_world/maps/lab2_map --ros-args -p use_sim_time:=true
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/lab2_world/maps/lab2_map --ros-args -p use_sim_time:=true -r __node:=map_saver_node
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/lab2_world/maps/lab2_map -t /map --ros-args -p use_sim_time:=true
ros2 run nav2_map_server map_saver_cli -f ~/ros2_ws/src/lab2_world/maps/lab2_map
cat ~/ros2_ws/src/lab2_world/maps/lab2_map.yaml
clear
cat ~/ros2_ws/src/lab2_world/maps/lab2_map.yaml
ros2 pkg list | grep nav2_bringup
ls $(ros2 pkg prefix nav2_bringup)/share/nav2_bringup/launch/
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python lab2_navigator --dependencies rclpy nav2_simple_commander geometry_msgs
nano ~/ros2_ws/src/lab2_navigator/lab2_navigator/go_to_point.py
nano ~/ros2_ws/src/lab2_navigator/setup.py
cd ~/ros2_ws
colcon build --packages-select lab2_navigator
source install/setup.bash
clear
nano ~/ros2_ws/src/lab2_navigator/launch/navigation.launch.py
mkdir -p ~/ros2_ws/src/lab2_navigator/launch
nano ~/ros2_ws/src/lab2_navigator/launch/navigation.launch.py
nano ~/ros2_ws/src/lab2_navigator/setup.py
cd ~/ros2_ws
colcon build --packages-select lab2_navigator
source install/setup.bash
rviz
rviz2
ros2 launch lab2_world lab2_world.launch.py
ros2 topic list | grep cmd_vel
ros2 node list
clear
mkdir -p ~/ros2_ws/src/lab2_navigator/lab2_navigator
nano ~/ros2_ws/src/lab2_navigator/lab2_navigator/cmd_vel_bridge.py
nano ~/ros2_ws/src/lab2_navigator/setup.py
cd ~/ros2_ws
colcon build --packages-select lab2_navigator
source install/setup.bash
ros2 run lab2_navigator go_to_point
ros2 launch lab2_navigator navigation.launch.py
ros2 run lab2_navigator go_to_point
ros2 launch lab2_world lab2_world.launch.py
ros2 run lab2_navigator cmd_vel_bridge
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=trueros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 launch lab2_world lab2_world.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
rviz
rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 launch lab2_world lab2_world.launch.py
nano ~/ros2_ws/src/lab2_navigator/lab2_navigator/go_to_point.py
cd ~/ros2_ws
colcon build --packages-select lab2_navigator
source install/setup.bash
ros2 run lab2_navigator go_to_point
ros2 run lab2_navigator cmd_vel_bridge
ros2 launch lab2_navigator navigation.launch.py
nano ~/ros2_ws/src/lab2_navigator/lab2_navigator/go_to_point.py
cd ~/ros2_ws
colcon build --packages-select lab2_navigator
source install/setup.bash
cd ~/ros2_ws
colcon build --packages-select lab2_navigator
source install/setup.bash
ros2 run lab2_navigator go_to_point
ros2 launch lab2_navigator navigation.launch.py
ros2 run lab2_navigator cmd_vel_bridge
ros2 launch lab2_world lab2_world.launch.py
ros2 run ulstu_turtlesim teleop_node
ros2 run turtlesim turtlesim_node
ros2 run ulstu_turtlesim teleop_node
ros2 run ulstu_turtlesim trajectory_node
ros2 run lab2_navigator go_to_point
ros2 launch lab2_navigator navigation.launch.py
ros2 launch lab2_world lab2_world.launch.py
ros2 run lab2_navigator cmd_vel_bridge
ros2 run turtlebot3_teleop teleop_keyboard
rviz2
ros2 launch lab2_world lab2_world.launch.py
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
ros2 launch lab2_world lab2_world.launch.py
ros2 run turtlebot3_teleop teleop_keyboard
rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
cat ~/ros2_ws/src/lab2_world/maps/lab2_map.yaml
python3 -c "from PIL import Image; print('OK')"
python3 << 'EOF'
from PIL import Image, ImageDraw

# Параметры карты
resolution = 0.05  # метров на пиксель
width_m = 14.0     # ширина карты в метрах (с запасом)
height_m = 14.0
origin_x = -7.0    # начало координат карты
origin_y = -7.0

w_px = int(width_m / resolution)   # 280
h_px = int(height_m / resolution)  # 280

# Создаём белое изображение (свободное пространство = 254)
img = Image.new('L', (w_px, h_px), 254)
draw = ImageDraw.Draw(img)

def m_to_px(x, y):
    """Конвертация метров в пиксели"""
    px = int((x - origin_x) / resolution)
    py = int((height_m - (y - origin_y)) / resolution)  # ось Y инвертирована
    return px, py

def draw_wall(x1, y1, x2, y2, thickness=0.2):
    """Рисует стену (чёрная линия)"""
    half = thickness / 2.0
    # Горизонтальная стена
    if abs(y1 - y2) < 0.01:
        corners = [
            m_to_px(min(x1,x2), y1 + half),
            m_to_px(max(x1,x2), y1 - half)
        ]
    # Вертикальная стена
    elif abs(x1 - x2) < 0.01:
        corners = [
            m_to_px(x1 - half, max(y1,y2)),
            m_to_px(x1 + half, min(y1,y2))
        ]
    else:
        corners = [m_to_px(x1, y1), m_to_px(x2, y2)]
    draw.rectangle(corners, fill=0)

def draw_obstacle(cx, cy, sx, sy):
    """Рисует препятствие (мебель)"""
    p1 = m_to_px(cx - sx/2, cy + sy/2)
    p2 = m_to_px(cx + sx/2, cy - sy/2)
    draw.rectangle([p1, p2], fill=0)

# === ВНЕШНИЕ СТЕНЫ ===
# Северная (Y=6, от X=-6.2 до X=6.2)
draw_wall(-6.2, 6.0, 6.2, 6.0)
# Южная (Y=-6)
draw_wall(-6.2, -6.0, 6.2, -6.0)
# Западная (X=-6)
draw_wall(-6.0, -6.0, -6.0, 6.0)
# Восточная (X=6)
draw_wall(6.0, -6.0, 6.0, 6.0)

# === ВНУТРЕННИЕ СТЕНЫ ===
# Горизонтальная верхняя Y=1, левая часть (X=-6 до X=-2, проём X=-2..0)
draw_wall(-6.0, 1.0, -2.0, 1.0, 0.15)
# Горизонтальная верхняя Y=1, правая часть (X=2 до X=6, проём X=0..2)
draw_wall(2.0, 1.0, 6.0, 1.0, 0.15)

# Горизонтальная нижняя Y=-1, левая часть
draw_wall(-6.0, -1.0, -2.0, -1.0, 0.15)
# Горизонтальная нижняя Y=-1, правая часть
draw_wall(2.0, -1.0, 6.0, -1.0, 0.15)

# Вертикальная центральная X=0, верхняя (Y=1 до Y=6)
draw_wall(0.0, 1.0, 0.0, 6.0, 0.15)
# Вертикальная центральная X=0, нижняя (Y=-6 до Y=-1)
draw_wall(0.0, -6.0, 0.0, -1.0, 0.15)

# === МЕБЕЛЬ (препятствия) ===
draw_obstacle(3.0, 4.0, 1.5, 0.8)    # Стол (Кухня)
draw_obstacle(2.2, 4.0, 0.4, 0.4)    # Стул 1
draw_obstacle(3.8, 4.0, 0.4, 0.4)    # Стул 2
draw_obstacle(5.5, 3.0, 0.6, 0.6)    # Холодильник
draw_obstacle(-3.0, 4.0, 2.0, 1.4)   # Кровать (Спальня)
draw_obstacle(-4.2, 4.8, 0.5, 0.4)   # Тумбочка
draw_obstacle(-3.0, -3.0, 0.8, 2.0)  # Диван (Гостиная, повёрнут)
draw_obstacle(-4.5, -4.5, 0.8, 0.8)  # Журнальный столик
draw_obstacle(3.0, -4.0, 1.2, 0.6)   # Рабочий стол (Кабинет)
draw_obstacle(5.5, -4.0, 0.4, 1.5)   # Книжный шкаф

# Серая рамка вокруг (неизвестная область = 205)
for x in range(w_px):
    for y in range(5):
        img.putpixel((x, y), 205)
        img.putpixel((x, h_px-1-y), 205)
for y in range(h_px):
    for x in range(5):
        img.putpixel((x, y), 205)
        img.putpixel((w_px-1-x, y), 205)

img.save('/home/dima/ros2_ws/src/lab2_world/maps/lab2_map.pgm')
print('Карта сохранена: lab2_map.pgm')
print(f'Размер: {w_px}x{h_px} пикселей, {width_m}x{height_m} метров')
EOF

cat > ~/ros2_ws/src/lab2_world/maps/lab2_map.yaml << 'EOF'
image: lab2_map.pgm
mode: trinary
resolution: 0.05
origin: [-7.0, -7.0, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
EOF

ls -la ~/ros2_ws/src/lab2_world/maps/
python3 -c "from PIL import Image; img=Image.open('/home/dima/ros2_ws/src/lab2_world/maps/lab2_map.pgm'); print(f'Size: {img.size}')"
ros2 run lab2_navigator go_to_point
ros2 run lab2_navigator cmd_vel_bridge
ros2 launch lab2_navigator navigation.launch.py
ros2 launch lab2_world lab2_world.launch.py
ros2 topic info /cmd_vel
export TURTLEBOT3_MODEL=burger
ros2 launch turtlebot3_gazebo empty_world.launch.py
ros2 topic info /cmd_vel
ros2 topic list
ros2 topic info /cmd_vel --verbose
clear
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python lab3_ellipse --dependencies rclpy geometry_msgs
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_controller.py
nano ~/ros2_ws/src/lab3_ellipse/setup.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 run lab3_ellipse ellipse
ls ~/ros2_ws/src/lab2_world/
ls ~/ros2_ws/src/lab2_world/launch/
ls ~/ros2_ws/src/lab2_world/worlds/
export TURTLEBOT3_MODEL=burger
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py
cat ~/ros2_ws/src/lab2_world/launch/lab2_world.launch.py
clear
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse ellipse
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse ellipse --ros-args -p a:=1.0 -p b:=0.5
cat ~/ros2_ws/src/lab2_world/worlds/lab2_world.sdf
clear
ros2 launch lab2_world lab2_world.launch.py
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-3.0 y_pose:=-4.0
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse ellipse --ros-args -p a:=0.8 -p b:=0.5
ros2 topic echo /cmd_vel --once
ros2 topic echo /odom --once
rviz2
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_controller.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse ellipse --ros-args -p a:=1.5 -p b:=0.7 -p loops:=1
ros2 run lab3_ellipse ellipse --ros-args -p a:=1.5 -p b:=0.7 
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
rviz2
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse ellipse --ros-args -p a:=1.5 -p b:=0.7 -p speed:=0.15
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_controller.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse ellipse --ros-args -p a:=1.5 -p b:=0.7 -p speed:=0.12 -p loops:=1
rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_controller.py
nano ~/ros2_ws/src/lab3_ellipse/package.xml
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
rm ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_controller.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/__init__.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/robot_controller.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
nano ~/ros2_ws/src/lab3_ellipse/setup.py
nano ~/ros2_ws/src/lab3_ellipse/package.xml
сдуфк
clear
ls ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
rviz2
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=1.0 -p b:=0.5
ls ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/
clear
cat ~/ros2_ws/src/lab3_ellipse/setup.py
nano ~/ros2_ws/src/lab3_ellipse/setup.py
clear
rm -rf ~/ros2_ws/build/lab3_ellipse
rm -rf ~/ros2_ws/install/lab3_ellipse
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=1.0 -p b:=0.5
ros2 run rqt_plot rqt_plot /wall_error/data /wall_speed/data
rviz2
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=1.0 -p b:=0.5
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
rviz
rviz2
ros2 run rqt_plot rqt_plot /wall_error/data /wall_speed/data
rviz2
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=1.0 -p b:=0.5 -p speed:=0.30
rviz2
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/robot_controller.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
clear
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/robot_controller.py
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
rqt
sudo apt install ros-jazzy-plotjuggler-ros
ros2 run plotjuggler plotjuggler
ros2 run lab3_ellipse robot --ros-args -p a:=1.0 -p b:=0.5
rviz2
clear
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run plotjuggler plotjuggler
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run lab3_ellipse robot --ros-args -p a:=1.0 -p b:=0.5 -p speed:=0.5
rviz2
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
sudo apt install ros-jazzy-plotjuggler-ros
source /opt/ros/jazzy/setup.bash
ros2 run plotjuggler plotjuggler
ros2 run lab2_navigator go_to_point
ros2 run lab2_navigator cmd_vel_bridge
ros2 launch lab2_navigator navigation.launch.py
ros2 launch lab2_world lab2_world.launch.py
ros2 run lab3_ellipse robot --ros-args -p a:=0.7 -p b:=0.4 -p speed:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
rviz2
source /opt/ros/jazzy/setup.bash
ros2 run plotjuggler plotjuggler
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5
rviz2
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/ellipse_motion.py
grep set_node ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/robot_controller.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5
rviz2
os2 run plotjuggler plotjuggler
ros2 run plotjuggler plotjuggler
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.7
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.30
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.25 -p wall_dist:=0.6
ros2 topic echo /rosout | grep wall
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.22 -p wall_dist:=0.55
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.25 -p wall_dist:=0.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.25 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.25 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.25 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.22 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.20 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.20 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.20 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
source ~/ros2_ws/install/setup.bash
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.22 -p wall_dist:=0.5
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
nano ~/ros2_ws/src/lab3_ellipse/lab3_ellipse/wall_follower.py
cd ~/ros2_ws
colcon build --packages-select lab3_ellipse
source install/setup.bash
export TURTLEBOT3_MODEL=waffle
source ~/ros2_ws/install/setup.bash
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
ros2 run plotjuggler plotjuggler
rviz2
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
rviz2
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
ros2 run plotjuggler plotjuggler
ros2 launch lab2_world lab2_world.launch.py x_pose:=-1.5 y_pose:=-3.5
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
rviz2
ros2 run plotjuggler plotjuggler
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
ros2 launch lab2_world lab2_world.launch.py
ros2 run plotjuggler plotjuggler
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=1.0 -p wall_dist:=0.5
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=1.0 -p wall_dist:=0.5
ros2 run plotjuggler plotjuggler
ros2 launch lab2_world lab2_world.launch.py
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.8 -p wall_dist:=0.5
ros2 run plotjuggler plotjuggler
ros2 run lab3_ellipse robot   --ros-args -p a:=0.6 -p b:=0.35 -p speed:=0.5 -p wall_dist:=0.5
ros2 launch lab2_world lab2_world.launch.py
