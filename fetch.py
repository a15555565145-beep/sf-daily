import asyncio
import re
import datetime
from playwright.async_api import async_playwright

async def fetch_data():
    print("启动模拟浏览器...")
    async with async_playwright() as p:
        # 启动真实的 Chromium 浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        print("访问网页...")
        await page.goto("https://wiki.avakot.org/", timeout=60000)
        
        # 获取网页上的所有纯文本
        text = await page.evaluate("document.body.innerText")
        await browser.close()

    # 用正则提取
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
