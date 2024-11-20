import math

import rclpy
from geometry_msgs.msg import Twist
from .keyboard_gui import KeyboardGui
from rclpy.node import Node


class TeleopManager(Node):
    PUB_RATE = 10.0

    def __init__(self, gui: KeyboardGui):
        super().__init__('teleop_manager')
        self.gui = gui
        self.publisher = self.create_publisher(Twist, 'teleop_cmd_vel', 1)
        timer_period = 1 / TeleopManager.PUB_RATE
        self.timer = self.create_timer(timer_period, self.pub_callback)
        self.current_linear_x = 0.0
        self.target_linear_x = 0.0
        self.current_angular_z = 0.0
        self.target_angular_z = 0.0

    def pub_callback(self):
        new_linear_x = self.gui.linear_velocity
        new_angular_z = self.gui.angular_velocity

        if new_linear_x != self.target_linear_x:
            self.target_linear_x = new_linear_x

        if new_angular_z != self.target_angular_z:
            self.target_angular_z = new_angular_z

        msg = Twist()
        msg.linear.x = float(self.target_linear_x)

        msg.angular.z = float(math.radians(self.target_angular_z))
        self.get_logger().info("linear.x = %.3f, angular.z = %.3f" % (msg.linear.x, msg.angular.z))
        self.publisher.publish(msg)

def main(args=None):
    gui = KeyboardGui()
    rclpy.init(args=args)
    manager = TeleopManager(gui)
    try:
        rclpy.spin(manager)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()