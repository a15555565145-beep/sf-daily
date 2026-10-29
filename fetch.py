import os
import requests
import re
import datetime

# 填入你的 DeepSeek API Key
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def fetch_data():
    url = "https://wiki.avakot.org/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=15)
    
    # 清理网页代码，提取纯文本
    text = re.sub(r'<script.*?</script>', '', response.text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 调用 DeepSeek 提取信息
    api_url = "https://api.deepseek.com/v1/chat/completions"
    api_headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个数据提取机器人。请阅读用户提供的网页纯文本，提取出【当前的先祖名字】以及【今日商店出售的武器名称与价格】。请用简洁的中文输出，格式为：\n🔮 当前先祖：xxx\n⚔️ 今日武器：xxx, xxx。不要输出任何废话。"},
            {"role": "user", "content": text[:30000]} 
        ]
    }
    
    res = requests.post(api_url, headers=api_headers, json=payload, timeout=60)
    ai_result = res.json()['choices'][0]['message']['content']

    # 拼装结果
    result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n{ai_result}"
    return result

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取并提取完毕！")
