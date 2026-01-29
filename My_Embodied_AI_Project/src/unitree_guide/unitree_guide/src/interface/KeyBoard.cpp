/**********************************************************************
 Copyright (c) 2020-2023, Unitree Robotics.Co.Ltd. All rights reserved.
***********************************************************************/
#include "interface/KeyBoard.h"
#include <iostream>

KeyBoard::KeyBoard(){
    userCmd = UserCommand::NONE;
    userValue.setZero();

    tcgetattr( fileno( stdin ), &_oldSettings );
    _newSettings = _oldSettings;
    _newSettings.c_lflag &= (~ICANON & ~ECHO);
    tcsetattr( fileno( stdin ), TCSANOW, &_newSettings );

    pthread_create(&_tid, NULL, runKeyBoard, (void*)this);
    ros::NodeHandle nh;
    ros::NodeHandle nh_private("~");
     initRos(nh_private);
}

KeyBoard::~KeyBoard(){
    pthread_cancel(_tid);
    pthread_join(_tid, NULL);
    tcsetattr( fileno( stdin ), TCSANOW, &_oldSettings );
}

UserCommand KeyBoard::checkCmd(){
    switch (_c){
    case '1':
        return UserCommand::L2_B;
    case '2':
        return UserCommand::L2_A;
    case '3':
        return UserCommand::L2_X;
    case '4':
        return UserCommand::START;
#ifdef COMPILE_WITH_MOVE_BASE
    case '5':
        return UserCommand::L2_Y;
#endif  // COMPILE_WITH_MOVE_BASE
    case '0':
        return UserCommand::L1_X;
    case '9':
        return UserCommand::L1_A;
    case '8':
        return UserCommand::L1_Y;
    case ' ':
        userValue.setZero();
        return UserCommand::NONE;
    default:
        return UserCommand::NONE;
    }
}

void KeyBoard::changeValue(){
    switch (_c){
    case 'w':case 'W':
        userValue.ly = min<float>(userValue.ly+sensitivityLeft, 1.0);
        break;
    case 's':case 'S':
        userValue.ly = max<float>(userValue.ly-sensitivityLeft, -1.0);
        break;
    case 'd':case 'D':
        userValue.lx = min<float>(userValue.lx+sensitivityLeft, 1.0);
        break;
    case 'a':case 'A':
        userValue.lx = max<float>(userValue.lx-sensitivityLeft, -1.0);
        break;

    case 'i':case 'I':
        userValue.ry = min<float>(userValue.ry+sensitivityRight, 1.0);
        break;
    case 'k':case 'K':
        userValue.ry = max<float>(userValue.ry-sensitivityRight, -1.0);
        break;
    case 'l':case 'L':
        userValue.rx = min<float>(userValue.rx+sensitivityRight, 1.0);
        break;
    case 'j':case 'J':
        userValue.rx = max<float>(userValue.rx-sensitivityRight, -1.0);
        break;
    default:
        break;
    }
}

#ifdef COMPILE_WITH_ROS
void KeyBoard::initRos(ros::NodeHandle& nh) {
    cmd_vel_sub = nh.subscribe<geometry_msgs::Twist>(
        "/cmd_vel", 1, &KeyBoard::cmdVelCallback, this);
    
    // 初始化默认值
    cmd_vel_linear_x = 0.0;
    cmd_vel_linear_y = 0.0;
    cmd_vel_angular_y = 0.0;
    cmd_vel_angular_y = 0.0;
    cmd_vel_angular_z = 0.0;
    new_cmd_received = false;
    cmd_timeout = 0.5;  // 500ms timeout
    max_linear_vel = 0.5;   // default max linear velocity: 0.5 m/s
    max_angular_vel = 1.0;  // default max angular velocity: 1.0 rad/s
    last_cmd_time = ros::Time(0);
    
    // 从 ROS 参数服务器获取参数
    nh.param<double>("max_linear_velocity", max_linear_vel, 0.5);
    nh.param<double>("max_angular_velocity", max_angular_vel, 1.0);
    nh.param<double>("cmd_timeout", cmd_timeout, 0.5);
    
    std::cout << "ROS Cmd_vel subscriber initialized" << std::endl;
    std::cout << "Max linear velocity: " << max_linear_vel << " m/s" << std::endl;
    std::cout << "Max angular velocity: " << max_angular_vel << " rad/s" << std::endl;
}

void KeyBoard::cmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg) {
    std::lock_guard<std::mutex> lock(mutex_);
    
    // 应用速度限制
    cmd_vel_linear_x = std::max(std::min(msg->linear.x, (double)max_linear_vel), -(double)max_linear_vel);
    cmd_vel_linear_y = std::max(std::min(msg->linear.y, (double)max_linear_vel), -(double)max_linear_vel);
    cmd_vel_angular_z = std::max(std::min(msg->angular.z, (double)max_angular_vel), -(double)max_angular_vel);
    
    cmd_vel_angular_x = std::max(std::min(msg->angular.x, (double)max_angular_vel), -(double)max_angular_vel);
   cmd_vel_angular_y = std::max(std::min(msg->angular.y, (double)max_angular_vel), -(double)max_angular_vel);
  

    // 更新 userValue，类似 keyboard 的 changeValue 功能
    userValue.lx = cmd_vel_linear_x;      // 映射 x 方向线速度到 lx
    userValue.ly = cmd_vel_linear_y;      // 映射 y 方向线速度到 ly
    //userValue.rx = cmd_vel_angular_x;     // 映射 z 轴角速度到 ry (旋转)
    userValue.ry = cmd_vel_angular_z;     // 映射 z 轴角速度到 ry (旋转)
   // userValue.rz = cmd_vel_angular_z;     // 映射 z 轴角速度到 ry (旋转)
    new_cmd_received = true;
    last_cmd_time = ros::Time::now();
    
    std::cout << "Received cmd_vel via ROS: linear.x=" << cmd_vel_linear_x 
              << ", linear.y=" << cmd_vel_linear_y 
              << ", angular.z=" << cmd_vel_angular_z 
              << ", userValue: lx=" << userValue.lx 
              << ", ly=" << userValue.ly 
              << ", rx=" << userValue.rx 
              << ", ry=" << userValue.ry  <<std::endl;
}
#endif // COMPILE_WITH_ROS

void* KeyBoard::runKeyBoard(void *arg){
    ((KeyBoard*)arg)->run(NULL);
    return NULL;
}

void* KeyBoard::run(void *arg){
    while(1){
        FD_ZERO(&set);
        FD_SET( fileno( stdin ), &set );

        res = select( fileno( stdin )+1, &set, NULL, NULL, NULL);

        if(res > 0){
            ret = read( fileno( stdin ), &_c, 1 );
            userCmd = checkCmd();
            if(userCmd == UserCommand::NONE)
                changeValue();
            _c = '\0';
        }
        usleep(1000);
    }
    return NULL;
}