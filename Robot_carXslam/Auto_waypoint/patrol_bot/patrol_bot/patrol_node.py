import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from geometry_msgs.msg import PoseStamped


def create_pose(navigator, x, y, qw, qx, qy, qz):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0
    pose.pose.orientation.w = qw
    pose.pose.orientation.x = qx
    pose.pose.orientation.y = qy
    pose.pose.orientation.z = qz
    return pose


def main():
    rclpy.init()
    navigator = BasicNavigator()

    navigator.waitUntilNav2Active()

    # ---- Hardcoded waypoints: (x, y, qw, qx, qy, qz) ----
    waypoints = [
        (0.89327335357666016, 1.1334505081176758,
         0.92752015501641683, 0.0, 0.0, 0.37377314247859234),

        (0.81780672073364258, -0.94519948959350586,
         0.90411574593179533, 0.0, 0.0, -0.42728762907226014),

        (5.00136, 1.86852,
         0.0072688065351738836, 0.0, 0.0, 0.99997358187681851),
    ]

    for i, (x, y, qw, qx, qy, qz) in enumerate(waypoints, start=1):
        goal_pose = create_pose(navigator, x, y, qw, qx, qy, qz)
        print(f'[Patrol] Dispatching to Waypoint {i}: x={x:.3f}, y={y:.3f}')
        navigator.goToPose(goal_pose)

        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            if feedback:
                print(f'[Patrol] Distance remaining: {feedback.distance_remaining:.2f} m')

        result = navigator.getResult()
        if result == TaskResult.SUCCEEDED:
            print(f'[Patrol] Waypoint {i} REACHED successfully.')
        elif result == TaskResult.CANCELED:
            print(f'[Patrol] Waypoint {i} was CANCELED.')
        elif result == TaskResult.FAILED:
            print(f'[Patrol] Waypoint {i} FAILED.')

    print('[Patrol] Patrol sequence complete.')
    navigator.lifecycleShutdown()
    rclpy.shutdown()


if __name__ == '__main__':
    main()