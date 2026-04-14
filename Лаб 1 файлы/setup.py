from setuptools import find_packages, setup

package_name = 'ulstu_turtlesim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/lab1.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your_email@ulstu.ru',
    description='Package for TurtleSim laboratory work',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sim_node = ulstu_turtlesim.sim_node:main',
            'teleop_node = ulstu_turtlesim.teleop_node:main',      # Добавлено
            'trajectory_node = ulstu_turtlesim.trajectory_node:main'  # Добавлено
        ],
    },
)