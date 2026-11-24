import sys
import rclpy
from rclpy.node import Node
from alan_interfaces.srv import RectangleArea

class AlanClient(Node):
    def __init__(self):
        super().__init__('alan_client')
        self.cli = self.create_client(RectangleArea, 'rectangle_area')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Servis bekleniyor...')
        self.req = RectangleArea.Request()

    def send_request(self, width, height):
        self.req.width = float(width)
        self.req.height = float(height)
        return self.cli.call_async(self.req)

def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) < 3:
        print("Kullanım: ros2 run alan_py alan_client <width> <height>")
        return

    client = AlanClient()
    future = client.send_request(sys.argv[1], sys.argv[2])
    rclpy.spin_until_future_complete(client, future)
    response = future.result()

    if response.success:
        client.get_logger().info(f'Sonuç: Alan = {response.area} (success: {response.success})')
    else:
        client.get_logger().error(f'Hata: Negatif değer gönderildi! (success: {response.success})')

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
