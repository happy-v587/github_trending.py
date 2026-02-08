# GitHub Trending Tool 快速开始

## 1. 安装依赖

```bash
# 使用pip安装
pip3 install requests beautifulsoup4 pandas lxml

# 或者使用conda
conda install requests beautifulsoup4 pandas lxml
```

## 2. 基本使用

```bash
# 查看帮助
python3 github_trending.py --help

# 获取今日热门项目（默认显示10个）
python3 github_trending.py

# 获取Python热门项目
python3 github_trending.py --language python

# 获取本周热门项目
python3 github_trending.py --since weekly

# 显示更多项目
python3 github_trending.py --limit 20
```

## 3. 输出示例

运行 `python3 github_trending.py` 会输出类似以下内容：

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
```

## 4. 高级功能

### 导出数据
```bash
# 导出为CSV
python3 github_trending.py --export csv

# 导出为JSON
python3 github_trending.py --export json

# 同时导出两种格式
python3 github_trending.py --export both
```

### 脚本集成
```bash
# 安静模式，输出JSON格式（适合脚本处理）
python3 github_trending.py --quiet > trending.json

# 然后可以用其他工具处理
cat trending.json | jq '.[0].name'  # 获取第一个项目名称
```

### 缓存控制
```bash
# 强制刷新（不使用缓存）
python3 github_trending.py --no-cache

# 显示所有项目（不限制数量）
python3 github_trending.py --all
```

## 5. 作为Python模块使用

```python
from github_trending import GitHubTrending

# 创建实例
trending = GitHubTrending()

# 获取数据
projects = trending.fetch_trending(language="python")

# 处理数据
for project in projects[:5]:
    print(f"{project['name']}: {project['stars_today']} stars today")

# 导出数据
trending.export_to_csv(projects, "python_trending.csv")
```

## 6. 常见问题

### 问题：ModuleNotFoundError: No module named 'requests'
**解决**：安装依赖
```bash
pip3 install requests beautifulsoup4 pandas lxml
```

### 问题：网络连接失败
**解决**：
1. 检查网络连接
2. 使用 `--no-cache` 参数
3. 如果之前成功过，工具会自动使用缓存

### 问题：输出乱码
**解决**：确保终端支持UTF-8编码

## 7. 一键安装脚本

```bash
# 运行安装脚本
python3 setup.py

# 安装脚本会：
# 1. 检查Python版本
# 2. 安装依赖
# 3. 设置执行权限
# 4. 可选创建全局命令
```

## 8. 文件说明

- `github_trending.py` - 主程序
- `requirements.txt` - 依赖列表
- `config.py` - 配置文件
- `README.md` - 详细文档
- `setup.py` - 安装脚本
- `test_tool.py` - 测试脚本

## 9. 获取帮助

```bash
# 查看完整帮助
python3 github_trending.py --help

# 查看README
cat README.md

# 查看配置选项
cat config.py
```