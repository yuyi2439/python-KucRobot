# 本项目已废弃，请使用[MyDM](https://github.com/yuyi2439/MyDM)

# python-KucRobot

## 一些想法

### 目前已知问题：
* input函数输入不方便，以后会改成prompt_toolkit库
* reload plugins指令无法正确重载插件
* 输出ws连接失败后，不能主动退出进程

### 可增加(修改)的地方：
* 在@机器人时，由主程序处理消息，可以实现全局菜单、撤回等功能
* 让用户可以给插件设置优先级，按照优先级依次交由插件处理
* 将plugin_base专用来声明，各种方法通过参数传进去

## 食用(使用)方法
* 下载[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)并部署(通讯方式选择0和2)
* clone本项目到本地，进入src目录
* 运行 `python main.py`

## 插件编写
* 将plugin_base放在插件所在的文件夹(我用的PyCharm看不懂`sys.path.append('..')`)
* 在插件中引入plugin_base中的Plugin类，创建一个类，使它继承Plugin类
* 类中需要有__init__和start_event函数
* __init__中需要声明self.name和self.version变量，然后`super().__init__()`
