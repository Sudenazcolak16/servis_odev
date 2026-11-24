import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea

class AlanServer(Node):
    def __init__(self):
        super().__init__('alan_server')
        self.srv = self.create_service(RectangleArea, 'rectangle_area', self.calculate_area_callback)
        self.get_logger().info('RectangleArea servisi hazır...')

    def calculate_area_callback(self, request, response):
        if request.width < 0.0 or request.height < 0.0:
            response.area = 0.0
            response.success = False
            self.get_logger().warn(f'Geçersiz (negatif) değer girildi: width={request.width}, height={request.height}')
        else:
            response.area = request.width * request.height
            response.success = True
            self.get_logger().info(f'İstek: width={request.width}, height={request.height} -> Alan: {response.area}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AlanServer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
