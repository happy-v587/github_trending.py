#!/usr/bin/env python3
"""
GitHub Trending Projects Tool
获取GitHub热门项目的Python工具
"""

import argparse
import json
import sys
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests
from bs4 import BeautifulSoup
import pandas as pd


class GitHubTrending:
    """GitHub趋势项目获取器"""
    
    def __init__(self, cache_timeout: int = 3600):
        """
        初始化GitHub趋势获取器
        
        Args:
            cache_timeout: 缓存超时时间（秒），默认1小时
        """
        self.base_url = "https://github.com/trending"
        self.cache_timeout = cache_timeout
        self.cache_file = ".github_trending_cache.json"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def _load_cache(self) -> Optional[Dict[str, Any]]:
        """加载缓存数据"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
                
            # 检查缓存是否过期
            cache_time = cache_data.get('timestamp', 0)
            current_time = time.time()
            
            if current_time - cache_time < self.cache_timeout:
                return cache_data.get('data')
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return None
    
    def _save_cache(self, data: List[Dict[str, Any]]) -> None:
        """保存数据到缓存"""
        cache_data = {
            'timestamp': time.time(),
            'data': data
        }
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"警告: 缓存保存失败: {e}")
    
    def fetch_trending(self, language: str = "", since: str = "daily", use_cache: bool = True) -> List[Dict[str, Any]]:
        """
        获取GitHub趋势项目
        
        Args:
            language: 编程语言过滤（可选）
            since: 时间范围（daily, weekly, monthly）
            use_cache: 是否使用缓存
            
        Returns:
            项目列表
        """
        # 检查缓存
        if use_cache:
            cached_data = self._load_cache()
            if cached_data:
                print("使用缓存数据...")
                return cached_data
        
        # 构建URL
        url = self.base_url
        params = {}
        
        if language:
            params['l'] = language
        if since:
            params['since'] = since
        
        try:
            print(f"正在获取GitHub趋势数据...")
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            projects = self._parse_projects(soup)
            
            # 保存缓存
            self._save_cache(projects)
            
            return projects
            
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            # 尝试使用缓存
            cached_data = self._load_cache()
            if cached_data:
                print("使用缓存数据...")
                return cached_data
            return []
    
    def _parse_projects(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """解析HTML获取项目信息"""
        projects = []
        
        # 查找项目列表
        articles = soup.find_all('article', class_='Box-row')
        
        for article in articles:
            try:
                # 提取项目名称和链接
                title_elem = article.find('h2', class_='h3')
                if not title_elem:
                    continue
                    
                link_elem = title_elem.find('a')
                if not link_elem:
                    continue
                    
                repo_name = link_elem.get('href', '').strip('/')
                repo_url = f"https://github.com{link_elem.get('href', '')}"
                
                # 提取描述
                desc_elem = article.find('p', class_='col-9')
                description = desc_elem.text.strip() if desc_elem else ""
                
                # 提取编程语言
                lang_elem = article.find('span', itemprop='programmingLanguage')
                language = lang_elem.text.strip() if lang_elem else "Unknown"
                
                # 提取星标数
                stars_elem = article.find('a', href=lambda x: x and 'stargazers' in x)
                stars_text = stars_elem.text.strip() if stars_elem else "0"
                stars = self._parse_number(stars_text)
                
                # 提取今日星标数
                stars_today_elem = article.find('span', class_='d-inline-block float-sm-right')
                stars_today_text = stars_today_elem.text.strip() if stars_today_elem else "0"
                stars_today = self._parse_number(stars_today_text.split()[0] if stars_today_text else "0")
                
                # 提取fork数
                forks_elem = article.find('a', href=lambda x: x and 'forks' in x)
                forks_text = forks_elem.text.strip() if forks_elem else "0"
                forks = self._parse_number(forks_text)
                
                project = {
                    'rank': len(projects) + 1,
                    'name': repo_name,
                    'url': repo_url,
                    'description': description,
                    'language': language,
                    'stars': stars,
                    'stars_today': stars_today,
                    'forks': forks,
                    'timestamp': datetime.now().isoformat()
                }
                
                projects.append(project)
                
            except Exception as e:
                print(f"解析项目时出错: {e}")
                continue
        
        return projects
    
    def _parse_number(self, text: str) -> int:
        """解析数字字符串（处理k、M等单位）"""
        text = text.lower().replace(',', '')
        
        if 'k' in text:
            return int(float(text.replace('k', '')) * 1000)
        elif 'm' in text:
            return int(float(text.replace('m', '')) * 1000000)
        
        try:
            return int(float(text))
        except ValueError:
            return 0
    
    def print_summary(self, projects: List[Dict[str, Any]], limit: int = 10) -> None:
        """打印项目摘要"""
        if not projects:
            print("未找到任何项目")
            return
        
        print(f"\n{'='*80}")
        print(f"GitHub热门项目 ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"{'='*80}")
        
        # 按今日星标数排序
        sorted_projects = sorted(projects, key=lambda x: x['stars_today'], reverse=True)
        
        for i, project in enumerate(sorted_projects[:limit], 1):
            print(f"\n{i:2d}. {project['name']}")
            print(f"    📝 {project['description'][:100]}{'...' if len(project['description']) > 100 else ''}")
            print(f"    🔤 语言: {project['language']}")
            print(f"    ⭐ 总星标: {project['stars']:,} | 今日新增: {project['stars_today']:,}")
            print(f"    🍴 Fork数: {project['forks']:,}")
            print(f"    🔗 {project['url']}")
        
        # 统计信息
        print(f"\n{'='*80}")
        print("📊 统计信息:")
        print(f"    • 总项目数: {len(projects)}")
        
        # 语言分布
        languages = {}
        for project in projects:
            lang = project['language']
            languages[lang] = languages.get(lang, 0) + 1
        
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"    • 热门语言: {', '.join([f'{lang}({count})' for lang, count in top_languages])}")
        
        # 今日最火项目
        if projects:
            top_project = max(projects, key=lambda x: x['stars_today'])
            print(f"    • 今日最火: {top_project['name']} (+{top_project['stars_today']:,}⭐)")
        
        print(f"{'='*80}")
    
    def export_to_csv(self, projects: List[Dict[str, Any]], filename: str = "github_trending.csv") -> None:
        """导出到CSV文件"""
        if not projects:
            print("没有数据可导出")
            return
        
        df = pd.DataFrame(projects)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据已导出到: {filename}")
    
    def export_to_json(self, projects: List[Dict[str, Any]], filename: str = "github_trending.json") -> None:
        """导出到JSON文件"""
        if not projects:
            print("没有数据可导出")
            return
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)
        print(f"数据已导出到: {filename}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='获取GitHub热门项目',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                          # 获取今日热门项目
  %(prog)s --language python        # 获取Python项目
  %(prog)s --since weekly           # 获取本周热门
  %(prog)s --limit 20               # 显示20个项目
  %(prog)s --export csv             # 导出为CSV
  %(prog)s --no-cache               # 不使用缓存
  %(prog)s --all                    # 显示所有项目
        """
    )
    
    parser.add_argument('--language', '-l', type=str, default='',
                       help='编程语言过滤 (如: python, javascript, go)')
    parser.add_argument('--since', '-s', type=str, default='daily',
                       choices=['daily', 'weekly', 'monthly'],
                       help='时间范围: daily(今日), weekly(本周), monthly(本月)')
    parser.add_argument('--limit', '-n', type=int, default=10,
                       help='显示项目数量 (默认: 10)')
    parser.add_argument('--export', '-e', type=str, choices=['csv', 'json', 'both'],
                       help='导出格式: csv, json, both')
    parser.add_argument('--no-cache', action='store_true',
                       help='不使用缓存')
    parser.add_argument('--all', '-a', action='store_true',
                       help='显示所有项目')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='安静模式，只输出数据')
    
    args = parser.parse_args()
    
    # 创建GitHub趋势获取器
    trending = GitHubTrending()
    
    # 获取数据
    projects = trending.fetch_trending(
        language=args.language,
        since=args.since,
        use_cache=not args.no_cache
    )
    
    if not projects:
        print("错误: 无法获取GitHub趋势数据")
        sys.exit(1)
    
    # 设置显示限制
    limit = None if args.all else args.limit
    
    # 输出结果
    if not args.quiet:
        trending.print_summary(projects, limit=limit if limit else len(projects))
    
    # 导出数据
    if args.export:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if args.export in ['csv', 'both']:
            filename = f"github_trending_{timestamp}.csv"
            trending.export_to_csv(projects, filename)
        
        if args.export in ['json', 'both']:
            filename = f"github_trending_{timestamp}.json"
            trending.export_to_json(projects, filename)
    
    # 在安静模式下只输出JSON
    if args.quiet:
        print(json.dumps(projects, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()