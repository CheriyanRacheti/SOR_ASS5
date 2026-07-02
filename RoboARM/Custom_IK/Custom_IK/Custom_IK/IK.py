import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class ManualIKPublisher(Node):
    def __init__(self):
        super().__init__('manual_ik_publisher')

        self.publisher_ = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',  # <-- confirm this matches your controller topic
            10
        )

        self.timer = self.create_timer(1.0, self.publish_trajectory)
        self.published = False

    def publish_trajectory(self):
        if self.published:
            return

        msg = JointTrajectory()

        # Must exactly match joint names from your URDF / controller yaml
        msg.joint_names = [
            'base_joint',
            'shoulder_joint',
            'elbow_joint',
            'wrist_joint'
        ]

        point = JointTrajectoryPoint()

        theta1 = 0.7854    # base
        theta2 = 0.3927    # shoulder
        theta3 = -0.5236   # elbow
        theta4 = -(theta2 + theta3)  # wrist,parallel to table

        point.positions = [theta1, theta2, theta3, theta4]
        point.velocities = [0.0, 0.0, 0.0, 0.0]
        point.time_from_start = Duration(sec=3, nanosec=0)

        msg.points = [point]

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Published trajectory -> base={theta1:.3f}, shoulder={theta2:.3f}, '
            f'elbow={theta3:.3f}, wrist={theta4:.3f}'
        )
        self.published = True


def main():
    rclpy.init()
    node = ManualIKPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()