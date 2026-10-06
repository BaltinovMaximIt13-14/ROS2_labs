import rclpy
from rclpy.node import Node
from sensor_msgs.msg import BatteryState

class BatterySensor(Node): #наследование Node у rclpy

	def __init__(self):
		super().__init__('battery_sensor')


		self.publisher = self.create_publisher(
			BatteryState,
			'/battery_state',
			10
		)
		self.battery_percent = 100.0

		self.timer = self.create_timer(
			1.0,
			self.publish_battery
		)
	def publish_battery(self):
		message = BatteryState()

		message.percentage = self.battery_percent

		self.publisher.publish(message)

		self.get_logger().info(
			f'BatteryState: {self.battery_percent:.1f} %'
		)

		self.battery_percent -= 5.0

		if self.battery_percent < 0.0:
			self.battery_percent = 0.0
def main(args=None):
	rclpy.init(args=args)

	node = BatterySensor()

	rclpy.spin(node)

	node.destroy_node()

	rclpy.shutdown()

if __name__ == '__main__':
	main()
