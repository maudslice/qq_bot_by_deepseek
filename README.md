# QQ Bot with DeepSeek

一个基于 DeepSeek API 的智能 QQ 聊天机器人，使用 graia-ariadne 框架开发。

## 功能特点

- 支持群聊和私聊
- 多角色切换系统
- 基于 DeepSeek API 的智能对话
- 灵活的配置系统
- 权限管理系统

## 安装部署

1. 克隆项目
```bash
git clone [repository_url]
cd qq_bot_by_deepseek
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置文件
- 复制配置文件模板并修改
- 修改 `config.yaml` 中的配置：
  - QQ 机器人账号信息
  - DeepSeek API 密钥
  - 允许使用的群组
  - 管理员列表
- 根据需要修改 `prompts.yaml` 中的角色设定

4. 启动机器人
```bash
python app/bot.py
```

## 指令说明

### 管理员指令
以下指令仅限管理员使用：

1. 查看角色列表 
```

### 普通对话
- 群聊中：@机器人 或包含机器人名字
- 私聊：直接发送消息（仅限管理员）

## 配置文件说明

### config.yaml
```yaml
qq:
  bot_id: 你的机器人QQ号
  verify_key: "mirai-api-http的验证密钥"
  http_host: "http://localhost:8080"
  ws_host: "ws://localhost:8080"
  bot_name: "小助手"
  allowed_groups: [群号1, 群号2]  # 允许使用的群号列表
  admin_users: [QQ号1, QQ号2]     # 管理员QQ号列表
  commands:
    switch_role: ["切换", "/role", "切换角色"]  # 角色切换指令

deepseek:
  api_key: "你的DeepSeek API密钥"
  base_url: "https://api.deepseek.com"
  model_name: "deepseek-reasoner"
```

### prompts.yaml
```yaml
roles:
  default:
    name: "默认助手"
    description: "友善的聊天助手"
    prompt: |
      你是一个友善的聊天助手...

  teacher:
    name: "教师"
    description: "耐心的教育者"
    prompt: |
      你是一位经验丰富的教师...

  programmer:
    name: "程序员"
    description: "专业的代码专家"
    prompt: |
      你是一位资深程序员...
```

## 注意事项

1. 安全性
   - 不要将包含敏感信息的配置文件提交到代码仓库
   - 确保只有可信的管理员有权限使用管理指令

2. 使用限制
   - 注意 DeepSeek API 的使用限制和计费
   - 建议在配置文件中设置合理的群组白名单

3. 部署要求
   - 需要 Python 3.8 或更高版本
   - 需要正确配置并运行 mirai-api-http
