/**********************************************************************
 Copyright (c) 2020-2023, Unitree Robotics.Co.Ltd. All rights reserved.
***********************************************************************/
#ifndef KEYBOARD_H
#define KEYBOARD_H

#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include "interface/CmdPanel.h"
#include "common/mathTools.h"
#ifdef COMPILE_WITH_ROS
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#endif
class KeyBoard : public CmdPanel{
public:
    KeyBoard();
    ~KeyBoard();
     // 新增 ROS cmd_vel 回调功能
    void cmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg);
    void initRos(ros::NodeHandle& nh);
private:
    static void* runKeyBoard(void *arg);
    void* run(void *arg);
    UserCommand checkCmd();
    void changeValue();

    pthread_t _tid;
    float sensitivityLeft = 0.05;
    float sensitivityRight = 0.05;
    struct termios _oldSettings, _newSettings;
    fd_set set;
    int res;
    int ret;
    char _c;
    #ifdef COMPILE_WITH_ROS
    ros::Subscriber cmd_vel_sub;
    float cmd_vel_linear_x, cmd_vel_linear_y,cmd_vel_angular_x,cmd_vel_angular_y, cmd_vel_angular_z;
    bool new_cmd_received;
    double cmd_timeout;
    double max_linear_vel, max_angular_vel;
    ros::Time last_cmd_time;
    std::mutex mutex_;
    #endif
};

#endif  // KEYBOARD_H