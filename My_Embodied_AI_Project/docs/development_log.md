由于时间安排冲突，我22至26日在上海参加比赛，没有可以完成任务的设备，27至29日白天需要参加学校的机器人创新设计与实践公选课，只有一天加上三个晚上的时间用于完成任务。时间很紧迫，因此有些部分难以细化
——————————————————————————————————————————————————————————————————————————————————————
————————————————————————————————————————————————————————————————————————————————————

1.26
完成ubuntu下载
我在26号晚上9点左右回到武汉，开始完成任务。由于设备条件允许，我没有使用vmware，而是直接下载了ubuntu。参考了CSDN：Ubuntu20.04安装指南及初步环境配置（超级详细）包含[ROS Noetic、Terminator、Pycahrm等常用工具安装]。
由于之前找到的一个镜像源暂停服务了，所以又花费了一定的时间去找别的镜像源。利用夜间时间完成安装。
————————————————————————————————————————————————————————————————————————————————————————————
————————————————————————————————————————————————————————————————————————————————————————————————

1.27
完成ROS环境部署和任务验收点1
27号晚，我先熟悉了ubuntu的终端的使用，学习了一些常用命令，然后跟随CSDN中的教程安装ROS。学习ubuntu的终端的使用时，我主要使用了AI工具，如豆包和deepseek。由于第一次使用linux系统，对用终端进行操作很不习惯，这一步花费了很多时间。
——————————————————————————————————————————————————————————————
然后完成ROS环境部署，这一步主要参考了CSDN：Ubuntu20.04安装指南及初步环境配置（超级详细）包含[ROS Noetic、Terminator、Pycahrm等常用工具安装]。
在完成任务验收点1的时候，我又遇到了ubuntu终端使用的新问题，文件的调用还是很不熟练，任务完成后查阅了资料才知道，文件的直接调用是有方向性的，要返回上一级需要使用 cd..。
————————————————————————————————————————————————————————————————————————————————————————
——————————————————————————————————————————————————————————————————————————————————————————

1.28
完成机器人仿生部署及任务验收点2
前两天都没有遇到什么难以解决的问题，知道开始着手于这部分。一开始，我对任务书上的“前往 GitHub 获取官方包”产生了一定误解，大费周章地想办法注册github账号（虽然本来就需要注册），在官网上找了很久，后来发现，CSDN上的文章提供了下载路径。我通过百度的文心助手，通过提供关键词让文心帮忙寻找需要的参考文献。
下载官方包这一步主要参考了CSDN：宇树机器狗开发go1。
————————————————————————————————————————————————————————————————————————
然后，在尝试完成任务验收点2的过程中，如直接编译报错，依赖库缺失。实际操作后才明白，其实就是东西没下载全，而且缺失的不仅是unitree_legged_msgs。所以，在参考了相关文献后，我又下载了lcm，unitree_legged_sdk，unitree_ros,unitree_ros_to_real,将unitree_ros、unitree_ros_to_real以及前面的unitree_legged_sdk放到go1_ws/src下,把unitree_ros_to_real里的unitree_legged_msgs也移动到go1_ws/src下。在这一步，我还学习了用终端移动文件的操作。
这一步主要参考了CSDN宇树机器狗开发go1
完成这一步后，已经可以打开有机器狗和特定环境的gazebo,还可以调节world的设定，如earth 、 space 和 stairs。但机器狗还无法站立，甚至会满地乱滑。
具体步骤如下：

1：
安装LCM
下载链接：https://github.com/lcm-proj/lcm/tree/v1.4.0

下载完成后，将文件解压缩至主目录下。

在lcm-1.4.0文件夹下，终端执行以下命令，编译安装：

mkdir build
cd build
cmake ..
make
sudo make install

2：
根据运动程序版本，下载对应的SDK包：
https://github.com/unitreerobotics/unitree_legged_sdk
这里下载的是3.8.0版本，不同版本适配的机器狗不同。

3：
下载完成后，将文件解压缩至主目录下，并重命名为unitree_legged_sdk。
在unitree_legged_sdk文件夹下，终端执行以下命令编译：

cd unitree_legged_sdk
mkdir build
cd build
cmake ..
make
在unitree_legged_sdk/build文件夹下执行以下命令
sudo ./example_walk

4：
<uri>model:///home/unitree/catkin_ws/src/unitree_ros/unitree_gazebo/worlds/building_editor_models/stairs</uri>
<uri>model:///home/ubuntu/go1_ws/src/unitree_ros/unitree_gazebo/worlds/building_editor_models/stairs</uri>
catkin_make
source devel/setup.bash
为了避免每次启动launch都要执行一次source devel/setup.bash这个命令，才能执行launch，可以将其写到bashrc 文件中。
gedit ~/.bashrc
source ~/go1_ws/devel/setup.bash
终端执行以下命令在 Rviz 中查看模型：
roslaunch go1_description go1_rviz.launch
使用以下命令启动 Gazebo 仿真，此时机器狗是趴在地上的：
roslaunch unitree_gazebo normal.launch rname:=go1 wname:=stairs


5：
完成这一步后，机器狗可以站立了，但还是无法移动。
启动 Gazebo 仿真后，另起一个终端控制机器狗站立：
rosrun unitree_controller unitree_servo
在另一个终端中运行以下命令，机器狗将围绕原点旋转，这是在世界坐标系下的运动：
rosrun unitree_controller unitree_move_kinetic
这里要注意的是：要在另一个终端运行另一个命令。


参考文献：
https://blog.csdn.net/2302_80099075/article/details/156571786
————————————————————————————————————————————————————————————————————

下一步，用键盘控制机器狗运动。参考项目指导书对下一阶段任务的提示，要使用unitree_guide。通过查阅相关文献，我又下载了unitree_guide，unitree_ros，unitree_legged_msgs三个文件，其中unitree_legged_msgs在上一步中已经完成下载了。

https://github.com/unitreerobotics/unitree_guide
https://github.com/unitreerobotics/unitree_ros
https://github.com/unitreerobotics/unitree_ros_to_real

下载完成后，编译还是会报错，根据文献的指导，安装了对应的功能包move_base_msgs
sudo apt-get install ros-noetic-navigation

然后先打开一个终端，运行source ./devel/setup.bash，然后执行
roslaunch unitree_guide gazeboSim.launch 打开gazebo仿生环境。
再打开另一个终端，在相同路径下输入sudo ./devel/lib/unitree_guide/junior_ctrl，启动控制器
先按下2切换至fixed stand状态，再按4切换至trotting状态，然后就可以用键盘控制了。
按下键盘上的 W A S D 键 分别控制机器人 前进 左平移 后退 右平移。按下键盘上的 J L 键 分别控制机器人 左转 右转

参考文献：https://blog.csdn.net/Teriri_/article/details/141787540



1.29
完成第二阶段任务

在完成第二阶段任务时，我在修改源代码中遇到了很多障碍。因此，我使用了通义灵码来辅助程序的编写。遇到的问题包括，无法理解源代码的含义，不知道如何建立映射，无法打印速度及打印了速度但机器狗无法行动，还有修改代码后出现编译错误。我尝试让通义灵码对源代码进行了细致的分析，用deepseek对任务进行解读和拆解，提供指引，并借助通义灵码完成代码的修改。
以下是我使用通义灵码的具体过程。

———————————————————————————————————————————————————————————————————————————————


Q:
如何引入 ROS 订阅者，监听 /cmd_vel 话题并建立映射：将接收到的线速度和角速度映射到机器人的内部控制变量中。

A：
提供的代码已经实现了对 /cmd_vel 话题的ROS订阅者功能。以下是其工作原理：

当前实现分析
RosCmdVel 类结构
私有成员: 包含内部变量 cmd_vel_linear_x、cmd_vel_linear_y、cmd_vel_angular_z 和 new_cmd_received 来存储接收到的速度数据
订阅设置: init() 方法创建了对 /cmd_vel 话题的订阅者，使用 cmd_vel_sub = nh.subscribe<geometry_msgs::Twist>("/cmd_vel", 1, &RosCmdVel::cmdVelCallback, this)
速度映射过程
回调函数: cmdVelCallback() 接收 geometry_msgs::Twist 消息并进行映射：
msg->linear.x → cmd_vel_linear_x (前进/后退运动)
msg->linear.y → cmd_vel_linear_y (横向运动)
msg->angular.z → cmd_vel_angular_z (旋转运动)
使用流程
使用 init(ros::NodeHandle& nh) 方法初始化
当新的 /cmd_vel 消息到达时，ROS自动调用 cmdVelCallback()
通过私有成员变量访问映射后的速度值
new_cmd_received 标志指示是否有新数据可用
此实现遵循了标准的ROS模式，用于订阅速度命令并将它们映射到机器人控制系统可使用的内部控制变量。

{
    IOROS ioInter;  // Stack allocation to avoid memory leak
    ros::NodeHandle nh;
    
    // Initialize ROS cmd_vel subscriber with correct syntax
    RosCmdVel ros_cmd_vel;
    ros_cmd_vel.init(nh);
}


Q:（尝试把键盘控制获得的速度打印出来）
没有打印速度的原因

A:（以下200行为通义灵码提供的解决方法，即功能实现的路径，可直接跳过到430行）
// 旧的（错误语法）
RosCmdVel ros_cmd_vel.init(nh);

// 新的（正确）
RosCmdVel ros_cmd_vel;
ros_cmd_vel.init(nh);

但是，调试输出没有出现的原因可能有几个：

打印速度值不显示的可能原因：
没有接收到 /cmd_vel 消息：只有当实际有 Twist 消息发布到 /cmd_vel 主题时，回调函数才会执行
ROS 节点时间问题：需要有适当的 ROS 初始化和循环机制来处理回调
缓冲区同步：节点可能需要正确的 ROS 循环来处理消息
推荐解决方案：
您需要在主循环中添加 ROS 循环，以便处理回调。修改您的主函数：

cpp
// 在您的主函数中，在 COMPILE_WITH_SIMULATION 部分：
#ifdef COMPILE_WITH_SIMULATION
    ioInter = new IOROS();
    ros::NodeHandle nh;
    
    // 初始化ROS cmd_vel订阅者
    RosCmdVel ros_cmd_vel;
    ros_cmd_vel.init(nh);

    ctrlPlat = CtrlPlatform::GAZEBO;
#endif // COMPILE_WITH_SIMULATION

// 在您的主控制循环中，添加 ros::spinOnce():
while (running)
{
    ctrlFrame.run();
    
#ifdef COMPILE_WITH_SIMULATION
    ros::spinOnce();  // 添加这行来处理ROS回调
#endif
}
出现这个问题的原因：
ros::spinOnce() 处理待处理的回调，允许当消息到达时调用 cmdVelCallback
如果没有这个函数，即使有消息发布，订阅者也不会接收任何消息
调试打印只有在实际从 /cmd_vel 主题接收到速度命令时才会出现
在主循环中添加 ros::spinOnce() 来启用回调处理，这样就能看到调试输出了。

收到的线速度和角速度 如何映射 到机器人的内部控制变量

# 机器人内部控制变量映射分析

## 映射流程概述

从 [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L121-L140) 接收的速度值到机器人内部控制变量的映射过程：

### 1. 数据接收层
- [RosCmdVel::cmdVelCallback()](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L130-L140) 将 [geometry_msgs::Twist](http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/Twist.html) 消息转换为：
  - [cmd_vel_linear_x](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L124-L124) → 前向/后向速度
  - [cmd_vel_linear_y](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L125-L125) → 左右平移速度
  - [cmd_vel_angular_z](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L126-L126) → 偏航角速度

### 2. 控制架构层级

#### IOROS 接口层
- [IOROS](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/IOROS.h#L17-L55) 类会获取这些速度值并将其整合到机器人状态中
- 这些值通常存储在机器人命令结构体中

#### CtrlComponents 层
- 速度命令最终传递给 [CtrlComponents](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/control/CtrlComponents.h#L30-L76) 对象
- 在 [CtrlComponents](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/control/CtrlComponents.h#L30-L76) 中，速度值被映射到以下控制参数：

### 3. 具体映射关系

#### 用户命令映射
```cpp
// 从 ROS cmd_vel 到用户命令
UserValue userValue;
userValue.lx = cmd_vel_linear_x;      // x方向线速度
userValue.ly = cmd_vel_linear_y;      // y方向线速度  
userValue.rz = cmd_vel_angular_z;     // z轴角速度
```

#### 波形生成器输入
- [WaveGenerator](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/Gait/WaveGenerator.h#L15-L31) 使用这些速度值调整步态参数
- 速度值影响：
  - 步长（stride length）
  - 步频（step frequency）
  - 足端轨迹（foot trajectory）

#### 平衡控制器
- [BalanceCtrl](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/control/BalanceCtrl.h#L17-L31) 使用这些速度目标进行姿态平衡控制
- 线速度和角速度被转换为期望的身体姿态和足部力

### 4. 关键映射函数

在 [IOROS](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/IOROS.h#L17-L55) 实现中可能存在类似这样的函数：
```cpp
void IOROS::getUserCmd(UserValue &userCmd) {
    userCmd.lx = ros_cmd_vel.cmd_vel_linear_x;
    userCmd.ly = ros_cmd_vel.cmd_vel_linear_y;
    userCmd.rz = ros_cmd_vel.cmd_vel_angular_z;
}
```

### 5. 控制流程
1. ROS 消息 `[geometry_msgs/Twist](http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/Twist.html)` → [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L121-L140) 成员变量
2. [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L121-L140) → [IOROS](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/IOROS.h#L17-L55) 接口
3. [IOROS](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/IOROS.h#L17-L55) → [CtrlComponents](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/control/CtrlComponents.h#L30-L76) 的用户命令
4. 用户命令 → [WaveGenerator](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/Gait/WaveGenerator.h#L15-L31) 和 [BalanceCtrl](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/control/BalanceCtrl.h#L17-L31)
5. 最终生成关节位置、速度和力矩命令

这个映射过程将高层的运动命令转化为底层的关节控制指令，实现对机器人运动的精确控制。

如何查看ros是否有Twist 消息发布到 /cmd_vel 主题

# 检查ROS /cmd_vel主题上的Twist消息

## 1. 查看活动话题

首先确认话题是否存在：
```bash
rostopic list
```

查找与/cmd_vel相关的主题：
```bash
rostopic list | grep cmd_vel
```

## 2. 查看话题信息

检查话题的数据类型和连接情况：
```bash
rostopic info /cmd_vel
```

这将显示：
- 发布者数量
- 订阅者数量（应显示您的节点）
- 消息类型（应该是 `geometry_msgs/Twist`）

## 3. 监听话题数据

实时查看发布的消息：
```bash
rostopic echo /cmd_vel
```

这会持续输出发送到/cmd_vel的所有Twist消息。

## 4. 测试发送消息

您可以手动发送测试消息来验证：
```bash
# 发送前进命令
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.5
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"

# 或者发送旋转命令
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.5"
```

## 5. 检查消息统计

查看话题的消息速率和带宽使用情况：
```bash
rostopic hz /cmd_vel
```

## 6. 使用rqt工具

更直观地监控话题：
```bash
rqt
```
然后在插件中选择"Topics" -> "Topic Monitor"。

## 7. 检查ROS节点图

查看整个ROS系统的节点连接情况：
```bash
rqt_graph
```

这将显示哪个节点正在发布到/cmd_vel，以及您的节点是否正确订阅了该话题。

## 8. 编程方式检查

如果您想在代码中添加调试功能，可以在您的程序中添加：
```cpp
// 检查是否有发布者
if (cmd_vel_sub.getNumPublishers() > 0) {
    std::cout << "Found publishers on cmd_vel topic" << std::endl;
}
```

通过这些方法，您可以确定是否有其他节点在发布Twist消息到/cmd_vel主题，并验证您的订阅是否正常工作。

这个C++头文件定义了一个名为**BalanceCtrl**的类，用于机器人的平衡控制，很可能是为四足机器人设计的。该类使用二次规划(QP)方法来计算维持平衡的最佳作用力，通过求解涉及机器人动力学、摩擦约束以及足部与地面之间接触力的约束优化问题来实现平衡控制。

增加的RosCmdVel.cpp 如何加入CMakeList

Based on your code snippets, there are several issues with the current implementation that need to be addressed. Here's how to properly add [RosCmdVel.cpp](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/RosCmdVel.cpp) to your CMakeLists.txt:

## Issues in Current Code

1. **Incorrect instantiation**: In your [main.cpp](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/main.cpp) you have `RosCmdVel ros_cmd_vel.init(nh);` which is invalid syntax
2. **Missing file compilation**: You're referencing [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L11-L64) but haven't compiled it into your project

## Solution

### 1. Add RosCmdVel.cpp to CMakeLists.txt

Add this to your [/home/zjn/go1_ws/src/unitree_ros_to_real/unitree_legged_real/CMakeLists.txt](file:///home/zjn/go1_ws/src/unitree_ros_to_real/unitree_legged_real/CMakeLists.txt):

```cmake
# Add the new source file to one of your executables or create a library
# Option 1: Add as part of existing executable
target_sources(example_walk PRIVATE 
    src/RosCmdVel.cpp
)

# OR Option 2: Create a library if multiple executables use it
add_library(ros_interface_lib 
    src/interface/RosCmdVel.cpp
    # other interface files...
)
target_link_libraries(example_walk ros_interface_lib ${EXTRA_LIBS} ${catkin_LIBRARIES})
```

### 2. Fix Your Main.cpp

Replace this incorrect line:
```cpp
// This is wrong:
RosCmdVel ros_cmd_vel.init(nh);
```

With proper initialization:
```cpp
// Correct approach:
RosCmdVel* rosCmdVel = new RosCmdVel();
rosCmdVel->init(nh);
```

### 3. Complete Integration Example

Your corrected main.cpp section should look like:
```cpp
#ifdef COMPILE_WITH_SIMULATION
ioInter = new IOROS();
#ifdef RUN_ROS
ros::NodeHandle nh;
ros::NodeHandle nh_private("~");

// Initialize ROS cmd_vel subscriber correctly
RosCmdVel* rosCmdVel = new RosCmdVel();
rosCmdVel->init(nh_private);
#endif // RUN_ROS
#endif // COMPILE_WITH_SIMULATION
```

### 4. Don't Forget Include

Make sure you have the proper include in main.cpp:
```cpp
#include "interface/RosCmdVel.h"
```

The key is to ensure that all source files that are referenced in your project are properly compiled using either `add_executable()` with `target_sources()` or `add_library()`.

————————————————————————————————————————————————————————————————————————


根据指导，实现了速度的打印，能实现监听，并且能打印手动输入的数据。接下来研究该如何建立映射，用输入的数据控制机器狗的运动,但是由于代码太复杂，难以入手。
我重新浏览了KeyBoard.cpp文件发现键盘控制于一个名为uservalue的变量密切相关，似乎键盘是通过改变uservalue的值来控制机器狗运动的。所以我希望通过手动输入的数据改变uservalue的值从而实现控制。我先研究了uservalue是什么，以及如何修改。

Q:
参考KeyBoard::changeValue() 函数 ，在RosCmdVel::cmdVelCallback里修改uservalue

A:
根据你的需求，你需要在 [RosCmdVel::cmdVelCallback](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L52-L52) 函数中修改 [userValue](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/CmdPanel.h#L51-L51)，类似于 [KeyBoard::changeValue()](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/src/interface/KeyBoard.cpp#L64-L91) 函数的功能。以下是修改后的代码：

## 修改 RosCmdVel.cpp

```cpp
void RosCmdVel::cmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
    std::lock_guard<std::mutex> lock(mutex_);
    
    // Apply velocity limits
    cmd_vel_linear_x = std::max(std::min(msg->linear.x, max_linear_vel), -max_linear_vel);
    cmd_vel_linear_y = std::max(std::min(msg->linear.y, max_linear_vel), -max_linear_vel);
    cmd_vel_angular_z = std::max(std::min(msg->angular.z, max_angular_vel), -max_angular_vel);
    
    // Update userValue based on received cmd_vel, similar to KeyBoard::changeValue()
    userValue.lx = cmd_vel_linear_x;  // Map linear x velocity to userValue.lx
    userValue.ly = cmd_vel_linear_y;  // Map linear y velocity to userValue.ly  
    userValue.ry = cmd_vel_angular_z; // Map angular z velocity to userValue.ry (rotation)
    
    new_cmd_received = true;
    last_cmd_time = ros::Time::now();
    
    std::cout << "Received cmd_vel: linear.x=" << cmd_vel_linear_x 
              << ", linear.y=" << cmd_vel_linear_y 
              << ", angular.z=" << cmd_vel_angular_z 
              << ", userValue: lx=" << userValue.lx 
              << ", ly=" << userValue.ly 
              << ", ry=" << userValue.ry << std::endl;
              
    // Optional: print received velocities
    ROS_DEBUG_THROTTLE(1.0, "Received cmd_vel: linear.x=%.2f, linear.y=%.2f, angular.z=%.2f", 
                       cmd_vel_linear_x, cmd_vel_linear_y, cmd_vel_angular_z);
}
```

## 需要注意的几点

1. **包含头文件**：确保 [RosCmdVel.h](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h) 中包含了所需的头文件，以便访问 [userValue](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/CmdPanel.h#L51-L51) 结构。

2. **添加成员变量**：在 [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L11-L64) 类中添加 [userValue](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/CmdPanel.h#L51-L51) 成员变量：

```cpp
// 在 RosCmdVel 类定义中添加
class RosCmdVel {
private:
    // ... 其他成员变量 ...
    UserValue userValue;  // 需要包含相应的头文件定义UserValue结构
    
public:
    // ... 其他方法 ...
};
```

3. **映射关系**：根据你的具体需求调整线性速度和角速度到 [userValue](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/CmdPanel.h#L51-L51) 各轴的映射关系，因为 `cmd_vel` 是笛卡尔坐标系下的速度，而 [userValue](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/CmdPanel.h#L51-L51) 可能是控制框架内的特定表示。

这样的修改使得 [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L11-L64) 类也能像 [KeyBoard](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/KeyBoard.h#L22-L45) 类一样更新用户的输入值，从而可以通过 ROS 的 `cmd_vel` 主题控制机器人移动。

roscmdvel类的功能整合到keyboard类

我理解您想要将 [RosCmdVel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L11-L64) 类的功能整合到 [KeyBoard](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/KeyBoard.h#L22-L45) 类中，这样可以通过 ROS 的 [cmd_vel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L60-L60) 主题和键盘同时控制机器人。以下是整合后的代码：

## 修改 KeyBoard.h 头文件

首先，在头文件中添加 ROS 相关功能：

```cpp
#ifndef KEYBOARD_H
#define KEYBOARD_H

#include <termios.h>
#include <pthread.h>
#include <sys/select.h>
#include <unistd.h>
#include <fcntl.h>
#include <mutex>

#ifdef COMPILE_WITH_ROS
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#endif

// 假设这些是你已有的类型定义
struct UserValue {
    float lx, ly, rx, ry;
    void setZero() { lx = ly = rx = ry = 0.0f; }
};

enum class UserCommand {
    NONE, L2_B, L2_A, L2_X, START, L2_Y, L1_X, L1_A, L1_Y
};

class KeyBoard {
public:
    KeyBoard();
    ~KeyBoard();

    UserCommand checkCmd();
    void changeValue();
    
    // 新增 ROS cmd_vel 回调功能
    void cmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg);
    void initRos(ros::NodeHandle& nh);
    
    // 公共访问成员
    UserCommand userCmd;
    UserValue userValue;

private:
    static void* runKeyBoard(void *arg);
    void* run(void *arg);
    
    // 键盘控制相关
    struct termios _oldSettings, _newSettings;
    pthread_t _tid;
    fd_set set;
    int res, ret;
    char _c;

    // ROS 控制相关
    #ifdef COMPILE_WITH_ROS
    ros::Subscriber cmd_vel_sub;
    float cmd_vel_linear_x, cmd_vel_linear_y, cmd_vel_angular_z;
    bool new_cmd_received;
    double cmd_timeout;
    double max_linear_vel, max_angular_vel;
    ros::Time last_cmd_time;
    std::mutex mutex_;
    #endif
};

#endif // KEYBOARD_H
```

## 修改 KeyBoard.cpp 实现文件

```cpp
/**********************************************************************
 Copyright (c) 2020-2023, Unitree Robotics.Co.Ltd. All rights reserved.
***********************************************************************/
#include "interface/KeyBoard.h"
#include <iostream>

#ifdef COMPILE_WITH_ROS
#include <geometry_msgs/Twist.h>
#endif

KeyBoard::KeyBoard(){
    userCmd = UserCommand::NONE;
    userValue.setZero();

    tcgetattr( fileno( stdin ), &_oldSettings );
    _newSettings = _oldSettings;
    _newSettings.c_lflag &= (~ICANON & ~ECHO);
    tcsetattr( fileno( stdin ), TCSANOW, &_newSettings );

    pthread_create(&_tid, NULL, runKeyBoard, (void*)this);
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
        userValue.ly = std::min<float>(userValue.ly+sensitivityLeft, 1.0);
        break;
    case 's':case 'S':
        userValue.ly = std::max<float>(userValue.ly-sensitivityLeft, -1.0);
        break;
    case 'd':case 'D':
        userValue.lx = std::min<float>(userValue.lx+sensitivityLeft, 1.0);
        break;
    case 'a':case 'A':
        userValue.lx = std::max<float>(userValue.lx-sensitivityLeft, -1.0);
        break;

    case 'i':case 'I':
        userValue.ry = std::min<float>(userValue.ry+sensitivityRight, 1.0);
        break;
    case 'k':case 'K':
        userValue.ry = std::max<float>(userValue.ry-sensitivityRight, -1.0);
        break;
    case 'l':case 'L':
        userValue.rx = std::min<float>(userValue.rx+sensitivityRight, 1.0);
        break;
    case 'j':case 'J':
        userValue.rx = std::max<float>(userValue.rx-sensitivityRight, -1.0);
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
    
    // 更新 userValue，类似 keyboard 的 changeValue 功能
    userValue.lx = cmd_vel_linear_x;      // 映射 x 方向线速度到 lx
    userValue.ly = cmd_vel_linear_y;      // 映射 y 方向线速度到 ly
    userValue.ry = cmd_vel_angular_z;     // 映射 z 轴角速度到 ry (旋转)
    
    new_cmd_received = true;
    last_cmd_time = ros::Time::now();
    
    std::cout << "Received cmd_vel via ROS: linear.x=" << cmd_vel_linear_x 
              << ", linear.y=" << cmd_vel_linear_y 
              << ", angular.z=" << cmd_vel_angular_z 
              << ", userValue: lx=" << userValue.lx 
              << ", ly=" << userValue.ly 
              << ", ry=" << userValue.ry << std::endl;
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
```

## 修改 main.cpp

```cpp
// 在 main.cpp 中，现在只需要初始化一个 KeyBoard 对象
#ifdef COMPILE_WITH_SIMULATION
    ioInter = new IOROS();
#ifdef RUN_ROS
    ros::NodeHandle nh;
    ros::NodeHandle nh_private("~");
    
    // 初始化键盘控制对象，它现在也包含 ROS 功能
    KeyBoard* keyboard = new KeyBoard();
    keyboard->initRos(nh_private);
    
    // 如果需要，也可以将 keyboard 对象传递给其他组件
#endif // RUN_ROS

    ctrlPlat = CtrlPlatform::GAZEBO;
#endif // COMPILE_WITH_SIMULATION

// 在主循环中也需要处理 ROS 回调
while (running)
{
    ctrlFrame.run();
    #ifdef COMPILE_WITH_SIMULATION
    ros::spinOnce();
    #endif
}
```

这样整合后，[KeyBoard](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/KeyBoard.h#L22-L45) 类既可以响应键盘输入，也可以接收 ROS 的 [cmd_vel](file:///home/zjn/go1_ws/src/unitree_guide/unitree_guide/include/interface/RosCmdVel.h#L60-L60) 消息，实现了两种控制方式的融合。


根据通义灵码的指导，我修改了KeyBoard.h的头文件，修改 KeyBoard.cpp实现文件，初始化默认值，更新 userValue，类似 keyboard 的 changeValue 功能，修改 main.cpp，最终实现了通过手动输入x y z的值来控制机器狗定向移动。

——————————————————————————————————————————————————————————————————————————————

接下来开始编写脚本，使机器狗走出一个正方形。
在这里我遇到了一个问题：无法通过输入z的值来使机器狗转向，只能使其前进后退及左右侧向移动。初步推断是底层代码的问题，但由于时间紧迫，无法深入研究，只能先将就着让机器狗往四个方向移动来实现走正方形，没有对转向的时间进行测试，但由于侧向移动的速度明显低于前进后退，需要修改运动的速度和时间来保证相邻两条边的长度近似。

发布指令有两种方式：
一是直接手动输入，这对排版缩进有很高的要求，我先草稿中编写再复制：
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.3
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.3
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: -0.3
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: -0.3
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"

  二是编写一个python脚本，这一步由deepseek提供了框架：
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


        ————————————————————————————————————————————————————————————————————
        ————————————————————————————————————————————————————————————————————

        1.30
        完成第三阶段任务和任务验收点4

        这个任务相对容易完成，因为将任务步骤交给deepseek之后就得到了完整的代码，而不是像上一个任务那样，只有模糊的指引，需要反复多次提问和修改。

        一开始deepseek提供的程序编译不通过，在统一了变量名后就编译通过了。
        然后对程序进行修改。一开始运行camera.py时，摄像头的视角是颠倒的，且角度和指导书中的实例相比明显偏高。在询问AI后实现了摄像头的角度调整及画面的上下翻转和左右翻转。

        然后在测试过程中发现改变y的值才能使机器狗前进后退，但deepseek搞成x了，以及移动速度过慢效果不明显等问题，都一一进行了修正。

        另外，一开始机器狗出现了走了几步就不走的情况，在打印了面积和质心坐标等数据后发现，这是由于deepseek提供的方块目标面积过小，在初始位置就达到了最终要求，所以更改了目标面积，效果明显变好了。

        但是，同上一个任务一样，我无法通过更改z的值实现机器狗的转向，只能改为在方块质心偏移时修改x的值，使其侧向移动来代替转向，但效果不是很好。后面再继续研究如何让机器狗转向。