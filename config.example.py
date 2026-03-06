# 配置文件模板
# 使用方法：
# 1. 复制本文件为 config.py
# 2. 填入你的真实API密钥
# 3. 确保 config.py 在 .gitignore 中，不要上传到GitHub

# EvoMap API配置
EVOMAP_API_KEY = "your_evomap_api_key_here"
EVOMAP_NODE_ID = "your_node_id_here"

# OpenAI/Kimi API配置
OPENAI_API_KEY = "your_openai_api_key_here"
KIMI_API_KEY = "your_kimi_api_key_here"

# Telegram Bot配置（如果使用）
TELEGRAM_BOT_TOKEN = "your_telegram_bot_token_here"
TELEGRAM_CHAT_ID = "your_chat_id_here"

# 其他API密钥
# 根据需要添加其他服务的API密钥

# 系统配置
DEBUG = False
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# 监控配置
CHECK_INTERVAL_MINUTES = 5  # 检查间隔
HEARTBEAT_TIMEOUT_MINUTES = 30  # 心跳超时
