"""
GitHub Trending Tool 配置文件
"""

# 缓存配置
CACHE_TIMEOUT = 3600  # 缓存超时时间（秒），默认1小时
CACHE_FILE = ".github_trending_cache.json"

# 请求配置
REQUEST_TIMEOUT = 10  # 请求超时时间（秒）
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# GitHub Trending URL
GITHUB_TRENDING_URL = "https://github.com/trending"

# 输出配置
DEFAULT_LIMIT = 10  # 默认显示项目数量
MAX_DESCRIPTION_LENGTH = 100  # 描述最大长度

# 支持的语言列表（用于自动补全）
SUPPORTED_LANGUAGES = [
    "python", "javascript", "java", "go", "rust", "typescript",
    "c++", "c#", "php", "ruby", "swift", "kotlin", "dart",
    "scala", "haskell", "elixir", "clojure", "erlang", "perl",
    "lua", "r", "matlab", "shell", "powershell", "html", "css"
]

# 时间范围选项
TIME_RANGES = {
    "daily": "今日",
    "weekly": "本周", 
    "monthly": "本月"
}

# 输出格式
OUTPUT_FORMATS = ["table", "json", "csv", "markdown"]