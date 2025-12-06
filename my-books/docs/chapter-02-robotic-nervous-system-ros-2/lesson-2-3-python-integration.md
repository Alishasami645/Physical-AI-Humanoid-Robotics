# Lesson 2.3: Python Integration

Python is commonly used to write ROS 2 nodes due to its simplicity and rich libraries.

**Key Concepts:**
- **rclpy library:** ROS 2 Python client library
- **Writing nodes:** Publisher, Subscriber, Service, Action in Python
- **Integration:** Easy testing, prototyping, and AI/ML integration
- **Execution:** Nodes can be launched via `ros2 launch` or scripts

**Example Node:**
- Camera node reads images → publishes to `/camera/image` topic
- Processing node subscribes → performs detection → publishes results
- Actuator node executes commands based on results

**Code Snippet:**
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class Talker(Node):
    def __init__(self):
        super().__init__('talker')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(1.0, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = "Hello from ROS 2 Python Node"
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Talker()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
