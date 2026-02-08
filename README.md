# GitHub Trending Tool

一个用于获取GitHub热门项目的Python工具，基于我之前为你获取GitHub趋势项目的操作流程。

## 功能特性

- 📊 获取GitHub今日/本周/本月热门项目
- 🔤 支持按编程语言过滤
- 💾 自动缓存机制，避免频繁请求
- 📈 多种输出格式：控制台表格、JSON、CSV
- 📝 详细的项目信息：描述、语言、星标数、Fork数
- ⚡ 快速响应，支持安静模式

## 安装

### 1. 克隆或下载工具
```bash
git clone <repository-url>
cd github-trending-tool
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

或者直接安装：
```bash
pip install requests beautifulsoup4 pandas lxml
```

### 3. 设置执行权限（可选）
```bash
chmod +x github_trending.py
```

## 使用方法

### 基本使用
```bash
# 获取今日热门项目（默认显示10个）
python github_trending.py

# 获取Python项目
python github_trending.py --language python

# 获取本周热门项目
python github_trending.py --since weekly

# 显示20个项目
python github_trending.py --limit 20
```

### 高级选项
```bash
# 导出为CSV文件
python github_trending.py --export csv

# 导出为JSON文件
python github_trending.py --export json

# 同时导出CSV和JSON
python github_trending.py --export both

# 不使用缓存（强制刷新）
python github_trending.py --no-cache

# 显示所有项目
python github_trending.py --all

# 安静模式（只输出JSON，适合脚本调用）
python github_trending.py --quiet
```

### 作为模块使用
```python
from github_trending import GitHubTrending

# 创建实例
trending = GitHubTrending()

# 获取数据
projects = trending.fetch_trending(language="python", since="daily")

# 打印摘要
trending.print_summary(projects, limit=10)

# 导出数据
trending.export_to_csv(projects, "python_trending.csv")
trending.export_to_json(projects, "python_trending.json")
```

## 输出示例

```
================================================================================
GitHub热门项目 (2026-02-08 14:30:00)
================================================================================

 1. obra/superpowers
    📝 An agentic skills framework & software development methodology that works.
    🔤 语言: Shell
    ⭐ 总星标: 47,030 | 今日新增: 47,030
    🍴 Fork数: 1,234
    🔗 https://github.com/obra/superpowers

 2. composiohq/awesome-claude-skills
    📝 A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI workflows
    🔤 语言: Python
    ⭐ 总星标: 32,056 | 今日新增: 32,056
    🍴 Fork数: 567
    🔗 https://github.com/composiohq/awesome-claude-skills

...

================================================================================
📊 统计信息:
    • 总项目数: 25
    • 热门语言: Python(8), JavaScript(5), Go(4), Rust(3), TypeScript(3)
    • 今日最火: obra/superpowers (+47,030⭐)
================================================================================
```

## 项目结构

```
github-trending-tool/
├── github_trending.py    # 主程序
├── requirements.txt      # 依赖文件
├── config.py            # 配置文件
├── README.md            # 说明文档
└── .github_trending_cache.json  # 缓存文件（自动生成）
```

## 配置说明

编辑 `config.py` 文件可以修改以下配置：

- `CACHE_TIMEOUT`: 缓存超时时间（秒）
- `REQUEST_TIMEOUT`: 请求超时时间
- `DEFAULT_LIMIT`: 默认显示项目数量
- `SUPPORTED_LANGUAGES`: 支持的语言列表

## 技术细节

### 数据来源
工具从 GitHub Trending 页面 (https://github.com/trending) 抓取数据。

### 缓存机制
- 默认缓存1小时，避免频繁请求GitHub
- 缓存文件：`.github_trending_cache.json`
- 可以使用 `--no-cache` 参数强制刷新

### 错误处理
- 网络错误时自动使用缓存数据
- 解析错误时跳过问题项目
- 请求失败时提供友好的错误信息

## 常见问题

### Q: 获取数据失败怎么办？
A: 检查网络连接，或使用 `--no-cache` 参数强制刷新。

### Q: 如何获取特定语言的项目？
A: 使用 `--language` 参数，如 `--language python`。

### Q: 数据不准确怎么办？
A: GitHub Trending 页面有时会有延迟，可以等待几分钟后重试。

### Q: 如何集成到其他脚本中？
A: 使用安静模式：`python github_trending.py --quiet` 输出JSON格式。

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0 (2026-02-08)
- 初始版本发布
- 支持基本的热门项目获取
- 添加缓存机制
- 支持多种输出格式