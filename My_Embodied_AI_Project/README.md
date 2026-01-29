# Unitree 机器狗仿真控制指南
## 安装ros 资料
https://blog.csdn.net/2302_80099075/article/details/156571786
### 安装 Gazebo仿真环境 资料
https://blog.csdn.net/Jenniehubby/article/details/134780066

## 一、仿真环境启动

### 1. 基础仿真启动
启动带有引导控制的 Gazebo 仿真环境：
```bash
roslaunch unitree_guide gazeboSim.launch


### 2.控制器启动
     在另一个终端中启动控制器：

# 方法1：使用编译后的控制器
./devel/lib/unitree_guide/junior_ctrl

# 方法2：使用标准控制器
rosrun unitree_controller unitree_servo

  
#### 基础控制操作

启动控制器后，机器人会躺在仿真环境中。按以下键位控制：

    '2'键 - 从Passive状态切换到FixedStand状态
    '4'键 - 从FixedStand状态切换到Trotting状态
    'WASD'键 - 控制机器人平移
    'JL'键 - 控制机器人旋转
    空格键 - 停止并站立

