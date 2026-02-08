#!/usr/bin/env python3
"""
GitHub Trending Tool 安装脚本
"""

import os
import sys
import subprocess
from pathlib import Path


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        sys.exit(1)
    
    print(f"✓ Python版本: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")


def install_dependencies():
    """安装依赖"""
    print("\n正在安装依赖...")
    
    requirements_file = "requirements.txt"
    if not os.path.exists(requirements_file):
        print(f"错误: 找不到 {requirements_file}")
        sys.exit(1)
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("✓ 依赖安装完成")
    except subprocess.CalledProcessError as e:
        print(f"错误: 依赖安装失败: {e}")
        sys.exit(1)


def make_executable():
    """设置执行权限"""
    script_file = "github_trending.py"
    
    if os.path.exists(script_file):
        try:
            # 在Unix-like系统上设置执行权限
            if os.name != 'nt':  # 不是Windows
                os.chmod(script_file, 0o755)
                print(f"✓ 已设置 {script_file} 为可执行文件")
            
            # 创建符号链接（可选）
            create_symlink = input("\n是否创建全局命令链接？(y/n): ").lower().strip()
            if create_symlink == 'y':
                create_global_command()
        except Exception as e:
            print(f"警告: 无法设置执行权限: {e}")


def create_global_command():
    """创建全局命令"""
    try:
        # 获取用户bin目录
        home = Path.home()
        bin_dir = home / ".local" / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建符号链接
        script_path = Path.cwd() / "github_trending.py"
        link_path = bin_dir / "github-trending"
        
        if link_path.exists():
            overwrite = input(f"{link_path} 已存在，是否覆盖？(y/n): ").lower().strip()
            if overwrite != 'y':
                print("跳过创建全局命令")
                return
        
        # 创建符号链接
        if link_path.is_symlink():
            link_path.unlink()
        
        link_path.symlink_to(script_path)
        
        # 检查PATH
        path_str = os.environ.get('PATH', '')
        if str(bin_dir) not in path_str:
            print(f"\n⚠️  注意: {bin_dir} 不在PATH中")
            print(f"请将以下内容添加到 ~/.bashrc, ~/.zshrc 或 ~/.profile:")
            print(f'export PATH="$HOME/.local/bin:$PATH"')
            print("然后运行: source ~/.bashrc (或对应的shell配置文件)")
        else:
            print(f"✓ 全局命令已创建: github-trending")
            
    except Exception as e:
        print(f"警告: 创建全局命令失败: {e}")
        print("您仍然可以使用 python github_trending.py 运行工具")


def show_usage():
    """显示使用说明"""
    print("\n" + "="*60)
    print("GitHub Trending Tool 安装完成！")
    print("="*60)
    
    print("\n使用方法:")
    print("  1. 直接运行: python github_trending.py")
    print("  2. 如果设置了执行权限: ./github_trending.py")
    print("  3. 如果创建了全局命令: github-trending")
    
    print("\n示例命令:")
    print("  github-trending                          # 获取今日热门")
    print("  github-trending --language python        # 获取Python项目")
    print("  github-trending --since weekly           # 获取本周热门")
    print("  github-trending --export csv             # 导出为CSV")
    
    print("\n查看帮助:")
    print("  github-trending --help")
    
    print("\n详细文档请查看 README.md")


def main():
    """主安装函数"""
    print("GitHub Trending Tool 安装程序")
    print("="*40)
    
    # 检查当前目录
    current_dir = Path.cwd()
    print(f"安装目录: {current_dir}")
    
    # 检查必要文件
    required_files = ["github_trending.py", "requirements.txt", "README.md"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"错误: 缺少必要文件: {', '.join(missing_files)}")
        print("请确保在正确的目录中运行安装程序")
        sys.exit(1)
    
    # 执行安装步骤
    check_python_version()
    install_dependencies()
    make_executable()
    show_usage()


if __name__ == "__main__":
    main()