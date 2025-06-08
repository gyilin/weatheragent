import requests
import datetime
import schedule
import time

# === 你的配置 ===
API_KEY = "bb9fddec56184e4490e99d8b2ca819c7"
CITY = "boston"
ADMIN = "USA"
SENDKEY = "SCT282122TJUyr6PRU9ATU1XlJTt9cZB7G"

# === 获取天气函数 ===
def get_weather():
    url = f"https://devapi.qweather.com/v7/weather/now?location={CITY}&adm={ADMIN}&key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()

    if data.get("code") != "200":
        return "❌ 天气获取失败"

    now = data["now"]
    weather_text = now["text"]
    temp = now["temp"]
    wind_dir = now["windDir"]
    wind_scale = now["windScale"]

    date = datetime.datetime.now().strftime("%Y-%m-%d (%A)")

    msg = (
        f"📍 城市：Boston 🇺🇸\n"
        f"📅 日期：{date}\n"
        f"🌦️ 天气：{weather_text}\n"
        f"🌡️ 气温：{temp}℃\n"
        f"💨 风力：{wind_dir} {wind_scale}级\n"
        f"🧥 提示：出门记得查看天气变化哦！"
    )
    return msg

# === 推送微信消息 ===
def send_wechat(msg):
    push_url = f"https://sctapi.ftqq.com/{SENDKEY}.send"
    data = {
        "title": "今日天气提醒 ☀️",
        "desp": msg
    }
    requests.post(push_url, data=data)

# === 组合函数：获取 + 推送 ===
def weather_agent():
    print("正在获取天气并推送中...")
    msg = get_weather()
    send_wechat(msg)
    print("已发送 ✔️")

# === 每天定时任务设置 ===
schedule.every().day.at("08:00").do(weather_agent)

print("🌤️ 天气提醒 Agent 正在运行（每天08:00自动提醒）")
while True:
    schedule.run_pending()
    time.sleep(60)
