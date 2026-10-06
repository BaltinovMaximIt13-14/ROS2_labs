import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature, Range, BatteryState
from std_msgs.msg import Float32

class SensorLogger(Node):

    def __init__(self):
        super().__init__('sensor_logger')

        self.temperature_subscription = self.create_subscription(
            Temperature,
            '/temperature',
            self.temperature_callback,
            10
        )

        self.distance_subscription = self.create_subscription(
            Range,
            '/distance',
            self.distance_callback,
            10
        )

        self.battery_subscription = self.create_subscription(
            BatteryState,
            '/battery_state',
            self.battery_callback,
            10
        )

        self.cpu_subscription = self.create_subscription(
            Float32,
            '/cpu_load',
            self.cpu_callback,
            10
        )

    def temperature_callback(self, message):
        self.get_logger().info(
            f'Temperature: {message.temperature:.1f} °C'
        )

    def distance_callback(self, message):
        self.get_logger().info(
            f'Distance: {message.range:.1f} m'
        )

    def battery_callback(self, message):
        self.get_logger().info(
            f'Battery level: {message.percentage:.1f} %'
        )

    def cpu_callback(self, message):
        self.get_logger().info(
            f'CPU load: {message.data:.1f} %'
        )
def main(args=None):
	rclpy.init(args=args)

	node = SensorLogger()

	rclpy.spin(node)

	node.destroy_node()

	rclpy.shutdown()

if __name__ == '__main__':
	main()

