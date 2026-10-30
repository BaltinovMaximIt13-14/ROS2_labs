
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

from lab2_control_movement_interfaces.srv import SetMode
from lab2_control_movement_interfaces.action import MoveDistance


class RobotController(Node):

    def __init__(self):
        super().__init__('robot_controller')

        self.current_mode = 'STOP'


        self.callback_group = ReentrantCallbackGroup()

        # Сервис переключения режимов
        self.mode_service = self.create_service(
            SetMode,
            '/set_mode',
            self.set_mode_callback,
            callback_group=self.callback_group
        )

        # Action Server для управления движением
        self.action_server = ActionServer(
            self,
            MoveDistance,
            '/move_distance',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=self.callback_group
        )

        self.get_logger().info(
            'Robot controller started. Current mode: STOP'
        )

    # Переключение режима робота
    def set_mode_callback(self, request, response):

        allowed_modes = ['STOP', 'MANUAL', 'AUTONOMOUS']

        if request.mode not in allowed_modes:
            response.success = False
            response.message = (
                f'Invalid mode: {request.mode}. '
                'Use STOP, MANUAL or AUTONOMOUS'
            )

            self.get_logger().warning(response.message)
            return response

        self.current_mode = request.mode

        response.success = True
        response.message = f'Mode changed to {self.current_mode}'

        self.get_logger().info(response.message)

        return response

    # Проверка цели перед началом движения
    def goal_callback(self, goal_request):


        if self.current_mode != 'AUTONOMOUS':
            self.get_logger().warning(
                'Goal rejected: robot is not in AUTONOMOUS mode'
            )
            return GoalResponse.REJECT

        if goal_request.distance <= 0:
            self.get_logger().warning(
                'Goal rejected: distance must be greater than zero'
            )
            return GoalResponse.REJECT

        if goal_request.speed <= 0 or goal_request.speed > 1.0:
            self.get_logger().warning(
                'Goal rejected: speed must be greater than zero '
                'and not exceed 1.0 m/s'
            )
            return GoalResponse.REJECT

        self.get_logger().info(
            f'Goal accepted: distance={goal_request.distance:.2f} m, '
            f'speed={goal_request.speed:.2f} m/s'
        )

        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):

        self.get_logger().info('Cancellation requested')

        return CancelResponse.ACCEPT

    # Имитация движения робота
    def execute_callback(self, goal_handle):

        distance = goal_handle.request.distance
        speed = goal_handle.request.speed

        traveled = 0.0
        previous_time = time.monotonic()

        feedback = MoveDistance.Feedback()
        result = MoveDistance.Result()

        self.get_logger().info('Movement started')

        # Начальный Feedback: 0%
        feedback.traveled_distance = 0.0
        feedback.progress = 0.0
        goal_handle.publish_feedback(feedback)

        while traveled < distance:

            # Проверка отмены действия
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()

                result.success = False
                result.message = 'Movement canceled'

                self.get_logger().warning('Movement canceled')
                return result


            if self.current_mode != 'AUTONOMOUS':
                goal_handle.abort()

                result.success = False
                result.message = (
                    f'Movement stopped: current mode is {self.current_mode}'
                )

                self.get_logger().warning(result.message)
                return result

            # Вычисление прошедшего времени
            current_time = time.monotonic()
            delta_time = current_time - previous_time
            previous_time = current_time

            # Расчёт пройденного расстояния
            traveled = min(
                distance,
                traveled + speed * delta_time
            )

            # Расчёт прогресса в процентах
            progress = traveled / distance * 100.0

            # Отправка Feedback клиенту
            feedback.traveled_distance = traveled
            feedback.progress = float(progress)

            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f'Traveled: {traveled:.2f}/{distance:.2f} m '
                f'({progress:.1f}%)'
            )

        # Успешное завершение движения
        goal_handle.succeed()

        result.success = True
        result.message = 'Movement completed'

        self.get_logger().info('Movement completed')

        return result


def main(args=None):

    rclpy.init(args=args)

    node = RobotController()

    # Многопоточный исполнитель
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(node)

    try:
        executor.spin()

    except KeyboardInterrupt:
        pass

    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
