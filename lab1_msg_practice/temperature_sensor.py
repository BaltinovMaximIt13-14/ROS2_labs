import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Temperature

class TemperatureSensor(Node): #наследование Node у rclpy

	def __init__(self):
		super().__init__('temperature_sensor')


		self.publisher = self.create_publisher(
			Temperature,
			'/temperature',
			10
		)
		self.temperature = 23.5

		self.timer = self.create_timer(
			1.0,
			self.publish_temperature
		)
	def publish_temperature(self):
		message = Temperature()

		message.temperature = self.temperature

		self.publisher.publish(message)

		self.get_logger().info(
			f'Temperature: {self.temperature:.1f} °C'
		)

		self.temperature += 0.2

		if self.temperature > 30.0:
			self.temperature = 23.5
def main(args=None):
	rclpy.init(args=args)

	node = TemperatureSensor()

	rclpy.spin(node)

	node.destroy_node()

	rclpy.shutdown()

if __name__ == '__main__':
	main()

