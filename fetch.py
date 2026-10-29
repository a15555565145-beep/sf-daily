import asyncio
from playwright.async_api import async_playwright

async def fetch_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://wiki.avakot.org/", timeout=60000)
        # 抓取网页上所有可见的纯文本
        text = await page.evaluate("document.body.innerText")
        await browser.close()
        return text

if __name__ == "__main__":
    data = asyncio.run(fetch_data())
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
