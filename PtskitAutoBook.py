from DrissionPage import Chromium
import os
import json
import time
url = 'https://www.ptskit.org/'
# 定义cookies文件路径
COOKIES_FILE = 'ptskit_cookies.json'

def read_cookie():
    """读取 cookie，优先从环境变量读取，其次从本地文件读取"""
    # 1. 首先尝试从环境变量读取
    if "PTSKIT_COOKIES" in os.environ:
        return json.loads(os.environ["PTSKIT_COOKIES"])
    
    # 2. 如果环境变量不存在，尝试从本地文件读取
    local_file = "ptskit_cookies.json"
    if os.path.exists(local_file):
        try:
            with open(local_file, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            print(f"已从本地文件 {local_file} 读取cookie")
            return cookies
        except Exception as e:
            print(f"读取本地cookie文件失败: {e}")
    
    # 3. 如果都找不到，返回空列表并提示
    print("贴吧Cookie未配置！详细请参考教程！")
    return []


def login_website():
    browser = Chromium()
    # 启动或接管浏览器，并获取标签页对象
    tab = browser.latest_tab

    # 跳转到登录页面
    tab.get(url,timeout=10)
    tab.set.cookies(read_cookie())
    tab.refresh()
    tab._wait_loaded()
    
    # 方式1：使用 XPath 定位（推荐，兼容性好）
    attendance = tab.ele('xpath://a[@href="attendance.php" and @class="faqlink"]')

    # 3. 点击按钮（确保元素可点击后再操作）
    if attendance:  # 检查元素是否存在
        tab.run_js('''
            const evt = new MouseEvent('click', { bubbles: true, cancelable: true });
            arguments[0].dispatchEvent(evt);
        ''', attendance)
        print("已点击签到按钮")
    else:
        print("未找到关闭按钮")

    #关闭
    browser.quit()



# 使用示例
if __name__ == "__main__":
    tab = login_website()