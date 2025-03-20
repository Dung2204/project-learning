import requests
import json
from datetime import datetime
import csv
import os

previous_weather_data = None

def fetch_weather_data(city, api_key="c898411271d292f65b6e627be80c0239"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code != 200:
            return None

        weather_info = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"] * 3.6,
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
        return weather_info
    
    except Exception as e:
        return None

def calculate_accuracy(current_data, previous_data):
    if not previous_data or current_data["city"] != previous_data["city"]:
        return 95.0
    
    current_time = datetime.strptime(current_data["timestamp"], "%Y-%m-%d %H:%M:%S")
    previous_time = datetime.strptime(previous_data["timestamp"], "%Y-%m-%d %H:%M:%S")
    time_diff = (current_time - previous_time).total_seconds() / 60
    
    temp_diff = abs(current_data["temperature"] - previous_data["temperature"])
    humidity_diff = abs(current_data["humidity"] - previous_data["humidity"])
    wind_diff = abs(current_data["wind_speed"] - previous_data["wind_speed"])
    
    base_accuracy = 95.0
    if time_diff < 60:
        if temp_diff > 5 or humidity_diff > 20 or wind_diff > 10:
            base_accuracy -= 10
        if temp_diff > 10 or humidity_diff > 40 or wind_diff > 20:
            base_accuracy -= 10
    
    return max(base_accuracy, 50.0)

def save_to_csv(weather_info, filename=r"C:\Users\Dell\OneDrive\Pictures\Documents\Code\python\OpenCV\Project\Thoitiet\weather_data.csv"):
    fieldnames = ["timestamp", "city", "temperature", "description", "humidity", "wind_speed", "lat", "lon"]
    
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow(weather_info)

def display_weather(weather_info):
    global previous_weather_data
    
    if weather_info:
        accuracy = calculate_accuracy(weather_info, previous_weather_data)
        print("\n=== Thông tin thời tiết hôm nay ===")
        print(f"Thời gian: {weather_info['timestamp']}")
        print(f"Thành phố: {weather_info['city']}")
        print(f"Nhiệt độ: {weather_info['temperature']}°C")
        print(f"Tình hình: {weather_info['description']}")
        print(f"Độ ẩm: {weather_info['humidity']}%")
        print(f"Tốc độ gió: {weather_info['wind_speed']} km/h")
        print(f"Tọa độ: ({weather_info['lat']}, {weather_info['lon']})")
        print(f"Độ chính xác ước lượng: {accuracy:.1f}%")
        
        save_to_csv(weather_info)
        
        previous_weather_data = weather_info.copy()
    else:
        print("Không thể lấy thông tin thời tiết.")

def main():
    api_key = "######"
    
    while True:
        city = input("Nhập tên thành phố (ví dụ: Hue, Hanoi, London): ")
        weather_info = fetch_weather_data(city, api_key)
        display_weather(weather_info)
        
        while True:
            choice = input("\nBạn muốn: 1. Tiếp tục | 2. Dừng? (Nhập 1 hoặc 2): ").strip()
            if choice in ['1', '2']:
                break
        
        if choice == '2':
            break

if __name__ == "__main__":
    main()
