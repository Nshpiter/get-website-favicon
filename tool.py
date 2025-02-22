import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import re

def get_favicon(url):
    try:
        # 解析 URL
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # 获取网页内容
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 存储所有可能的图标 URL
        icon_urls = []
        
        # 1. 从 HTML 头部搜索图标链接
        for link in soup.find_all('link'):
            rel = link.get('rel', [])
            if isinstance(rel, str):
                rel = [rel]
            
            if any(x in ['icon', 'shortcut icon', 'apple-touch-icon', 'apple-touch-icon-precomposed'] for x in rel):
                href = link.get('href')
                if href:
                    icon_urls.append(urljoin(base_url, href))
        
        # 2. 检查常见的图标位置
        common_paths = [
            '/favicon.ico',
            '/favicon.png',
            '/apple-touch-icon.png',
            '/apple-touch-icon-precomposed.png'
        ]
        
        for path in common_paths:
            icon_urls.append(base_url + path)
        
        # 尝试下载每个可能的图标
        for icon_url in icon_urls:
            try:
                icon_response = requests.get(icon_url, timeout=5)
                if icon_response.status_code == 200:
                    # 从 URL 中提取文件扩展名
                    file_ext = re.search(r'\.(ico|png|jpg|jpeg)$', icon_url.lower())
                    file_ext = file_ext.group() if file_ext else '.ico'
                    
                    # 保存图标
                    filename = f"favicon{file_ext}"
                    with open(filename, "wb") as f:
                        f.write(icon_response.content)
                    print(f"成功下载图标：{filename}")
                    print(f"图标 URL：{icon_url}")
                    return True
            except Exception as e:
                continue
        
        print("未找到可用的网站图标。")
        return False
        
    except Exception as e:
        print(f"发生错误：{str(e)}")
        return False

# 示例用法
if __name__ == "__main__":
    website_url = input("请输入网站 URL: ")
    get_favicon(website_url)
