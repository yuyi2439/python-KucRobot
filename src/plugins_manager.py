import os
import pkgutil
import inspect
from error import MsgTypeError, NoMsg, NoMsgId
from utils import get_logger
from plugin_base import Utils


class PluginManager:
    """
    该类会通过传入的package查找继承了Plugin类的插件类
    """

    def __init__(self):
        self.plugins = []
        self.logger = get_logger('plugins_manager')
        self.reload_plugins()

    def reload_plugins(self):
        """
        重置plugins列表，遍历传入的package查询有效的插件
        """
        self.logger.info('加载plugins中')
        self.plugins = []
        self.walk_package()
        self.logger.info('plugins加载成功')

    def walk_package(self):
        """
        递归遍历plugins包里获取所有的插件
        """
        imported_package = __import__('plugins', fromlist=['blah'])
        for _, plugin_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not is_pkg:
                plugin_module = __import__(plugin_name, fromlist=['blah'])
                cls_members = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in cls_members:
                # 加载插件
                    if not c().name or not c().version or not c().author or not c().description:
                        self.logger.warning(f'加载插件类失败(插件信息未完全定义): {c.__module__}.{c.__name__}')
                        continue
                    # 检查插件目录
                    plugin_dir = f'./plugins/{c().name}/'
                    if not os.path.isdir(plugin_dir):
                        os.mkdir(plugin_dir)
                    # 执行插件初始化
                    ret = c().on_load(Utils)
                    if ret == 0:
                        self.plugins.append(c())
                        self.logger.info(f'加载插件类成功: {c.__module__}.{c.__name__}:{c().version}')
                    elif ret == -1:
                        self.logger.warning(f'加载插件类失败(插件启动事件未成功): {c.__module__}.{c.__name__}:{c().version}')


    def msg_event(self, msg_type, **kwargs):
        for plugin in self.plugins:
            try:
                os.chdir(f'./plugins/{plugin.name}/')
                # 根据msg_type判断使用哪个方法
                if msg_type == 'group':
                    try:
                        kwargs['reply_msg_id']
                    except KeyError:
                        kwargs['reply_msg_id'] = 0
                    plugin.group_msg_event(Utils, kwargs['sub_type'], kwargs['msg_id'], kwargs['user_id'], kwargs['msg'], kwargs['group_id'], kwargs['anonymous'], kwargs['reply_msg_id'])
                elif msg_type == 'private':
                    if kwargs['sub_type'] == 'group':
                        plugin.private_msg_event(Utils, kwargs['sub_type'], kwargs['msg_id'], kwargs['user_id'], kwargs['msg'], kwargs['temp_source'])
                    else:
                        plugin.private_msg_event(Utils, kwargs['sub_type'], kwargs['msg_id'], kwargs['user_id'], kwargs['msg'])
                else:
                    raise MsgTypeError
            except NoMsg:
                pass
            except NoMsgId:
                pass
            except MsgTypeError as e:
                self.logger.warning(f'消息类型错误: {e}, msg_type: {msg_type}')
            except Exception as e:
                self.logger.error(f'执行插件 {plugin.name} 时出错: {e}')
            finally:
                os.chdir(f'../../')