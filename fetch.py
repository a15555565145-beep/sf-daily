import requests
import re
import datetime

def fetch_data():
    # 直接请求 API 接口，拿到纯净的 JSON 数据
    api_url = "https://wiki.avakot.org/w/api.php?action=parse&page=Main_Page&prop=wikitext&format=json"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(api_url, headers=headers, timeout=15)
        data = response.json()
        
        # 提取维基源码
        wikitext = data['parse']['wikitext']['*']
        
        # 1. 精准提取先祖名字（匹配模板参数里的 ancestor = 某单词）
        ancestor = "未知"
        match_anc = re.search(r'ancestor\s*=\s*([A-Za-z]+)', wikitext, re.IGNORECASE)
        if match_anc:
            ancestor = match_anc.group(1).strip()
            
        # 2. 提取今日武器（匹配 Today's Weapons 区域里的武器名）
        weapons = "未知"
        # 从 Today's Weapons 开始截取一段，直到遇到下一个大标题
        match_weapons_block = re.search(r"Today's Weapons(.*?)(?:Weatherways|WEATHERWAYS)", wikitext, re.DOTALL | re.IGNORECASE)
        if match_weapons_block:
            block = match_weapons_block.group(1)
            # 提取里面所有的武器名字（通常是 =[[ 名字 ]] 这种格式）
            weapon_names = re.findall(r'\[\[([A-Za-z]+)', block)
            if weapon_names:
                weapons = ", ".join(weapon_names[:8])

        # 拼装结果
        result = f"【Soulframe 每日播报】\n📅 日期：{datetime.datetime.now().strftime('%Y-%m-%d')}\n\n🔮 当前先祖：{ancestor}\n⚔️ 今日武器：{weapons}"
        return result
        
    except Exception as e:
        return f"【Soulframe 每日播报】\nAPI解析失败: {e}"

if __name__ == "__main__":
    data = fetch_data()
    with open("sf_daily.txt", "w", encoding="utf-8") as f:
        f.write(data)
    print("抓取完毕！")
