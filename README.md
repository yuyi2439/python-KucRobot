# python-KucRobot

## 一些想法

### 目前已知问题：
1、input函数输入不方便，以后会改成prompt_toolkit库

2、reload plugins指令无法正确重载插件

### 可增加的功能：
1、在@机器人时，由主程序处理消息，可以实现全局菜单、撤回等功能

2、让用户可以给插件设置优先级，按照优先级依次交由插件处理

## 食用(使用)方法

1、下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)并部署

2、clone本项目到本地，进入src目录

3、运行 `python main.py`