import requests
import re
import datetime
import os
import json

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

def fetch_data():
    url = "https://wiki.avakot.org/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=15)
    
    # 剔除网页里的无用代码
    text = re.sub(r'<script.*?</script>', '', response.text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    print("让 DeepSeek 提取信息...")
    api_url = "https://api.deepseek.com/v1/chat/completions"
    api_headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个数据提取机器人。请从下面的网页文本中，帮我找出 CURRENT ANCESTOR 后面的先祖名字，以及 Today's Weapons 附近的武器列表。用中文简洁输出。"},
            {"role": "user", "content": text[:20000]} # 截取前两万字符
        ]
    }
    
    try:
        res = requests.post(api_url, headers=api_headers, json=payload, timeout=60)
        res_data = res.json()
        
        # 增加容错：如果 API 报错，把报错信息打出来
        if 'choices' not in res_data:
            print("API 报错啦！返回内容：", res_data)
            return "【Soulframe 每日播报】\n🔮 当前先祖：API解析失败\n⚔️ 今日武器：请查看服务器日志"
            
        ai_result = res_data['choices'][0]['message']['content']
    except Exception as e:
        print("请求失败:", e)
        return "【Soulframe 每日播报】\n🔮 当前先祖：请求超时\n"

    # 拼装结果
    result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n{ai_result}"
    return result

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
