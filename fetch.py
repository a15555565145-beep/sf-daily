import requests
import re
import datetime

def fetch_data():
    url = "https://wiki.avakot.org/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=15)
    
    text = re.sub(r'<script.*?</script>', '', response.text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    ancestor = "未知"
    match_anc = re.search(r'CURRENT ANCESTOR\s*([A-Za-z]+)', text, re.IGNORECASE)
    if match_anc:
        ancestor = match_anc.group(1).strip()

    result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n🔮 当前先祖：{ancestor}\n"
    return result

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
