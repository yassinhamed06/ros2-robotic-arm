import tkinter as tk
import rclpy

from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


class ControlGUI(Node):

    def __init__(self):
        super().__init__('control_gui')

        self.publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

        self.window = tk.Tk()
        self.window.title('Robotic Arm Control')
        self.window.geometry('450x520')

        self.sliders = []

        for i in range(4):

            slider = tk.Scale(
                self.window,
                from_=-0.78 if i < 2 else -1.57,
                to=0.78 if i < 2 else 1.57,
                resolution=0.01,
                orient=tk.HORIZONTAL,
                length=350,
                label=f'Joint {i + 1} (rad)'
            )

            slider.set(0)
            slider.pack(pady=5)

            self.sliders.append(slider)

        self.duration = tk.Scale(
            self.window,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            length=350,
            label='Movement Duration (seconds)'
        )

        self.duration.set(3)
        self.duration.pack(pady=5)

        tk.Button(
            self.window,
            text='Send Movement',
            command=self.send_trajectory,
            width=25
        ).pack(pady=10)

        tk.Button(
            self.window,
            text='Reset',
            command=self.reset,
            width=25
        ).pack(pady=5)

        self.status = tk.Label(
            self.window,
            text='Ready'
        )

        self.status.pack(pady=5)

    def send_trajectory(self):

        if self.publisher.get_subscription_count() == 0:
            self.status.config(text='Controller not connected')
            return

        msg = JointTrajectory()

        msg.joint_names = [
            'joint1', 'joint2', 'joint3', 'joint4'
        ]

        point = JointTrajectoryPoint()

        point.positions = [
            float(slider.get())
            for slider in self.sliders
        ]

        point.time_from_start.sec = int(self.duration.get())

        msg.points = [point]

        self.publisher.publish(msg)

        self.status.config(text='Movement command sent')

    def reset(self):

        for slider in self.sliders:
            slider.set(0)

        self.send_trajectory()


def main(args=None):

    rclpy.init(args=args)

    node = ControlGUI()

    try:
        node.window.mainloop()
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
