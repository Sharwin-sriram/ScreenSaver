import sys
import tkinter as tk
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO
import ctypes

run_screensaver = False
preview_mode = False
preview_hwnd = None
weather_icon = None

root = tk.Tk()
root.configure(bg="black")
root.config(cursor="none")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

API_KEY = ""
IPINFO_API = "http://ip-api.com/json/"
LAT, LON, CITY, REGION = 0, 0, "", ""

if len(sys.argv) > 1:
    arg = sys.argv[1].lower()
    if arg == "/s":
        run_screensaver = True
    elif arg == "/c":
        sys.exit()
    elif arg == "/p":
        preview_mode = True
        if len(sys.argv) > 2:
            try:
                preview_hwnd = int(sys.argv[2])
                run_screensaver = True
            except ValueError:
                sys.exit()
else:
    run_screensaver = True
if not run_screensaver:
    sys.exit()
    
if preview_mode and preview_hwnd:
    ctypes.windll.user32.SetParent(root.winfo_id(), preview_hwnd)
    root.overrideredirect(True)
else:
    root.attributes("-fullscreen", True)


try:
    ipinfo = requests.get(IPINFO_API, timeout=5)
    data = ipinfo.json()
    print(data)
    LAT, LON = data["lat"], data["lon"]
    CITY, REGION = data.get("city","Unknown"), data.get("regionName", "")
except:
    LAT, LON, CITY, REGION = 0, 0, "Unknown", ""

def get_weather():
    global weather_icon
    try:
        URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        response = requests.get(URL, timeout=5)
        data = response.json()
        if data.get("cod") != 200:
            return "Weather N/A"
        temp = data["main"]["temp"]
        icon_code = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url, timeout=5)
        img_data = icon_response.content
        img = Image.open(BytesIO(img_data)).convert("RGBA")
        img = img.resize((70, 70), Image.LANCZOS)
        weather_icon = ImageTk.PhotoImage(img)
        return f"{temp:.1f}°C   {CITY},{REGION}"
    except:
        return "API FETCH ERROR"

def draw_clock_text():
    canvas.delete("clock")
    now = time.strftime("%I:%M %p")
    date = time.strftime("%a, %d %b")
    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2
    canvas.create_text(x, y - 90, text=date, fill="white", font=("Calibri", 30), tags="clock")
    canvas.create_text(x, y, text=now, fill="white", font=("Calibri", 120), tags="clock")
    if current_weather != "Weather N/A" and weather_icon:
        temp_font = ("Calibri", 32)
        text_width = canvas.create_text(0, 0, text=current_weather, font=temp_font, tags="measure")
        bbox = canvas.bbox(text_width)
        canvas.delete("measure")
        text_w = bbox[2] - bbox[0] if bbox else 0
        icon_w = weather_icon.width()
        total_w = icon_w + 10 + text_w
        start_x = x - total_w // 2
        canvas.create_image(start_x + icon_w // 2, y + 110, image=weather_icon, tags="clock")
        canvas.create_text(start_x + icon_w + 10, y + 110, text=current_weather, fill="white", font=temp_font, anchor="w", tags="clock")
    else:
        canvas.create_text(x, y + 90, text="Weather N/A", fill="white", font=("Calibri", 32, "bold"), tags="clock")
    root.after(1000, draw_clock_text)

def update_weather():
    global current_weather
    current_weather = get_weather()
    root.after(600000, update_weather)

root.bind("<Escape>", lambda e: sys.exit())
root.bind("<Button>", lambda e: sys.exit())
root.bind("<Motion>", lambda e: sys.exit())
root.bind("<Escape>", lambda e: root.destroy())
root.bind("<Button>", lambda e: root.destroy())
root.bind("<Motion>", lambda e: root.destroy())

current_weather = get_weather()
draw_clock_text()
update_weather()
root.mainloop()