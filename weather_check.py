import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

LATITUDE = 25.0375
LONGITUDE = 121.5637
RAIN_THRESHOLD = 70

token = os.environ["TELEGRAM_BOT_TOKEN"]
chat_id = os.environ["TELEGRAM_CHAT_ID"]

url = "https://api.open-meteo.com/v1/forecast"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "daily": "precipitation_probability_max,temperature_2m_max,temperature_2m_min",
    "timezone": "Asia/Taipei",
    "forecast_days": 1
}

print("正在取得天氣資料...")

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()

weather = response.json()

rain_probability = weather["daily"]["precipitation_probability_max"][0]
max_temperature = weather["daily"]["temperature_2m_max"][0]
min_temperature = weather["daily"]["temperature_2m_min"][0]

taiwan = ZoneInfo("Asia/Taipei")
today = datetime.now(taiwan).strftime("%Y-%m-%d")

print("日期:", today)
print("最高降雨機率:", rain_probability, "%")
print("最高溫:", max_temperature, "°C")
print("最低溫:", min_temperature, "°C")

if rain_probability >= RAIN_THRESHOLD:
    print("降雨機率超過 70%，發送 Telegram！")

    message = (
        "☔ 記得帶傘喔！\n\n"
        "📅 日期：" + today + "\n"
        "🌧️ 最高降雨機率：" + str(rain_probability) + "%\n"
        "🌡️ 最高溫：" + str(max_temperature) + "°C\n"
        "🌡️ 最低溫：" + str(min_temperature) + "°C\n\n"
        "出門記得帶雨具 ☂️"
    )

    telegram_url = "https://api.telegram.org/bot" + token + "/sendMessage"

    telegram_data = {
        "chat_id": chat_id,
        "text": message
    }

    telegram_response = requests.post(
        telegram_url,
        data=telegram_data,
        timeout=30
    )

    telegram_response.raise_for_status()

    print("Telegram 通知成功！")

else:
    print("降雨機率低於 70%，不發送通知。")

if __name__ == "__main__":
    msg = get_weather()
    print(f"氣象資訊內容：\n{msg}")
    send_telegram_msg(msg)
