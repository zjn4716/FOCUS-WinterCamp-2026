# 第一条边（前进3秒）
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.3
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

# 第一个转角（右转1.6秒）
# rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
#   x: 0.0
#   y: 0.0
#   z: 0.0
# angular:
#   x: 0.0
#   y: 0.0
#   z: 0.5"
# sleep 1.6

# 第二条边
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.3
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

# 第二个转角
# rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
#   x: 0.0
#   y: 0.0
#   z: 0.0
# angular:
#   x: 0.0
#   y: 0.0
#   z: 0.5"
# sleep 1.6

# 第三条边
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: -0.3
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

# 第三个转角
# rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
#   x: 0.0
#   y: 0.0
#   z: 0.0
# angular:
#   x: 0.0
#   y: 0.0
#   z: 0.5"
# sleep 1.6

# 第四条边
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: -0.3
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"
sleep 3

# 停止
rostopic pub -1 /cmd_vel geometry_msgs/Twist "linear:
  x: 0.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 0.0"