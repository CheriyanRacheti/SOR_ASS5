import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution


def generate_launch_description():
    world_arg = DeclareLaunchArgument(
        'world', default_value='home.sdf',
        description='Name of the Gazebo world file to load'
    )

    pkg_bme_ros2_navigation = get_package_share_directory('bme_ros2_navigation')
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')

    # Custom models path
    gazebo_models_path = "/home/ubuntu/gazebo_models"

    # Package's own models directory (make sure this folder exists and is installed)
    pkg_models_path = os.path.join(pkg_bme_ros2_navigation, 'models')

    # Safely build GZ_SIM_RESOURCE_PATH without crashing if it isn't already set
    os.environ["GZ_SIM_RESOURCE_PATH"] = os.pathsep.join(filter(None, [
        os.environ.get("GZ_SIM_RESOURCE_PATH", ""),
        gazebo_models_path,
        pkg_models_path,
    ]))

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'),
        ),
        launch_arguments={
            'gz_args': [
                PathJoinSubstitution([
                    pkg_bme_ros2_navigation,
                    'worlds',
                    LaunchConfiguration('world')
                ]),
                TextSubstitution(text=' -r -v -v1')
                # TextSubstitution(text=' -r -v -v1 --render-engine ogre --render-engine-gui-api-backend opengl')
            ],
            'on_exit_shutdown': 'true'
        }.items()
    )

    launchDescriptionObject = LaunchDescription()
    launchDescriptionObject.add_action(world_arg)
    launchDescriptionObject.add_action(gazebo_launch)
    return launchDescriptionObject