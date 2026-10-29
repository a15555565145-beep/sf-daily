import requests
import re
import datetime
import os

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def fetch_data():
    url = "https://wiki.avakot.org/"
    
    # 终极伪装：伪装成真实的 Windows 浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        # 启用 Session 来保持 cookies
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        # 提取纯文本
        text = re.sub(r'<script.*?</script>', '', response.text, flags=re.DOTALL)
        text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # 如果还是拦截页面，直接让 AI 告诉我们
        print("让 DeepSeek 提取信息...")
        api_url = "https://api.deepseek.com/v1/chat/completions"
        api_headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": "你是一个数据提取机器人。请从下面的网页文本中，找出 CURRENT ANCESTOR 后面的先祖名字，以及 Today's Weapons 附近的武器列表。如果网页是一个拦截页面，请直接告诉我‘被拦截’。"},
                {"role": "user", "content": text[:20000]} 
            ]
        }
        
        res = requests.post(api_url, headers=api_headers, json=payload, timeout=60)
        res_data = res.json()
        
        if 'choices' not in res_data:
            return f"【Soulframe 每日播报】\nAPI解析失败：{res_data}"
            
        ai_result = res_data['choices'][0]['message']['content']
    except Exception as e:
        return f"【Soulframe 每日播报】\n请求失败: {e}"

    result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n{ai_result}"
    return result

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
