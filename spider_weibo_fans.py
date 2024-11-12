import requests
import pandas as pd
import time

# author: gagaduck
# date: 2024-11-12
# description: 爬取微博某个人的粉丝数据

def scrape_weibo_fans(uid, cookie):
    # 设置请求头
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    }

    all_fans_data = []  # 存放所有爬取的粉丝数据
    page = 1            # 初始页码
    # 备注！！！ 
    # 用户数据是非常重要的商业数据，由于微博的限制，哪怕粉丝数量很多也是最多只能爬到page=99的

    while True:
        url = f"https://weibo.com/ajax/friendships/friends?relate=fans&page={page}&uid={uid}&type=fans&newFollowerCount=0"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to retrieve data for page {page}. Status code: {response.status_code}")
            break

        data = response.json()

        # 检查是否有粉丝数据
        fans_list = data.get("users")
        if not fans_list:
            print(f"No more data found on page {page}. Stopping.")
            break

        # 处理每个粉丝信息并添加到列表中
        for fan in fans_list:
            fan_data = {
                "id": fan.get("id"),
                "avatar_hd": fan.get("avatar_hd"),
                "screen_name": fan.get("screen_name"),
                "description": fan.get("description"),
                "followers_count": fan.get("followers_count"),
                "friends_count": fan.get("friends_count"),
                "statuses_count": fan.get("statuses_count"),
                "verified": fan.get("verified"),
                "verified_reason": fan.get("verified_reason"),
                "created_at": fan.get("created_at"),
                "location": fan.get("location")
            }
            all_fans_data.append(fan_data)

        print(f"Page {page} scraped successfully.")
        page += 1
        time.sleep(1)  # 每秒增加一次页码

    # 保存数据到 Excel
    df = pd.DataFrame(all_fans_data)
    df.to_excel("weibo_fans_data.xlsx", index=False)
    print("Data saved to weibo_fans_data.xlsx")

# 提供uid和cookie
# UID = "需要爬取的微博用户ID"
uid = ""
# COOKIE = "当前用户的cookie"
cookie = ""

scrape_weibo_fans(uid, cookie)
