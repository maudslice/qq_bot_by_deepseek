from typing import Optional
from config.config import Config, RoleConfig

class PromptManager:
    """提示词管理器"""
    
    def __init__(self):
        """初始化提示词管理器"""
        self.config = Config()
        self._current_role: str = "default"
    
    @property
    def current_role(self) -> RoleConfig:
        """获取当前角色配置"""
        return self.config.roles[self._current_role]
    
    def switch_role(self, role_id: str) -> Optional[RoleConfig]:
        """
        切换角色
        
        Args:
            role_id (str): 角色ID
            
        Returns:
            Optional[RoleConfig]: 切换后的角色配置，如果角色不存在则返回 None
        """
        if role_id in self.config.roles:
            self._current_role = role_id
            return self.current_role
        return None
    
    def get_chat_prompt(self) -> str:
        """
        获取当前角色的聊天提示词
        
        Returns:
            str: 提示词内容
        """
        return self.current_role.prompt
    
    def list_roles(self) -> dict:
        """
        获取所有可用角色列表
        
        Returns:
            dict: 角色ID和名称的映射
        """
        return {role_id: role.name for role_id, role in self.config.roles.items()} 