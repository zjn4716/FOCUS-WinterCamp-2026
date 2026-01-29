#!/usr/bin/env python3
"""
unitree_go1_camera.py - 用于Unitree Go1相机的图像处理器
"""

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge, CvBridgeError

class UnitreeGo1Camera:
    def __init__(self):
        rospy.init_node('unitree_go1_camera', anonymous=True)
        
        # 获取参数
        self.image_topic = rospy.get_param('~image_topic', '/camera_face/color/image_raw')
        self.display = True #rospy.get_param('~display', True)
        
        # 初始化CV Bridge
        self.bridge = CvBridge()
        
        # 订阅图像话题
        rospy.loginfo(f"订阅相机话题: {self.image_topic}")
        self.image_sub = rospy.Subscriber(
            self.image_topic,
            Image,
            self.image_callback,
            queue_size=1,
            buff_size=2**24  # 大缓冲区，防止丢帧
        )
        
        # 可选：订阅相机信息
        self.camera_info_sub = rospy.Subscriber(
            self.image_topic.replace('image_raw', 'camera_info'),
            CameraInfo,
            self.info_callback
        )
        
        # 相机内参
        self.camera_matrix = None
        self.distortion_coeffs = None
        
        # 创建窗口
        
        rospy.loginfo("cv2win")
        cv2.namedWindow('Unitree Go1 Camera', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Unitree Go1 Camera', 640, 480)
        
        rospy.loginfo("Unitree Go1 相机节点已启动")
    
    def info_callback(self, msg):
        """相机信息回调"""
        if self.camera_matrix is None:
            self.camera_matrix = np.array(msg.K).reshape(3, 3)
            self.distortion_coeffs = np.array(msg.D)
            rospy.loginfo(f"相机内参已接收:\n{self.camera_matrix}")
    
    def image_callback(self, msg):
        """图像处理回调"""
        try:
            # 转换图像
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # 处理图像
            processed = self.process_image(cv_image)
            
            # 显示图像
            #if self.display:
            cv2.imshow('Unitree Go1 Camera', processed)
            cv2.waitKey(1)
            rospy.loginfo(f"相机image已接收:\n")    
            # 可选：保存图像示例
            if rospy.get_param('~save_image', False):
                timestamp = rospy.get_time()
                cv2.imwrite(f'/tmp/go1_camera_{timestamp:.3f}.jpg', cv_image)
                
        except CvBridgeError as e:
            rospy.logerr(f"CV桥接错误: {e}")
        except Exception as e:
            rospy.logerr(f"图像处理错误: {e}")
    
    def process_image(self, image):
        """图像处理函数"""
        if image is None:
            return None
        
        # 复制图像以避免修改原始数据
        result = image.copy()
        
        # 获取图像尺寸
        height, width = image.shape[:2]
        
        # 添加文本信息
        cv2.putText(
            result,
            f"Unitree Go1 Camera - {width}x{height}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
        
        # 添加帧率显示（简化版）
        current_time = rospy.Time.now()
        if hasattr(self, 'last_time'):
            dt = (current_time - self.last_time).to_sec()
            fps = 1.0 / dt if dt > 0 else 0
            cv2.putText(
                result,
                f"FPS: {fps:.1f}",
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
        self.last_time = current_time
        
        # 可选：添加网格线
        if rospy.get_param('~show_grid', False):
            # 水平线
            for i in range(1, 3):
                y = int(height * i / 3)
                cv2.line(result, (0, y), (width, y), (0, 255, 255), 1)
            
            # 垂直线
            for i in range(1, 3):
                x = int(width * i / 3)
                cv2.line(result, (x, 0), (x, height), (0, 255, 255), 1)
        
        # 可选：边缘检测
        if rospy.get_param('~edge_detection', False):
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            # 叠加边缘到原图
            result = cv2.addWeighted(result, 0.8, edges_colored, 0.2, 0)
        
        return result
    
    def run(self):
        """主循环"""
        rate = rospy.Rate(30)  # 30Hz
        
        while not rospy.is_shutdown():
            try:
                rate.sleep()
            except KeyboardInterrupt:
                break
        
        if self.display:
            cv2.destroyAllWindows()

def main():
    try:
        camera = UnitreeGo1Camera()
        camera.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
