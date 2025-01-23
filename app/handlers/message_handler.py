from typing import Optional, Tuple
from openai import OpenAI
from loguru import logger

from config.config import Config
from models.prompt_templates import PromptManager

class MessageHandler:
    """消息处理器类"""
    
    def __init__(self):
        """初始化消息处理器"""
        self.config = Config()
        self.prompt_manager = PromptManager()
        self.client = OpenAI(
            api_key=self.config.deepseek_api_key,
            base_url=self.config.deepseek_base_url
        )
    
    def _clean_message(self, message: str) -> str:
        """
        清理消息内容，去除@信息等
        
        Args:
            message (str): 原始消息
            
        Returns:
            str: 清理后的消息
        """
        # 移除@机器人的信息
        message = message.replace(f"@{self.config.qq_id}", "").strip()
        # 移除机器人名称
        message = message.replace(self.config.bot_name, "").strip()
        return message

    def _parse_command(self, message: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        解析命令
        
        Args:
            message (str): 消息内容
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: 
                (是否是命令, 命令类型, 命令参数)
        """
        # 首先清理消息内容
        cleaned_message = self._clean_message(message)
        
        # 检查重载配置命令
        if cleaned_message.strip() == "/reload":
            return True, "reload", None
            
        # 检查角色切换命令
        for cmd_prefix in self.config.commands["switch_role"]:
            if cleaned_message.startswith(cmd_prefix):
                # 移除命令前缀，获取参数
                param = cleaned_message[len(cmd_prefix):].strip()
                if param:  # 有参数
                    return True, "role", param
                return True, "role", None  # 无参数
                
        return False, None, None
    
    def _check_group_permission(self, group_id: int) -> bool:
        """检查群聊权限"""
        return group_id in self.config.allowed_groups
    
    def _check_admin_permission(self, user_id: int) -> bool:
        """检查管理员权限"""
        return user_id in self.config.admin_users
    
    async def handle_message(self, message: str, sender_id: int, group_id: Optional[int] = None) -> Optional[str]:
        """
        处理接收到的消息
        
        Args:
            message (str): 接收到的消息内容
            sender_id (int): 发送者ID
            group_id (Optional[int]): 群ID，如果是群消息的话
            
        Returns:
            Optional[str]: 响应消息，如果不需要回复则返回 None
        """
        try:
            # 检查群权限
            if group_id is not None and not self._check_group_permission(group_id):
                return None
            
            # 检查是否是命令
            is_command, cmd_type, cmd_arg = self._parse_command(message)
            
            if is_command:
                # 检查管理员权限
                if not self._check_admin_permission(sender_id):
                    return "抱歉，只有管理员才能使用命令哦~"
                
                if cmd_type == "reload":
                    # 重载配置
                    try:
                        self.config.reload()
                        # 重新初始化 prompt_manager 以加载新的角色配置
                        self.prompt_manager = PromptManager()
                        return "配置重载成功！"
                    except Exception as e:
                        logger.error(f"重载配置时发生错误: {str(e)}")
                        return f"配置重载失败: {str(e)}"
                        
                elif cmd_type == "role":
                    if cmd_arg is None:
                        # 显示当前角色和可用角色列表
                        roles = self.prompt_manager.list_roles()
                        current = self.prompt_manager.current_role
                        return f"当前角色：{current.name}\n可用角色：\n" + \
                               "\n".join(f"- {role_id}: {name}" for role_id, name in roles.items())
                    
                    # 切换角色
                    new_role = self.prompt_manager.switch_role(cmd_arg)
                    if new_role:
                        return f"已切换至角色：{new_role.name}\n{new_role.description}"
                    return f"未知角色：{cmd_arg}"
            
            # 如果不是命令，才进行普通对话
            return await self._handle_chat(message)
            
        except Exception as e:
            logger.error(f"处理消息时发生错误: {str(e)}")
            return "抱歉，我现在有点累，请稍后再试~"
    
    async def _handle_chat(self, message: str) -> str:
        """处理普通对话"""
        # 获取当前角色的系统提示词
        system_prompt = self.prompt_manager.get_chat_prompt()
        
        # 调用 DeepSeek API
        response = self.client.chat.completions.create(
            model=self.config.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            stream=False
        )
        
        return response.choices[0].message.content 