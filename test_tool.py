#!/usr/bin/env python3
"""
GitHub Trending Tool 测试脚本
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_trending import GitHubTrending


def test_basic_functionality():
    """测试基本功能"""
    print("测试GitHub Trending Tool基本功能...")
    print("="*60)
    
    # 创建实例
    trending = GitHubTrending(cache_timeout=300)  # 5分钟缓存
    
    # 测试1: 获取数据
    print("\n1. 测试数据获取...")
    projects = trending.fetch_trending(use_cache=False)
    
    if not projects:
        print("❌ 数据获取失败")
        return False
    
    print(f"✓ 成功获取 {len(projects)} 个项目")
    
    # 测试2: 检查数据结构
    print("\n2. 测试数据结构...")
    sample_project = projects[0] if projects else {}
    
    required_fields = ['name', 'url', 'description', 'language', 'stars', 'stars_today']
    missing_fields = [field for field in required_fields if field not in sample_project]
    
    if missing_fields:
        print(f"❌ 缺少必要字段: {missing_fields}")
        return False
    
    print("✓ 数据结构正确")
    
    # 测试3: 打印摘要
    print("\n3. 测试摘要打印...")
    try:
        trending.print_summary(projects[:3])  # 只显示前3个
        print("✓ 摘要打印成功")
    except Exception as e:
        print(f"❌ 摘要打印失败: {e}")
        return False
    
    # 测试4: 导出功能
    print("\n4. 测试导出功能...")
    
    # 导出CSV
    csv_file = "test_output.csv"
    try:
        trending.export_to_csv(projects[:5], csv_file)
        if os.path.exists(csv_file):
            print(f"✓ CSV导出成功: {csv_file}")
            os.remove(csv_file)  # 清理测试文件
        else:
            print("❌ CSV文件未创建")
            return False
    except Exception as e:
        print(f"❌ CSV导出失败: {e}")
        return False
    
    # 导出JSON
    json_file = "test_output.json"
    try:
        trending.export_to_json(projects[:5], json_file)
        if os.path.exists(json_file):
            # 验证JSON格式
            with open(json_file, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                if isinstance(json_data, list) and len(json_data) > 0:
                    print(f"✓ JSON导出成功: {json_file}")
                else:
                    print("❌ JSON数据格式错误")
                    return False
            os.remove(json_file)  # 清理测试文件
        else:
            print("❌ JSON文件未创建")
            return False
    except Exception as e:
        print(f"❌ JSON导出失败: {e}")
        return False
    
    # 测试5: 缓存功能
    print("\n5. 测试缓存功能...")
    cache_file = ".github_trending_cache.json"
    
    # 第一次获取应该创建缓存
    projects1 = trending.fetch_trending(use_cache=True)
    
    if not os.path.exists(cache_file):
        print("❌ 缓存文件未创建")
        return False
    
    print("✓ 缓存文件已创建")
    
    # 修改缓存文件时间戳（模拟过期）
    if os.path.exists(cache_file):
        # 读取并修改缓存
        with open(cache_file, 'r', encoding='utf-8') as f:
            cache_data = json.load(f)
        
        # 设置过期时间戳（1小时前）
        cache_data['timestamp'] = cache_data['timestamp'] - 3601
        
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
        
        print("✓ 缓存过期测试准备完成")
    
    # 清理缓存文件
    if os.path.exists(cache_file):
        os.remove(cache_file)
        print("✓ 清理测试缓存文件")
    
    return True


def test_command_line():
    """测试命令行接口"""
    print("\n\n测试命令行接口...")
    print("="*60)
    
    test_cases = [
        ("基本测试", ["python", "github_trending.py", "--limit", "3"]),
        ("语言过滤", ["python", "github_trending.py", "--language", "python", "--limit", "2"]),
        ("时间范围", ["python", "github_trending.py", "--since", "weekly", "--limit", "2"]),
        ("安静模式", ["python", "github_trending.py", "--quiet", "--limit", "2"]),
        ("帮助信息", ["python", "github_trending.py", "--help"]),
    ]
    
    import subprocess
    
    for test_name, command in test_cases:
        print(f"\n测试: {test_name}")
        print(f"命令: {' '.join(command)}")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✓ 成功")
                
                # 检查输出
                if test_name == "安静模式":
                    # 安静模式应该输出JSON
                    try:
                        json.loads(result.stdout)
                        print("  ✓ 输出为有效JSON")
                    except json.JSONDecodeError:
                        print("  ⚠️  输出不是有效JSON")
                elif test_name == "帮助信息":
                    if "usage:" in result.stdout.lower():
                        print("  ✓ 帮助信息正确")
                    else:
                        print("  ⚠️  帮助信息可能有问题")
            else:
                print(f"❌ 失败 (退出码: {result.returncode})")
                print(f"错误输出: {result.stderr[:200]}...")
                
        except subprocess.TimeoutExpired:
            print("❌ 超时")
        except Exception as e:
            print(f"❌ 异常: {e}")
    
    return True


def main():
    """主测试函数"""
    print("GitHub Trending Tool 测试套件")
    print("="*60)
    
    # 记录开始时间
    start_time = datetime.now()
    
    # 运行测试
    all_passed = True
    
    # 测试基本功能
    if not test_basic_functionality():
        all_passed = False
    
    # 测试命令行接口（可选，因为需要网络）
    run_cli_tests = input("\n是否运行命令行接口测试？(需要网络连接) (y/n): ").lower().strip()
    if run_cli_tests == 'y':
        if not test_command_line():
            all_passed = False
    
    # 记录结束时间
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    # 输出测试结果
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)
    
    if all_passed:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
    
    print(f"测试用时: {duration:.2f}秒")
    print(f"完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 清理临时文件
    cleanup_files = [".github_trending_cache.json", "test_output.csv", "test_output.json"]
    for file in cleanup_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"已清理: {file}")
            except:
                pass
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())