import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class CPUSensor(Node): #наследование Node у rclpy

	def __init__(self):
		super().__init__('cpu_monitor')


		self.publisher = self.create_publisher(
			Float32,
			'/cpu_load',
			10
		)
		self.cpu_load = 24.5

		self.timer = self.create_timer(
			1.0,
			self.publish_cpu_load
		)
	def publish_cpu_load(self):
		message = Float32()

		message.data = self.cpu_load

		self.publisher.publish(message)

		self.get_logger().info(
			f'CPU load: {self.cpu_load:.1f} %'
		)

		self.cpu_load += 5.0

		if self.cpu_load > 90.0:
			self.cpu_load = 24.5
def main(args=None):
	rclpy.init(args=args)

	node = CPUSensor()

	rclpy.spin(node)

	node.destroy_node()

	rclpy.shutdown()

if __name__ == '__main__':
	main()

