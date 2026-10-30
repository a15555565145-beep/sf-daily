import asyncio
from playwright.async_api import async_playwright

async def fetch_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
        """)
        
        await page.goto("https://wiki.avakot.org/", timeout=60000)
        # 稍微等 5 秒，确保动态内容加载完毕
        await page.wait_for_timeout(5000) 
        
        text = await page.evaluate("document.body.innerText")
        await browser.close()
        return text

if __name__ == "__main__":
    data = asyncio.run(fetch_data())
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
