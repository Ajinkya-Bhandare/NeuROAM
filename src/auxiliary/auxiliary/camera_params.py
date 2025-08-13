import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image  # Change this to match your message type
import time
from cv_bridge import CvBridge
import cv2
import matplotlib.pyplot as plt
import numpy as np
CAMERA_FREQ = 20
class CameraparamsNode(Node):
    def __init__(self):
        super().__init__('cameraparams_node')

        self.cam0_input_topic = '/cam_sync/cam0/image_raw'
        self.cam1_input_topic = '/cam_sync/cam1/image_raw'
        
        self.cam0_subscriber = self.create_subscription(
            Image,
            self.cam0_input_topic,
            self.callback_cam0,
            10
        )

        # self.cam1_subscriber = self.create_subscription(
        #     Image,
        #     self.cam1_input_topic,
        #     self.callback_cam1,
        #     10
        # )

        self.bridge = CvBridge()
        # Setup matplotlib interactive mode
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlim(0, 256)
        self.ax.set_ylim(0, 255)
        self.ax.set_title("Grayscale Histogram")
        self.ax.set_xlabel("Pixel Intensity")
        self.ax.set_ylabel("Frequency")
        self.hist_line, = self.ax.plot([], [], lw=2)  # Empty plot to start with

    def callback_cam0(self, msg):
        
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        fname = f'{msg.header.stamp.sec}{msg.header.stamp.nanosec}'

        # Display the image
        cv2.imshow('Cam0 Image', cv_image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite(f'{fname}.png',cv_image)

        # Convert ROS Image message to OpenCV image (cv2)
        cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        self.ax.clear()

        # Plot Histogram for the image
        color = ('b','g','r')
        for i,col in enumerate(color):
            histr = cv2.calcHist([cv_image],[i],None,[256],[0,256])
            self.ax.plot(histr,color = col)
        
        # Set the plot parameters after clearing
        self.ax.set_title("Color Histogram")
        self.ax.set_xlabel("Pixel Intensity")
        self.ax.set_ylabel("Frequency")
        self.ax.set_xlim([0, 256])

        # Update the histogram plot
        self.fig.canvas.draw()  # Redraw the figure
        self.fig.canvas.flush_events()  # Update the plot in real-time
    
        if key == ord('s'):
            self.fig.savefig(f"{fname}_histogram.png")  # Change filename/path as needed

    # def callback_cam1(self, msg):
    #     cv_image = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

    #     # Display the image
    #     cv2.imshow('ROS2 Image', cv_image)
    #     cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = CameraparamsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()