import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

class DistanceSensor(Node): #наследование Node у rclpy

	def __init__(self):
		super().__init__('distance_sensor')


		self.publisher = self.create_publisher(
			Range,
			'/distance',
			10
		)
		self.distance = 10.2

		self.timer = self.create_timer(
			1.0,
			self.publish_distance
		)
	def publish_distance(self):
		message = Range()
		
		message.radiation_type = Range.ULTRASOUND
		message.field_of_view = 0.5
		message.min_range = 0.2
		message.max_range = 15.0
		message.range = self.distance

		self.publisher.publish(message)

		self.get_logger().info(
			f'Distance: {self.distance:.1f} m'
		)

		self.distance -= 0.2

		if self.distance < 0.5:
			self.distance = 10.2
def main(args=None):
	rclpy.init(args=args)

	node = DistanceSensor()

	rclpy.spin(node)

	node.destroy_node()

	rclpy.shutdown()

if __name__ == '__main__':
	main()
