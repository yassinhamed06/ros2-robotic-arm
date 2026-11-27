import math
import time
import glob
import os
import serial
import rclpy

from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory


class SerialBridge(Node):

    def __init__(self):
        super().__init__('serial_bridge')

        self.arduino = None
        self.ready = False
        self.ready_at = 0

        self.declare_parameter('port', 'auto')

        self.subscription = self.create_subscription(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            self.move_servos,
            1
        )

        self.timer = self.create_timer(
            1.0, self.connect_arduino
        )

        self.get_logger().info('Waiting for Arduino')

    def connect_arduino(self):

        if self.arduino is not None:

            if not os.path.exists(self.arduino.port):
                self.disconnect()
                return

            if not self.ready and time.monotonic() >= self.ready_at:
                try:
                    self.arduino.reset_input_buffer()
                    self.ready = True
                    self.get_logger().info('Arduino connected')

                except (serial.SerialException, OSError):
                    self.disconnect()

            return

        port = self.get_parameter('port').value

        if port == 'auto':
            ports = glob.glob('/dev/serial/by-id/*Arduino*')

            if len(ports) != 1:
                return

            port = ports[0]

        try:
            self.arduino = serial.Serial(
                port,
                9600,
                timeout=1,
                write_timeout=1
            )

            self.ready = False
            self.ready_at = time.monotonic() + 3

        except (serial.SerialException, OSError):
            self.arduino = None

    def disconnect(self):

        if self.arduino is not None:
            try:
                self.arduino.close()
            except (serial.SerialException, OSError):
                pass

        self.arduino = None
        self.ready = False

        self.get_logger().warning(
            'Arduino disconnected. Reconnecting...'
        )

    def move_servos(self, msg):

        if self.arduino is None or not self.ready:
            self.get_logger().warning('Arduino not ready')
            return

        if not msg.points:
            return

        try:
            positions = msg.points[-1].positions

            joint1 = positions[msg.joint_names.index('joint1')]
            joint2 = positions[msg.joint_names.index('joint2')]

            if not math.isfinite(joint1) or not math.isfinite(joint2):
                return

            angle1 = round(math.degrees(joint1) + 90)
            angle2 = round(math.degrees(joint2) + 90)

            angle1 = max(45, min(135, angle1))
            angle2 = max(45, min(135, angle2))

            duration = msg.points[-1].time_from_start
            duration_ms = duration.sec * 1000 + duration.nanosec // 1000000
            duration_ms = max(1000, min(10000, duration_ms))

            command = f'{angle1},{angle2},{duration_ms}\n'

            self.arduino.write(command.encode())

            response = self.arduino.readline().decode(
                errors='replace'
            ).strip()

            if response == 'OK':
                self.get_logger().info(
                    f'Sent: {angle1}, {angle2}, {duration_ms} ms | Arduino: OK'
                )

            elif not response:
                self.disconnect()

            else:
                self.get_logger().warning(response)

        except (serial.SerialException, OSError):
            self.disconnect()

        except (ValueError, IndexError):
            self.get_logger().warning('Invalid trajectory')


def main(args=None):

    rclpy.init(args=args)
    node = SerialBridge()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        if node.arduino is not None:
            node.arduino.close()

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
