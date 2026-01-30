
# 机器人仿真开发项目日志

## 时间安排说明
由于时间安排冲突：
- **22至26日**：在上海参加比赛，没有可以完成任务的设备
- **27至29日白天**：需要参加学校的机器人创新设计与实践公选课
- 只有一天加上三个晚上的时间用于完成任务
- 时间很紧迫，因此有些部分难以细化

---

## 1月26日：完成Ubuntu下载

**时间**：26号晚上9点左右回到武汉，开始完成任务

**工作内容**：
- 由于设备条件允许，我没有使用VMware，而是直接下载了Ubuntu
- 参考了CSDN文章：[Ubuntu20.04安装指南及初步环境配置（超级详细）包含[ROS Noetic、Terminator、Pycahrm等常用工具安装]]()

**遇到的问题**：
- 之前找到的一个镜像源暂停服务了，花费了一定的时间去找别的镜像源

**解决方案**：
- 利用夜间时间完成安装

---

## 1月27日：完成ROS环境部署和任务验收点1

### 一、熟悉Ubuntu终端
**工作内容**：
- 熟悉Ubuntu终端的使用，学习了一些常用命令
- 跟随CSDN教程安装ROS

**学习工具**：
- AI工具：豆包和DeepSeek

**遇到的困难**：
- 第一次使用Linux系统，对用终端进行操作很不习惯
- 这一步花费了很多时间

### 二、完成ROS环境部署
**参考资料**：
- CSDN：[Ubuntu20.04安装指南及初步环境配置（超级详细）包含[ROS Noetic、Terminator、Pycahrm等常用工具安装]]()

### 三、完成任务验收点1
**遇到的问题**：
- 文件的调用不熟练
- 任务完成后查阅资料才知道，文件的直接调用是有方向性的
- 要返回上一级需要使用 `cd..`

---

## 1月28日：完成机器人仿真部署及任务验收点2

### 一、获取官方包
**遇到的问题**：
- 对任务书上的"前往 GitHub 获取官方包"产生误解
- 大费周章地想办法注册GitHub账号（虽然本来就需要注册）
- 在官网上找了很久，后来发现CSDN上的文章提供了下载路径

**解决方案**：
- 通过百度的文心助手，提供关键词让文心帮忙寻找需要的参考文献
- 参考CSDN文章：[宇树机器狗开发go1]()

### 二、依赖库安装与编译
**遇到的问题**：
- 直接编译报错，依赖库缺失
- 实际操作后才明白，不仅是`unitree_legged_msgs`缺失

**解决方案**：
1. 下载以下组件：
   - `lcm`
   - `unitree_legged_sdk`
   - `unitree_ros`
   - `unitree_ros_to_real`

2. 文件放置：
   - 将`unitree_ros`、`unitree_ros_to_real`以及前面的`unitree_legged_sdk`放到`go1_ws/src`下
   - 把`unitree_ros_to_real`里的`unitree_legged_msgs`也移动到`go1_ws/src`下

3. 学习用终端移动文件的操作

### 三、具体安装步骤

#### 1. 安装LCM
```bash
# 下载链接：https://github.com/lcm-proj/lcm/tree/v1.4.0
# 将文件解压缩至主目录下

# 在lcm-1.4.0文件夹下，终端执行以下命令，编译安装：
mkdir build
cd build
cmake ..
make
sudo make install
```

#### 2. 下载SDK包
```bash
# 根据运动程序版本，下载对应的SDK包：
# https://github.com/unitreerobotics/unitree_legged_sdk
# 这里下载的是3.8.0版本，不同版本适配的机器狗不同

# 下载完成后，将文件解压缩至主目录下，并重命名为unitree_legged_sdk
cd unitree_legged_sdk
mkdir build
cd build
cmake ..
make

# 在unitree_legged_sdk/build文件夹下执行以下命令
sudo ./example_walk
```

#### 3. 环境配置
```bash
# 修改路径配置
<uri>model:///home/unitree/catkin_ws/src/unitree_ros/unitree_gazebo/worlds/building_editor_models/stairs</uri>
<uri>model:///home/ubuntu/go1_ws/src/unitree_ros/unitree_gazebo/worlds/building_editor_models/stairs</uri>

# 编译
catkin_make
source devel/setup.bash

# 将命令写入bashrc文件，避免每次启动都要执行
gedit ~/.bashrc
# 添加：source ~/go1_ws/devel/setup.bash
```

#### 4. 启动仿真环境
```bash
# 在Rviz中查看模型
roslaunch go1_description go1_rviz.launch

# 启动Gazebo仿真（此时机器狗是趴在地上的）
roslaunch unitree_gazebo normal.launch rname:=go1 wname:=stairs

# 控制机器狗站立
rosrun unitree_controller unitree_servo

# 机器狗围绕原点旋转（世界坐标系下的运动）
rosrun unitree_controller unitree_move_kinetic
```

**注意**：需要在另一个终端运行另一个命令

**参考文献**：
- https://blog.csdn.net/2302_80099075/article/details/156571786

### 四、键盘控制机器狗运动
**需要下载的文件**：
1. https://github.com/unitreerobotics/unitree_guide
2. https://github.com/unitreerobotics/unitree_ros
3. https://github.com/unitreerobotics/unitree_ros_to_real

**安装依赖**：
```bash
sudo apt-get install ros-noetic-navigation
```

**启动步骤**：
```bash
# 打开Gazebo仿真环境
source ./devel/setup.bash
roslaunch unitree_guide gazeboSim.launch

# 启动控制器（另一个终端）
sudo ./devel/lib/unitree_guide/junior_ctrl
```

**控制方式**：
1. 按下 `2` 切换至 `fixed stand` 状态
2. 按下 `4` 切换至 `trotting` 状态
3. 键盘控制：
   - `W` `A` `S` `D`：前进、左平移、后退、右平移
   - `J` `L`：左转、右转

**参考文献**：
- https://blog.csdn.net/Teriri_/article/details/141787540

---

## 1月29日：完成第二阶段任务

### 一、使用AI辅助编程
**遇到的问题**：
1. 无法理解源代码的含义
2. 不知道如何建立映射
3. 无法打印速度及打印了速度但机器狗无法行动
4. 修改代码后出现编译错误

**使用的工具**：
1. **通义灵码**：对源代码进行细致的分析，完成代码的修改
2. **DeepSeek**：对任务进行解读和拆解，提供指引

### 二、具体问题与解决方案

#### 问题1：如何引入ROS订阅者，监听`/cmd_vel`话题并建立映射
**回答分析**：
- `RosCmdVel`类已实现订阅`/cmd_vel`话题的功能
- 速度映射过程：
  - `msg->linear.x` → `cmd_vel_linear_x`（前进/后退运动）
  - `msg->linear.y` → `cmd_vel_linear_y`（横向运动）
  - `msg->angular.z` → `cmd_vel_angular_z`（旋转运动）

**正确初始化方式**：
```cpp
#ifdef COMPILE_WITH_SIMULATION
    ioInter = new IOROS();
    ros::NodeHandle nh;
    
    // 初始化ROS cmd_vel订阅者
    RosCmdVel ros_cmd_vel;
    ros_cmd_vel.init(nh);

    ctrlPlat = CtrlPlatform::GAZEBO;
#endif // COMPILE_WITH_SIMULATION
```

#### 问题2：没有打印速度的原因
**解决方案**：
在主循环中添加`ros::spinOnce()`：
```cpp
while (running)
{
    ctrlFrame.run();
    
#ifdef COMPILE_WITH_SIMULATION
    ros::spinOnce();  // 添加这行来处理ROS回调
#endif
}
```

#### 问题3：速度映射到机器人内部控制变量
**映射流程**：
1. ROS消息`geometry_msgs/Twist` → `RosCmdVel`成员变量
2. `RosCmdVel` → `IOROS`接口
3. `IOROS` → `CtrlComponents`的用户命令
4. 用户命令 → `WaveGenerator`和`BalanceCtrl`
5. 最终生成关节位置、速度和力矩命令

#### 问题4：如何检查ROS是否有Twist消息发布
**检查方法**：
```bash
# 1. 查看活动话题
rostopic list
rostopic list | grep cmd_vel

# 2. 查看话题信息
rostopic info /cmd_vel

# 3. 监听话题数据
rostopic echo /cmd_vel

# 4. 测试发送消息
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear: x: 0.5 y: 0.0 z: 0.0 angular: x: 0.0 y: 0.0 z: 0.0"
```

#### 问题5：将`RosCmdVel.cpp`加入CMakeLists.txt
**解决方案**：
```cmake
# 选项1：作为现有可执行文件的一部分
target_sources(example_walk PRIVATE 
    src/RosCmdVel.cpp
)

# 选项2：创建库（如果多个可执行文件使用它）
add_library(ros_interface_lib 
    src/interface/RosCmdVel.cpp
    # other interface files...
)
target_link_libraries(example_walk ros_interface_lib ${EXTRA_LIBS} ${catkin_LIBRARIES})
```

### 三、关键代码修改

#### 1. 修改`RosCmdVel::cmdVelCallback`函数
```cpp
void RosCmdVel::cmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg)
{
    std::lock_guard<std::mutex> lock(mutex_);
    
    // 应用速度限制
    cmd_vel_linear_x = std::max(std::min(msg->linear.x, max_linear_vel), -max_linear_vel);
    cmd_vel_linear_y = std::max(std::min(msg->linear.y, max_linear_vel), -max_linear_vel);
    cmd_vel_angular_z = std::max(std::min(msg->angular.z, max_angular_vel), -max_angular_vel);
    
    // 更新userValue，类似KeyBoard::changeValue()功能
    userValue.lx = cmd_vel_linear_x;  // 映射x方向线速度到userValue.lx
    userValue.ly = cmd_vel_linear_y;  // 映射y方向线速度到userValue.ly  
    userValue.ry = cmd_vel_angular_z; // 映射z轴角速度到userValue.ry（旋转）
    
    new_cmd_received = true;
    last_cmd_time = ros::Time::now();
    
    std::cout << "Received cmd_vel: linear.x=" << cmd_vel_linear_x 
              << ", linear.y=" << cmd_vel_linear_y 
              << ", angular.z=" << cmd_vel_angular_z 
              << ", userValue: lx=" << userValue.lx 
              << ", ly=" << userValue.ly 
              << ", ry=" << userValue.ry << std::endl;
}
```

#### 2. 将`RosCmdVel`功能整合到`KeyBoard`类
**修改`KeyBoard.h`头文件**：
```cpp
#ifdef COMPILE_WITH_ROS
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#endif

class KeyBoard {
public:
    // 新增 ROS cmd_vel 回调功能
    void cmdVelCallback(const geometry_msgs::Twist::ConstPtr& msg);
    void initRos(ros::NodeHandle& nh);
    
private:
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
```

### 四、实现结果
根据通义灵码的指导，完成了以下修改：
1. 修改了`KeyBoard.h`的头文件
2. 修改了`KeyBoard.cpp`实现文件
3. 初始化默认值
4. 更新`userValue`，类似`keyboard`的`changeValue`功能
5. 修改了`main.cpp`

**最终效果**：实现了通过手动输入x、y、z的值来控制机器狗定向移动

### 五、正方形运动脚本

#### 方案一：手动输入命令
```bash
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
```

#### 方案二：Python脚本（DeepSeek提供框架）
```python
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
```

**遇到的问题**：
- 无法通过输入z的值来使机器狗转向，只能使其前进后退及左右侧向移动
- 初步推断是底层代码的问题，但由于时间紧迫，无法深入研究
- 只能用机器狗往四个方向移动来实现走正方形
- 侧向移动的速度明显低于前进后退，需要修改运动的速度和时间来保证相邻两条边的长度近似

---

## 1月30日：完成第三阶段任务和任务验收点4

### 一、任务特点
- 相对容易完成，因为将任务步骤交给DeepSeek之后就得到了完整的代码
- 不像上一个任务那样只有模糊的指引，需要反复多次提问和修改

### 二、遇到的问题与解决方案

#### 1. 程序编译不通过
**问题**：DeepSeek提供的程序编译不通过
**解决方案**：统一变量名后编译通过

#### 2. 摄像头视角问题
**问题**：
- 摄像头的视角是颠倒的
- 角度和指导书中的实例相比明显偏高

**解决方案**：
- 询问AI后实现了摄像头的角度调整
- 实现画面的上下翻转和左右翻转

#### 3. 控制方向问题
**问题**：改变y的值才能使机器狗前进后退，但DeepSeek搞成x了
**解决方案**：修正控制方向映射

#### 4. 移动速度问题
**问题**：移动速度过慢效果不明显
**解决方案**：调整速度参数

#### 5. 机器狗停止过早
**问题**：机器狗走了几步就不走
**调试过程**：
1. 打印面积和质心坐标等数据
2. 发现DeepSeek提供的方块目标面积过小
3. 在初始位置就达到了最终要求

**解决方案**：更改目标面积，效果明显变好

#### 6. 转向控制问题
**问题**：同上一个任务一样，无法通过更改z的值实现机器狗的转向
**临时解决方案**：
- 在方块质心偏移时修改x的值
- 使其侧向移动来代替转向
- 效果不是很好

**后续计划**：需要继续研究如何让机器狗转向

---

## 总结

### 取得的成果
1. 成功搭建了Ubuntu环境和ROS系统
2. 完成了机器狗仿真环境的部署
3. 实现了基本的键盘控制和ROS话题控制
4. 开发了正方形运动脚本
5. 完成了摄像头视觉识别任务

### 遇到的问题
1. 时间紧迫，部分功能无法深入研究
2. 机器狗转向控制存在底层问题
3. 对Linux系统和ROS框架不熟悉，学习成本较高

### 使用的工具
1. **AI辅助编程**：通义灵码、DeepSeek、豆包
2. **参考资料**：CSDN博客、GitHub官方文档
3. **开发环境**：Ubuntu 20.04、ROS Noetic

### 经验教训
1. 对于复杂项目，提前做好时间规划非常重要
2. AI工具可以大大提高开发效率，但仍需要人工调试和验证
3. 遇到问题时要善于查阅文档和寻求帮助

---

**文档生成时间**：2024年1月

**开发者**：[周佳妮]

**项目名称**：机器狗仿真与控制项目



