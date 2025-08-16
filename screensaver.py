import tkinter as tk
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="env/.env")
API_KEY = os.getenv("API_KEY")

LAT = 0
LON = 0
CITY = "API ERROR"
REGION = ""
URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
try:
  ipinfo = requests.get("https://ipinfo.io/json")
  data = ipinfo.json()
  LAT , LON = data["loc"].split(",")
  CITY , REGION = data["city"] , data["region"]
  print(data)
except:
  print("err")


print(CITY)
print(LAT , LON)


root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg="black")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

weather_icon = None


def get_weather():
    global weather_icon
    try:
        response = requests.get(URL, timeout=5)
        data = response.json()
        if data["cod"] != 200:
            return "Weather N/A"
        
        temp = data["main"]["temp"]
        icon_code = data["weather"][0]["icon"]


        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, timeout=5)
        img_data = icon_response.content
        img = Image.open(BytesIO(img_data)).convert("RGBA")
        img = img.resize((70, 70), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(img)

        return f"{temp:.1f}°C  {CITY},{REGION}"
    except Exception as e:
        print("Error fetching weather:", e)
        return "Weather N/A"


def draw_clock_text():
    canvas.delete("clock")

    now = time.strftime("%I:%M %p")
    date = time.strftime("%a, %d %b")

    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2

    canvas.create_text(
        x, y - 90,
        text=date,
        fill="white",
        font=("Calibri", 30, ""),
        tags="clock"
    )

    canvas.create_text(
        x, y,
        text=now,
        fill="white",
        font=("Calibri", 120, ""),
        tags="clock"
    )

    if current_weather != "Weather N/A":
        if weather_icon:
            temp_font = ("Calibri", 32, "")
            text_width = canvas.create_text(0, 0, text=current_weather, font=temp_font, tags="measure")
            bbox = canvas.bbox(text_width)
            canvas.delete("measure")
            text_w = bbox[2] - bbox[0] if bbox else 0

            icon_w = weather_icon.width()

            total_w = icon_w + 10 + text_w
            start_x = x - total_w // 2

            canvas.create_image(
                start_x + icon_w // 2, y + 110,
                image=weather_icon,
                tags="clock"
            )

            canvas.create_text(
                start_x + icon_w + 10, y + 110,
                text=current_weather,
                fill="white",
                font=temp_font,
                anchor="w",
                tags="clock"
            )
        else:
            canvas.create_text(
                x, y + 110,
                text=current_weather,
                fill="white",
                font=("Calibri", 32, ""),
                tags="clock"
            )
    else:
        canvas.create_text(
            x, y + 90,
            text="Weather N/A",
            fill="white",
            font=("Calibri", 32, "bold"),
            tags="clock"
        )

    root.after(1000, draw_clock_text)



def update_weather():
    global current_weather
    current_weather = get_weather()
    root.after(600000, update_weather)


root.bind("<Escape>", lambda e: root.destroy())
root.bind("<Button>", lambda e: root.destroy())
root.bind("<Motion>", lambda e: root.destroy())


current_weather = get_weather()
draw_clock_text()
update_weather()
root.mainloop()
