import asyncio
import re
import datetime
from playwright.async_api import async_playwright

async def fetch_data():
    print("启动隐身浏览器...")
    async with async_playwright() as p:
        # 启动 Chromium 浏览器，headless=True 表示无头模式（后台运行）
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 关键：模拟真实浏览器特征，降低被检测概率
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
        """)

        print("访问网页...")
        await page.goto("https://wiki.avakot.org/", timeout=60000)

        # 等待页面核心内容加载（等待包含“CURRENT ANCESTOR”的文本出现）
        try:
            await page.wait_for_function("document.body.innerText.includes('CURRENT ANCESTOR')", timeout=30000)
        except:
            print("等待超时，可能被拦截或页面结构变化。")

        # 获取网页上的所有纯文本
        text = await page.evaluate("document.body.innerText")
        await browser.close()

    # 用正则提取先祖和武器
    ancestor = "未知"
    match_anc = re.search(r'CURRENT ANCESTOR\s*([A-Za-z]+)', text, re.IGNORECASE)
    if match_anc:
        ancestor = match_anc.group(1).strip()

    weapons = "未知"
    match_wep = re.search(r"Today's Weapons(.*?)(?:WEATHERWAYS|Search|CURRENT)", text, re.DOTALL | re.IGNORECASE)
    if match_wep:
        lines = [l.strip() for l in match_wep.group(1).strip().split('\n') if l.strip()]
        weapons = ", ".join(lines[:8])

    result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n🔮 当前先祖：{ancestor}\n⚔️ 今日武器：{weapons}"
    return result

if __name__ == "__main__":
    data = asyncio.run(fetch_data())
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
