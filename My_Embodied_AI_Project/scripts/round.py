#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import time
from geometry_msgs.msg import Twist

class SquareMovementXY:
    def __init__(self):
        rospy.init_node('square_movement_xy', anonymous=True)
        self.pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        time.sleep(1)  # 等待发布者建立连接
        
        self.twist = Twist()
        print("初始化完成，准备开始正方形运动")
        
    def move_direction(self, linear_x, linear_y, duration):
        """向指定方向移动"""
        self.twist.linear.x = linear_x
        self.twist.linear.y = linear_y
        self.twist.linear.z = 0.0
        self.twist.angular.x = 0.0
        self.twist.angular.y = 0.0
        self.twist.angular.z = 0.0
        
        direction = ""
        if linear_x > 0 and linear_y == 0:
            direction = "向前"
        elif linear_x < 0 and linear_y == 0:
            direction = "向后"
        elif linear_x == 0 and linear_y > 0:
            direction = "向左"
        elif linear_x == 0 and linear_y < 0:
            direction = "向右"
            
        print(f"{direction}移动: X={linear_x}, Y={linear_y}, 时间={duration}秒")
        
        # 发布命令并等待
        self.pub.publish(self.twist)
        time.sleep(duration)
        
        # 停止
        self.stop()
        time.sleep(0.5)  # 短暂停顿
        
    def stop(self):
        """停止机器人"""
        self.twist.linear.x = 0.0
        self.twist.linear.y = 0.0
        self.twist.angular.z = 0.0
        self.pub.publish(self.twist)
        
    def run_square(self):
        """走正方形（使用X,Y方向）"""
        print("\n=== 开始走正方形 ===")
        
        # 第一条边：向前（X轴正方向）
        self.move_direction(0.3, 0.0, 3)
        
        # 第二条边：向左（Y轴正方向）
        self.move_direction(0.0, 0.3, 3)
        
        # 第三条边：向后（X轴负方向）
        self.move_direction(-0.3, 0.0, 3)
        
        # 第四条边：向右（Y轴负方向）
        self.move_direction(0.0, -0.3, 3)
        
        print("\n=== 正方形运动完成 ===")

if __name__ == '__main__':
    try:
        controller = SquareMovementXY()
        controller.run_square()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        # 确保机器人停止
        controller.stop()
    except Exception as e:
        print(f"\n发生错误: {e}")
        controller.stop()