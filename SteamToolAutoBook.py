from DrissionPage import Chromium
import os
import json
import time

# 定义cookies文件路径
COOKIES_FILE = 'steamtool_cookies.json'

def read_cookie():
    """读取 cookie，优先从环境变量读取，其次从本地文件读取"""
    # 1. 首先尝试从环境变量读取
    if "STEAMTOOL_COOKIES" in os.environ:
        return json.loads(os.environ["STEAMTOOL_COOKIES"])
    
    # 2. 如果环境变量不存在，尝试从本地文件读取
    local_file = "steamtool_cookies.json"
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
    # 启动或接管浏览器，并获取标签页对象
    tab = Chromium().latest_tab

    # 跳转到登录页面
    tab.get('https://caigamer.cn/')
    tab.set.cookies(read_cookie())
    tab.refresh()
    tab._wait_loaded(15)
    
    # 方式1：使用 XPath 定位（推荐，兼容性好）
    close_btn = tab.ele('xpath://button[@class="btn-close" and @data-bs-dismiss="modal"]')

    # 3. 点击按钮（确保元素可点击后再操作）
    if close_btn:  # 检查元素是否存在
        close_btn.click()  # 普通点击
        # 若点击无效，可尝试强制点击（跳过可点击校验）
        # close_btn.click(force=True)
    else:
        print("未找到关闭按钮")

    # 方式1：通过ID定位最可靠
    sign_button = tab.ele('#sg_sign')
    if sign_button:  # 检查元素是否存在
        # sign_button.click()  # 普通点击
        sign_button.hover()  # 先悬停
        tab.wait(0.5)       # 等待动画效果
        sign_button.click()  # 点击元素中心位置
        print("已点击签到按钮")
    else:
        print("未找到关闭按钮")



# 使用示例
if __name__ == "__main__":
    tab = login_website()