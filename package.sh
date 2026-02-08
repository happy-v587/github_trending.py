#!/bin/bash
# GitHub Trending Tool 打包脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 函数：打印带颜色的消息
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否在正确的目录
check_directory() {
    if [ ! -f "github_trending.py" ]; then
        print_error "请在包含 github_trending.py 的目录中运行此脚本"
        exit 1
    fi
    print_info "检查目录... ✓"
}

# 清理之前的构建
clean_previous_builds() {
    print_info "清理之前的构建..."
    rm -rf build/ dist/ *.egg-info/ 2>/dev/null || true
    rm -f github_trending_tool*.tar.gz github_trending_tool*.zip 2>/dev/null || true
}

# 创建发布目录结构
create_release_structure() {
    print_info "创建发布目录结构..."
    
    RELEASE_DIR="github-trending-tool-$(date +%Y%m%d)"
    rm -rf "$RELEASE_DIR" 2>/dev/null || true
    mkdir -p "$RELEASE_DIR"
    
    # 复制必要文件
    cp github_trending.py "$RELEASE_DIR/"
    cp requirements.txt "$RELEASE_DIR/"
    cp config.py "$RELEASE_DIR/"
    cp README.md "$RELEASE_DIR/"
    cp QUICK_START.md "$RELEASE_DIR/"
    cp setup.py "$RELEASE_DIR/"
    
    # 创建示例脚本
    cat > "$RELEASE_DIR/example.py" << 'EOF'
#!/usr/bin/env python3
"""
GitHub Trending Tool 使用示例
"""

from github_trending import GitHubTrending

def main():
    # 创建趋势获取器
    trending = GitHubTrending()
    
    print("获取GitHub今日热门项目...")
    
    # 获取数据
    projects = trending.fetch_trending()
    
    if not projects:
        print("无法获取数据")
        return
    
    print(f"\n成功获取 {len(projects)} 个项目")
    
    # 显示前5个项目
    print("\n今日最热门的5个项目:")
    print("="*80)
    
    for i, project in enumerate(projects[:5], 1):
        print(f"{i}. {project['name']}")
        print(f"   描述: {project['description'][:80]}...")
        print(f"   语言: {project['language']}")
        print(f"   今日星标: {project['stars_today']:,}")
        print()
    
    # 统计信息
    languages = {}
    for project in projects:
        lang = project['language']
        languages[lang] = languages.get(lang, 0) + 1
    
    top_lang = max(languages.items(), key=lambda x: x[1])
    print(f"最流行的语言: {top_lang[0]} ({top_lang[1]}个项目)")

if __name__ == "__main__":
    main()
EOF
    
    chmod +x "$RELEASE_DIR/example.py"
    
    # 创建安装脚本
    cat > "$RELEASE_DIR/install.sh" << 'EOF'
#!/bin/bash
# GitHub Trending Tool 一键安装脚本

echo "GitHub Trending Tool 安装程序"
echo "=============================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要Python3，请先安装Python3"
    exit 1
fi

echo "Python3 已安装 ✓"

# 安装依赖
echo "安装依赖..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "依赖安装完成 ✓"
else
    echo "依赖安装失败，尝试使用pip..."
    pip install -r requirements.txt
fi

# 设置执行权限
chmod +x github_trending.py
chmod +x example.py

echo ""
echo "安装完成！"
echo ""
echo "使用方法:"
echo "  ./github_trending.py                 # 获取今日热门"
echo "  python3 github_trending.py --help    # 查看帮助"
echo "  ./example.py                         # 运行示例"
echo ""
echo "详细文档请查看 README.md"
EOF
    
    chmod +x "$RELEASE_DIR/install.sh"
    
    print_info "发布目录创建完成: $RELEASE_DIR"
}

# 创建压缩包
create_archives() {
    print_info "创建压缩包..."
    
    RELEASE_DIR="github-trending-tool-$(date +%Y%m%d)"
    
    # 创建tar.gz
    tar -czf "${RELEASE_DIR}.tar.gz" "$RELEASE_DIR"
    print_info "创建: ${RELEASE_DIR}.tar.gz"
    
    # 创建zip
    zip -rq "${RELEASE_DIR}.zip" "$RELEASE_DIR"
    print_info "创建: ${RELEASE_DIR}.zip"
    
    # 计算文件大小
    tar_size=$(du -h "${RELEASE_DIR}.tar.gz" | cut -f1)
    zip_size=$(du -h "${RELEASE_DIR}.zip" | cut -f1)
    
    print_info "压缩包大小: tar.gz=$tar_size, zip=$zip_size"
}

# 创建PyPI包（可选）
create_pypi_package() {
    if command -v python3 &> /dev/null; then
        print_info "创建PyPI包..."
        
        # 创建setup.cfg
        cat > setup.cfg << 'EOF'
[metadata]
name = github-trending-tool
version = 1.0.0
author = GitHub Trending Tool
author_email = example@example.com
description = A tool to fetch GitHub trending projects
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/example/github-trending-tool
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
packages = find:
python_requires = >=3.7
install_requires =
    requests>=2.28.0
    beautifulsoup4>=4.11.0
    pandas>=1.5.0
    lxml>=4.9.0

[options.entry_points]
console_scripts =
    github-trending = github_trending:main

[options.packages.find]
exclude = tests*, examples*

[egg_info]
tag_build = 
tag_date = 0
EOF
        
        # 创建MANIFEST.in
        cat > MANIFEST.in << 'EOF'
include *.py
include *.md
include *.txt
include *.sh
EOF
        
        # 构建包
        python3 -m build 2>/dev/null || python3 setup.py sdist bdist_wheel
        
        if [ $? -eq 0 ]; then
            print_info "PyPI包创建完成"
            ls -la dist/
        else
            print_warning "PyPI包创建失败（跳过）"
        fi
        
        # 清理临时文件
        rm -f setup.cfg MANIFEST.in
    else
        print_warning "Python3未找到，跳过PyPI包创建"
    fi
}

# 显示摘要
show_summary() {
    print_info "\n打包完成！"
    print_info "="*50
    
    RELEASE_DIR="github-trending-tool-$(date +%Y%m%d)"
    
    echo "生成的文件:"
    echo "  - ${RELEASE_DIR}.tar.gz"
    echo "  - ${RELEASE_DIR}.zip"
    
    if [ -d "dist" ]; then
        echo "  - dist/*.whl"
        echo "  - dist/*.tar.gz"
    fi
    
    echo ""
    echo "发布目录内容:"
    find "$RELEASE_DIR" -type f | sort
    
    echo ""
    echo "使用方法:"
    echo "  1. 解压: tar -xzf ${RELEASE_DIR}.tar.gz"
    echo "  2. 进入目录: cd ${RELEASE_DIR}"
    echo "  3. 运行安装: ./install.sh"
    echo "  4. 使用工具: ./github_trending.py"
    
    echo ""
    echo "或者直接安装PyPI包:"
    echo "  pip install dist/*.whl"
    echo "  github-trending --help"
}

# 主函数
main() {
    echo "GitHub Trending Tool 打包脚本"
    echo "=============================="
    
    check_directory
    clean_previous_builds
    create_release_structure
    create_archives
    create_pypi_package
    show_summary
}

# 运行主函数
main "$@"
