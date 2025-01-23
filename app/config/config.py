from typing import Optional, Dict
import yaml
from pathlib import Path
from dataclasses import dataclass

@dataclass
class RoleConfig:
    """角色配置类"""
    name: str
    description: str
    prompt: str

@dataclass
class Config:
    """配置类"""
    
    def __init__(self):
        self.reload()
    
    def reload(self) -> None:
        """重新加载所有配置文件"""
        config_path = Path(__file__).parent / "config.yaml"
        prompts_path = Path(__file__).parent / "prompts.yaml"
        
        # 加载主配置
        with open(config_path, "r", encoding="utf-8") as f:
            config_data = yaml.safe_load(f)
            
        # 加载提示词配置
        with open(prompts_path, "r", encoding="utf-8") as f:
            prompts_data = yaml.safe_load(f)
            
        # Mirai 配置
        self.qq_id: int = config_data["qq"]["bot_id"]
        self.verify_key: str = config_data["qq"]["verify_key"]
        self.http_host: str = config_data["qq"]["http_host"]
        self.ws_host: str = config_data["qq"]["ws_host"]
        self.bot_name: str = config_data["qq"]["bot_name"]
        self.allowed_groups: list[int] = config_data["qq"]["allowed_groups"]
        self.admin_users: list[int] = config_data["qq"]["admin_users"]
        self.commands: dict[str, list[str]] = config_data["qq"]["commands"]
        
        # DeepSeek 配置
        self.deepseek_api_key: str = config_data["deepseek"]["api_key"]
        self.deepseek_base_url: str = config_data["deepseek"]["base_url"]
        self.model_name: str = config_data["deepseek"]["model_name"]
        
        # 角色配置
        self.roles: Dict[str, RoleConfig] = {}
        for role_id, role_data in prompts_data["roles"].items():
            self.roles[role_id] = RoleConfig(
                name=role_data["name"],
                description=role_data["description"],
                prompt=role_data["prompt"]
            ) 