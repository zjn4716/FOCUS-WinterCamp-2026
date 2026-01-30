#!/usr/bin/env python3
"""
red_box_tracker.py - 检测和追踪红色方块的视觉伺服控制系统
订阅：/trunk_camera/image_raw (或其他相机话题)
控制：/cmd_vel 或 /go1_controller/cmd_vel
"""

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge, CvBridgeError

class RedBoxTracker:
    def __init__(self):
        rospy.init_node('red_box_tracker', anonymous=True)
        
        # 初始化参数
        self.bridge = CvBridge()
        self.cv_image = None
        self.image_received = False
        
        # 红色HSV阈值（需要根据Gazebo环境调整）
        # 红色有两个范围，因为它在HSV色轮的两端
        self.lower_red1 = np.array([0, 100, 100])    # 低红色范围
        self.upper_red1 = np.array([10, 255, 255])
        self.lower_red2 = np.array([160, 100, 100])  # 高红色范围
        self.upper_red2 = np.array([180, 255, 255])
        
        # 控制参数
        # 转向控制 (Yaw)
        self.kp_yaw = rospy.get_param('~kp_yaw', 0.005)  # 比例系数
        self.yaw_error_threshold = rospy.get_param('~yaw_error_threshold', 20)  # 像素误差阈值
        
        # 距离控制 (Forward)
        self.target_area = rospy.get_param('~target_area',20000)  # 目标像素面积
        self.area_tolerance = rospy.get_param('~area_tolerance', 1000)  # 面积容差
        self.min_area = rospy.get_param('~min_area', 500)  # 最小有效面积
        self.max_area = rospy.get_param('~max_area', 30000)  # 最大有效面积
        
        # 速度限制
        self.max_linear_speed = rospy.get_param('~max_linear_speed', 0.5)  # m/s
        self.max_angular_speed = rospy.get_param('~max_angular_speed', 0.5)  # rad/s
        self.min_linear_speed = rospy.get_param('~min_linear_speed', 0.1)  # m/s
        
        # 图像中心坐标（在process_image中计算）
        self.image_center_x = None
        self.image_center_y = None
        
        # 订阅相机话题
        self.image_topic = rospy.get_param('~image_topic', '/camera_face/color/image_raw')
        self.image_sub = rospy.Subscriber(
            self.image_topic,
            Image,
            self.image_callback,
            queue_size=1
        )
        
        # 发布控制命令
        self.cmd_vel_topic = rospy.get_param('~cmd_vel_topic', '/cmd_vel')
        self.cmd_vel_pub = rospy.Publisher(
            self.cmd_vel_topic,
            Twist,
            queue_size=10
        )
        
        # 可选：发布处理后的图像用于调试
        self.debug_image_pub = rospy.Publisher(
            '/red_box_debug/image_raw',
            Image,
            queue_size=10
        )
        
        # 初始化控制命令
        self.cmd_vel = Twist()
        
        # 状态变量
        self.red_box_detected = False
        self.centroid_x = 0
        self.centroid_y = 0
        self.area = 0
        self.yaw_error = 0
        self.area_error = 0
        
        # 创建显示窗口
        self.display = rospy.get_param('~display', True)
        #if self.display:
        cv2.namedWindow('Red Box Tracker', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Red Box Tracker', 800, 600)
        
        rospy.loginfo(f"Red Box Tracker 初始化完成")
        rospy.loginfo(f"订阅图像: {self.image_topic}")
        rospy.loginfo(f"发布控制: {self.cmd_vel_topic}")
        rospy.loginfo(f"目标面积: {self.target_area} 像素")
    
    def image_callback(self, msg):
        """图像回调函数"""
        try:
            # 转换为OpenCV格式
            self.cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.image_received = True
            # 处理图像
            self.cv_image = cv2.flip(self.cv_image, -1)  # -1表示水平和垂直都翻转

            #processed = self.process_image2(self.cv_image)
            
            # 显示图像
            #if self.display:
            #cv2.imshow('Unitree Go1 Camera', processed)
            #cv2.waitKey(1)
            # 处理图像并计算控制命令
            self.process_image()
            
        except CvBridgeError as e:
            rospy.logerr(f"CV桥接错误: {e}")
    def process_image2(self, image):
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
    def process_image(self):
        """处理图像：检测红色方块并计算控制命令"""
        if self.cv_image is None:
            return
        
        # 获取图像尺寸
        height, width = self.cv_image.shape[:2]
        self.image_center_x = width // 2
        self.image_center_y = height // 2
        
        # 步骤1: 颜色分割 - 转换到HSV空间
        hsv_image = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2HSV)
        
        # 创建红色掩码（两个范围）
        mask1 = cv2.inRange(hsv_image, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv_image, self.lower_red2, self.upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        # 形态学操作：去除噪声并填充空洞
        kernel = np.ones((5, 5), np.uint8)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)
        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        
        # 步骤2: 特征提取 - 寻找轮廓
        contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 重置状态
        self.red_box_detected = False
        self.centroid_x = self.image_center_x
        self.centroid_y = self.image_center_y
        self.area = 0
        
        if contours:
            # 找到最大的轮廓（假设是红色方块）
            largest_contour = max(contours, key=cv2.contourArea)
            
            # 计算轮廓面积
            self.area = cv2.contourArea(largest_contour)
            
            if self.min_area < self.area < self.max_area:
                self.red_box_detected = True
                
                # 计算质心
                M = cv2.moments(largest_contour)
                if M["m00"] > 0:
                    self.centroid_x = int(M["m10"] / M["m00"])
                    self.centroid_y = int(M["m01"] / M["m00"])
                
                # 计算外接矩形（用于可视化）
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # 步骤3: 闭环控制计算
                # 3.1 转向控制：计算质心与图像中心的水平误差
                self.yaw_error = self.centroid_x - self.image_center_x
                
                # 3.2 距离控制：计算面积误差
                self.area_error = self.target_area - self.area
                
                # 应用控制逻辑
                self.compute_control()
                
                # 创建调试图像
                debug_image = self.create_debug_image(red_mask, contours, (x, y, w, h))
                
                # 发布调试图像
                try:
                    debug_msg = self.bridge.cv2_to_imgmsg(debug_image, "bgr8")
                    self.debug_image_pub.publish(debug_msg)
                except CvBridgeError as e:
                    rospy.logwarn(f"无法发布调试图像: {e}")
                
                # 显示图像
                if self.display:
                    cv2.imshow('Red Box Tracker', debug_image)
                    cv2.waitKey(1)
            else:
                # 面积无效，停止机器人
                rospy.logwarn(f"检测到红色区域，但面积 {self.area:.0f} 超出有效范围")
                self.stop_robot()
                self.create_no_box_debug_image()
        else:
            # 没有检测到红色，停止机器人
            rospy.logwarn("未检测到红色方块")
            self.stop_robot()
            self.create_no_box_debug_image()
        
        # 发布控制命令
        self.cmd_vel_pub.publish(self.cmd_vel)
    
    def compute_control(self):
        """计算控制命令"""
        # 初始化控制命令
        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        
        if not self.red_box_detected:
            return
        
        # 转向控制 (Yaw)
        # 使用P控制器：角速度 = Kp * 误差
        if abs(self.yaw_error) > self.yaw_error_threshold:
            angular_speed = -self.kp_yaw * self.yaw_error  # 负号因为坐标系转换
            # 限制角速度
            self.cmd_vel.angular.x = np.clip(
                angular_speed,
                -self.max_angular_speed,
                self.max_angular_speed
            )
        else:
            # 误差在阈值内，不转向
            self.cmd_vel.angular.x = 0.0
        
        # 距离控制 (Forward)
        # 如果面积太小（方块太远），前进
        # 如果面积达到目标，停止
        if self.area < (self.target_area - self.area_tolerance):
            # 太远，前进
            # 速度与面积误差成比例，但限制最大速度
            linear_speed = 0.01 * abs(self.area_error)  # 比例系数
            self.cmd_vel.linear.y = np.clip(
                linear_speed,
                self.min_linear_speed,
                self.max_linear_speed
            )
        elif self.area > (self.target_area + self.area_tolerance):
            # 太近，后退
            self.cmd_vel.linear.y = -self.min_linear_speed
        else:
            # 在目标范围内，停止前进
            self.cmd_vel.linear.y = 0.0
        
        # 记录调试信息
        rospy.loginfo_throttle(1.0,
            f"检测到红色方块 | "
            f"质心: ({self.centroid_x}, {self.centroid_y}) | "
            f"面积: {self.area:.0f} | "
            f"转向误差: {self.yaw_error:.0f} px | "
            f"线性速度: {self.cmd_vel.linear.x:.2f} m/s | "
            f"角速度: {self.cmd_vel.angular.z:.2f} rad/s"
        )
    
    def stop_robot(self):
        """停止机器人"""
        self.cmd_vel.linear.x = 0.0
        self.cmd_vel.angular.z = 0.0
        self.red_box_detected = False
    
    def create_debug_image(self, red_mask, contours, bbox):
        """创建调试图像"""
        # 创建显示图像
        debug_image = self.cv_image.copy()
        
        # 在原始图像上绘制红色掩码（半透明）
        red_overlay = np.zeros_like(debug_image)
        red_overlay[red_mask > 0] = (0, 0, 255)  # 红色
        debug_image = cv2.addWeighted(debug_image, 0.7, red_overlay, 0.3, 0)
        
        # 绘制检测到的最大轮廓
        largest_contour = max(contours, key=cv2.contourArea)
        cv2.drawContours(debug_image, [largest_contour], -1, (0, 255, 0), 2)
        
        # 绘制边界框
        x, y, w, h = bbox
        cv2.rectangle(debug_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # 绘制质心
        cv2.circle(debug_image, (self.centroid_x, self.centroid_y), 5, (0, 255, 255), -1)
        
        # 绘制图像中心
        cv2.circle(debug_image, (self.image_center_x, self.image_center_y), 5, (255, 255, 0), -1)
        
        # 绘制质心到中心的连线
        cv2.line(debug_image, 
                (self.image_center_x, self.image_center_y),
                (self.centroid_x, self.centroid_y),
                (255, 0, 255), 2)
        
        # 添加文本信息
        cv2.putText(debug_image, f"Centroid: ({self.centroid_x}, {self.centroid_y})", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(debug_image, f"Area: {self.area:.0f} / Target: {self.target_area}", 
                   (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(debug_image, f"Yaw Error: {self.yaw_error:.0f} px", 
                   (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(debug_image, f"Linear: {self.cmd_vel.linear.x:.2f} m/s", 
                   (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(debug_image, f"Angular: {self.cmd_vel.angular.z:.2f} rad/s", 
                   (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # 状态指示器
        if self.red_box_detected:
            status_text = "RED BOX DETECTED"
            status_color = (0, 255, 0)
        else:
            status_text = "NO RED BOX"
            status_color = (0, 0, 255)
        
        cv2.putText(debug_image, status_text, 
                   (w - 300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, status_color, 2)
        
        return debug_image
    
    def create_no_box_debug_image(self):
        """创建没有检测到方块的调试图像"""
        if self.cv_image is None or not self.display:
            return
        
        debug_image = self.cv_image.copy()
        cv2.putText(debug_image, "NO RED BOX DETECTED", 
                   (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
        
        if self.display:
            cv2.imshow('Red Box Tracker', debug_image)
            cv2.waitKey(1)
    
    def run(self):
        """主循环"""
        rate = rospy.Rate(30)  # 30Hz
        
        while not rospy.is_shutdown():
            if not self.image_received:
                rospy.loginfo_once("等待相机图像...")
            
            rate.sleep()
        
        # 清理
        if self.display:
            cv2.destroyAllWindows()
        self.stop_robot()

def main():
    try:
        tracker = RedBoxTracker()
        tracker.run()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()