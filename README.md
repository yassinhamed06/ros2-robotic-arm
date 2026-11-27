# ROS 2 Robotic Arm

## 1. Project Overview

This project implements a four-joint robotic arm using ROS 2,
Gazebo, RViz2, and Arduino Uno.

The robotic arm can be controlled through a graphical user
interface (GUI). The first two joints are connected to physical
servo motors, while all four joints are simulated.

## 2. Software Requirements

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Fortress
- RViz2
- ROS 2 Control
- Python 3
- Tkinter
- PySerial
- Arduino IDE
- Arduino Servo Library

## 3. Hardware Components

- Arduino Uno
- 2 x SG90 180-degree position servo motors
- 5V 2A external power supply
- Breadboard
- Jumper wires
- USB cable

## 4. System Architecture

The GUI publishes joint trajectory commands to:

/arm_controller/joint_trajectory

The trajectory controller moves the simulated robotic arm.

The serial bridge receives the same commands, converts radians
to servo angles, and sends the angles and movement duration
to Arduino through USB serial communication.

RViz2 displays the simulated robot using joint states.

## 5. Project Structure

    arm_description/
        urdf/
        launch/
        rviz/

    arm_simulation/
        worlds/
        config/
        launch/

    arm_control/
        arm_control/

    arduino/
        servo_control/
            servo_control.ino

## 6. Arduino Wiring

| Connection | Arduino / Power Supply |
|------------|------------------------|
| Servo 1 Signal | D9 |
| Servo 2 Signal | D10 |
| Servo VCC | External 5V |
| Servo GND | External GND |
| Arduino GND | External GND |

The Arduino is powered through USB.
The servos are powered by the external 5V 2A power supply.

Both systems share a common ground.

## 7. Build the Workspace

Place the project files inside ~/ros2_ws/src.

```bash
cd ~/ros2_ws
source /opt/ros/humble/setup.bash
colcon build
source install/setup.bash
```

## 8. Simulation Only Mode

```bash
ros2 launch arm_simulation full_system.launch.py
```

This launches Gazebo, RViz2, the ROS 2 controllers,
and the control GUI.

## 9. Full System Mode

Upload servo_control.ino to Arduino Uno using Arduino IDE.

Connect Arduino through USB and connect the external
servo power supply.

```bash
ros2 launch arm_simulation full_system.launch.py hardware:=true
```

This also launches the serial bridge and enables physical
servo control.

## 10. Joint Limits

| Joint | Minimum (rad) | Maximum (rad) |
|-------|---------------|---------------|
| Joint 1 | -0.78 | 0.78 |
| Joint 2 | -0.78 | 0.78 |
| Joint 3 | -1.57 | 1.57 |
| Joint 4 | -1.57 | 1.57 |

The physical servo commands are limited to 45-135 degrees.

## 11. Speed Control

The GUI allows the user to select a movement duration
between 1 and 10 seconds.

Arduino gradually changes the commanded servo positions
during the selected movement duration.

## 12. Automatic Reconnection

The serial bridge automatically detects the Arduino
and attempts to reconnect if the USB cable is disconnected.

## 13. Testing Results

- URDF visualization: Passed
- Gazebo simulation: Passed
- ROS 2 controllers: Passed
- GUI control: Passed
- Arduino communication: Passed
- Automatic reconnection: Passed
- Individual servo movement: Passed
- Combined servo movement: Passed
- Joint limits: Passed
- Speed control: Passed
- Visual synchronization: Passed
- Unified launch file: Passed

## 14. Current Limitations

- Only the first two joints have physical servo motors.
- Physical servo position feedback is not returned to ROS 2.
- Synchronization was verified visually.
- Exact physical angle accuracy has not been measured.

## 15. Conclusion

The project demonstrates the integration of ROS 2 simulation,
robot visualization, graphical control, and physical servo
control through Arduino serial communication.
