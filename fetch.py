import requests
import re
import datetime

def fetch_data():
    url = "https://wiki.avakot.org/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, timeout=15)
    
    # 清理网页代码，提取纯文本
    text = re.sub(r'<script.*?</script>', '', response.text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # 直接用正则硬抠
    ancestor = "未知"
    match_anc = re.search(r'CURRENT ANCESTOR\s*([A-Za-z]+)', text, re.IGNORECASE)
    if match_anc:
        ancestor = match_anc.group(1).strip()
    else:
        # 尝试另一种可能
        match_anc2 = re.search(r'CURRENT ANCESTOR.*?([A-Z][a-z]+)', text, re.IGNORECASE)
        if match_anc2:
            ancestor = match_anc2.group(1).strip()

    weapons = "未知"
    match_wep = re.search(r"Today's Weapons(.*?)(?:WEATHERWAYS|Search|CURRENT)", text, re.DOTALL | re.IGNORECASE)
    if match_wep:
        # 只取前面一部分，去除多余空行
        lines = [l.strip() for l in match_wep.group(1).strip().split('\n') if l.strip()]
        weapons = ", ".join(lines[:8])

    # 拼装结果
    result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n🔮 当前先祖：{ancestor}\n⚔️ 今日武器：{weapons}"
    return result

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
