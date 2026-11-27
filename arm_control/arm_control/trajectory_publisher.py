import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class TrajectoryPublisher(Node):

    def __init__(self):
        super().__init__('trajectory_publisher')

        self.publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

        self.timer = self.create_timer(
            1.0, self.send_trajectory
        )

    def send_trajectory(self):

        if self.publisher.get_subscription_count() == 0:
            return

        msg = JointTrajectory()

        msg.joint_names = [
            'joint1', 'joint2', 'joint3', 'joint4'
        ]

        point = JointTrajectoryPoint()

        point.positions = [0.0, 0.5, -0.3, 0.0]

        point.time_from_start.sec = 3

        msg.points = [point]

        self.publisher.publish(msg)

        self.get_logger().info('Trajectory sent successfully')

        self.timer.cancel()


def main(args=None):

    rclpy.init(args=args)

    node = TrajectoryPublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
