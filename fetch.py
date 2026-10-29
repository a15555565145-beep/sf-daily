import requests
import datetime
import json

def fetch_data():
    api_url = "https://wiki.avakot.org/w/api.php?action=parse&page=Main_Page&prop=wikitext&format=json"
    
    # 终极伪装头部
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        
        # 如果返回的状态码不是 200，说明被拦截了
        if response.status_code != 200:
            return f"【Soulframe 每日播报】\nAPI 被拦截，状态码: {response.status_code}"
            
        data = response.json()
        
        # 如果返回的数据里没有 parse 字段，说明格式不对
        if 'parse' not in data:
            return f"【Soulframe 每日播报】\nAPI 解析失败，返回内容: {str(data)[:100]}"

        wikitext = data['parse']['wikitext']['*']
        
        ancestor = "未找到"
        if "ancestor =" in wikitext:
            part = wikitext.split("ancestor =")[1]
            ancestor = part.split("|")[0].strip()

        weapons = "未找到"
        if "Today's Weapons" in wikitext:
            part = wikitext.split("Today's Weapons")[1]
            weapons = part[:200].replace("\n", " ").strip()

        result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n🔮 当前先祖：{ancestor}\n⚔️ 今日武器：{weapons}"
        return result
        
    except Exception as e:
        return f"【Soulframe 每日播报】\n请求异常: {e}"

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
