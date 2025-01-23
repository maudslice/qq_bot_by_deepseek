from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import MatchContent
from graia.ariadne.model import Friend, Group, Member
from loguru import logger
from typing import Union
import asyncio

from config.config import Config
from handlers.message_handler import MessageHandler
from utils.logger import setup_logger

class Bot:
    """QQ聊天机器人主类"""
    
    def __init__(self):
        """初始化机器人实例"""
        self.config = Config()
        setup_logger()
        self.message_handler = MessageHandler()
        
        # 添加详细的配置日志
        logger.info(f"正在连接到 mirai-api-http:")
        logger.info(f"HTTP地址: {self.config.http_host}")
        logger.info(f"WS地址: {self.config.ws_host}")
        logger.info(f"验证密钥: {self.config.verify_key}")
        logger.info(f"机器人QQ: {self.config.qq_id}")
        
        # 初始化 Ariadne
        self.app = Ariadne(
            connection=config(
                self.config.qq_id,  # 机器人的 QQ 号
                self.config.verify_key,  # mirai-api-http 的 verify_key
                HttpClientConfig(host=self.config.http_host),
                WebsocketClientConfig(host=self.config.ws_host),
            ),
        )
        
        self._setup_handlers()
        
    def _setup_handlers(self) -> None:
        """设置消息处理器"""
        
        @self.app.broadcast.receiver("FriendMessage")
        async def friend_message_handler(app: Ariadne, friend: Friend, message: MessageChain):
            """处理好友消息"""
            # 好友消息只允许管理员发送
            if not self.message_handler._check_admin_permission(friend.id):
                return
            response = await self.message_handler.handle_message(message.display, friend.id)
            if response:
                await app.send_message(friend, MessageChain(response))

        @self.app.broadcast.receiver("GroupMessage")
        async def group_message_handler(app: Ariadne, group: Group, member: Member, message: MessageChain):
            """处理群消息"""
            # 检查是否被@或者触发关键词
            if self.config.bot_name in message.display or f"@{self.config.qq_id}" in message.display:
                response = await self.message_handler.handle_message(
                    message.display, 
                    member.id,  # 使用 member.id 获取发送者QQ号
                    group.id    # 群号
                )
                if response:
                    await app.send_message(group, MessageChain(response))

    def run(self):
        """运行机器人"""
        logger.info("Starting QQ Bot...")
        self.app.launch_blocking()

if __name__ == "__main__":
    bot = Bot()
    bot.run() 