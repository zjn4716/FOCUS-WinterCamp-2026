# Unitree 机器狗仿真控制指南

## 安装资料

### ROS 安装
- 参考链接：https://blog.csdn.net/2302_80099075/article/details/156571786

### Gazebo 仿真环境安装
- 参考链接：https://blog.csdn.net/Jenniehubby/article/details/134780066

---

## 一、仿真环境启动

### 1. 基础仿真启动
启动带有引导控制的 Gazebo 仿真环境：
```bash
roslaunch unitree_guide gazeboSim.launch
```

### 2. 控制器启动
在另一个终端中启动控制器：

**方法1：使用编译后的控制器**
```bash
./devel/lib/unitree_guide/junior_ctrl
```

**方法2：使用标准控制器**
```bash
rosrun unitree_controller unitree_servo
```

### 3. 基础控制操作
启动控制器后，机器人会躺在仿真环境中。按以下键位控制：

| 按键 | 功能说明 |
|------|----------|
| `2` | 从 Passive 状态切换到 FixedStand 状态 |
| `4` | 从 FixedStand 状态切换到 Trotting 状态 |
| `WASD` | 控制机器人平移 |
| `J` `L` | 控制机器人旋转 |
| `空格键` | 停止并站立 |

---

## 二、任务运行命令

### 任务 1：基础 ROS 控制
```bash
# 启动 roscore
roscore

# 启动小乌龟仿真器
rosrun turtlesim turtlesim_node

# 启动键盘控制
rosrun turtlesim turtle_teleop_key
```

### 任务 2：机器狗基础控制
```bash
# （根据具体任务内容填写命令）
# 请在此处添加任务2的具体运行命令
```

### 任务 3：圆形轨迹运动
```bash
# 启动仿真环境
roslaunch unitree_guide gazeboSim.launch

# 启动控制器
./devel/lib/unitree_guide/junior_ctrl

# 运行圆形轨迹脚本
./scripts/round.py
```

### 任务 4：红色方块跟踪
```bash
# 启动仿真环境
roslaunch unitree_guide gazeboSim.launch

# 启动控制器
./devel/lib/unitree_guide/junior_ctrl

# 运行红色方块跟踪脚本
./scripts/red_box_track.py
```

---

## 三、目录结构说明

```
项目根目录/
├── devel/
│   └── lib/
│       └── unitree_guide/
│           └── junior_ctrl      # 控制器可执行文件
├── scripts/
│   ├── round.py                # 圆形轨迹脚本
│   └── red_box_track.py        # 红色方块跟踪脚本
└── src/
    └── unitree_guide/
        └── launch/
            └── gazeboSim.launch  # 仿真启动文件
```

---

## 四、注意事项

1. **终端管理**：每个命令都需要在单独的终端中运行
2. **启动顺序**：
   - 先启动仿真环境 (`gazeboSim.launch`)
   - 再启动控制器 (`junior_ctrl`)
   - 最后运行任务脚本
3. **权限问题**：确保脚本文件具有执行权限
   ```bash
   chmod +x ./scripts/*.py
   ```
4. **依赖检查**：运行前确保所有 ROS 包已正确编译
   ```bash
   catkin_make
   source devel/setup.bash
   ```

---

## 五、故障排除

### 常见问题 1：无法找到启动文件
```bash
# 确保已 source 环境
source devel/setup.bash
```

### 常见问题 2：控制器无响应
- 检查是否已按 `2` 切换到 FixedStand 状态
- 检查是否已按 `4` 切换到 Trotting 状态

### 常见问题 3：脚本无法执行
```bash
# 检查 Python 环境
python3 --version

# 检查脚本权限
ls -la ./scripts/

# 安装缺失的 Python 包
pip install rospkg numpy opencv-python
```

---

**文档版本：** v1.0  
**更新日期：** 2024年1月