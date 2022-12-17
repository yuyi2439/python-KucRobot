import logging
import os
import pkgutil
import inspect
from plugin_base import Plugin
from main import login_user_id, msg_sender
from error import NoStartEvent, MsgTypeError


class PluginCollection:
    """
    该类会通过传入的package查找继承了Plugin类的插件类
    """

    def __init__(self, plugin_package):
        self.plugins = []
        self.seen_paths = []
        self.plugin_package = plugin_package
        self.logger = logging.getLogger('__main__.plugins_collection')
        self.reload_plugins()

    def reload_plugins(self):
        """
        重置plugins列表，遍历传入的package查询有效的插件
        """
        self.logger.debug(f'加载plugins中')
        self.plugins = []
        self.seen_paths = []
        self.walk_package(self.plugin_package)
        self.logger.info(f'plugins加载成功')

    def walk_package(self, package):
        """
        递归遍历包里获取所有的插件
        """
        imported_package = __import__(package, fromlist=['blah'])
        for _, plugin_name, is_pkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not is_pkg:
                plugin_module = __import__(plugin_name, fromlist=['blah'])
                cls_members = inspect.getmembers(plugin_module, inspect.isclass)
                for (_, c) in cls_members:
                    # 仅加入Plugin类的子类，忽略掉Plugin本身
                    if issubclass(c, Plugin) and (c is not Plugin):
                        # 加载插件
                        if c().name == 'unknown' or c().version == 'unknown':
                            self.logger.warning(
                                f'加载插件类失败(插件名或版本未定义): {c.__module__}.{c.__name__}:{c().version}')
                        plugin_dir = f'./plugins/{c().name}/'
                        if not os.path.isdir(plugin_dir):
                            os.mkdir(plugin_dir)
                        try:
                            c().start_event()
                            self.plugins.append(c())
                            self.logger.info(f'加载插件类成功: {c.__module__}.{c.__name__}:{c().version}')
                        except NoStartEvent:
                            self.logger.warning(
                                f'加载插件类失败(插件无启动事件): {c.__module__}.{c.__name__}:{c().version}')

        # # 现在我们已经查找了当前package中的所有模块，现在我们递归查找子packages里的附件模块
        # all_current_paths = []
        # if isinstance(imported_package.__path__, str):
        #     all_current_paths.append(imported_package.__path__)
        # else:
        #     all_current_paths.extend([x for x in imported_package.__path__])

        # 加载子目录
        # for pkg_path in all_current_paths:
        #     if pkg_path not in self.seen_paths:
        #         self.seen_paths.append(pkg_path)
        #
        #         # 获取当前package中的子目录
        #         child_pkgs = [p for p in os.listdir(pkg_path) if os.path.isdir(os.path.join(pkg_path, p))]
        #
        #         # 递归遍历子目录的package
        #         for child_pkg in child_pkgs:
        #             self.walk_package(package + '.' + child_pkg)

    async def msg_event(self, msg_type, **kwargs):
        try:
            if kwargs['msg'][:13] == '[CQ:reply,id=':
                msg_id = int(kwargs['msg'][13:].split(']')[0])
                kwargs['msg'] = kwargs['msg'].split(f'[CQ:reply,id={msg_id}][CQ:at,qq={login_user_id}] ')[-1]
                try:
                    plugin = msg_sender[msg_id]
                    kwargs['sub_type'] = 'reply'
                    kwargs['reply_msg_id'] = msg_id
                    await self._msg_event(plugin, msg_type, **kwargs)
                except KeyError:
                    pass
            else:
                for plugin in self.plugins:
                    await self._msg_event(plugin, msg_type, **kwargs)
        except MsgTypeError as e:
            self.logger.warning(f'消息类型错误: {e}, msg_type: {msg_type}')

    async def _msg_event(self, plugin, msg_type, **kwargs):
        try:
            os.chdir(f'./plugins/{plugin.name}/')
            # 根据msg_type判断使用哪个方法
            if msg_type == 'group':
                try:
                    kwargs['reply_msg_id']
                except KeyError:
                    kwargs['reply_msg_id'] = 0
                await plugin.group_msg_event(kwargs['sub_type'], kwargs['msg_id'], kwargs['user_id'], kwargs['msg'],
                                             kwargs['group_id'], kwargs['anonymous'], kwargs['reply_msg_id'])
            elif msg_type == 'private':
                if kwargs['sub_type'] == 'group':
                    await plugin.private_msg_event(kwargs['sub_type'], kwargs['msg_id'],
                                                   kwargs['user_id'], kwargs['msg'],
                                                   kwargs['temp_source'])
                else:
                    await plugin.private_msg_event(kwargs['sub_type'], kwargs['msg_id'],
                                                   kwargs['user_id'], kwargs['msg'])
            else:
                raise MsgTypeError
        except Exception as e:
            self.logger.error(f'执行插件 {plugin.name} 时出错: {e}')
        finally:
            os.chdir(f'../../')
