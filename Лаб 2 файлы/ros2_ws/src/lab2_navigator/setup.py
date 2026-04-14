import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'lab2_navigator'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/lab2_navigator']),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dima',
    maintainer_email='dima@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'go_to_point = lab2_navigator.go_to_point:main',
            'cmd_vel_bridge = lab2_navigator.cmd_vel_bridge:main',
        ],
    },
)
