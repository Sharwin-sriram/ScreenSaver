import sys
import tkinter as tk
import time
import requests
from PIL import Image, ImageTk
from io import BytesIO
import ctypes


# ----------------- NOTES -----------------
# USE 6-DIGIT HEX FOR COLORS
# REPLACE THE API KEY WITH YOUR OWN API KEY 
# GET A API KEY FROM https://openweathermap.org/


# ----------------- DONT CHANGE -----------------
run_screensaver = False
preview_mode = False
preview_hwnd = None
weather_icon = None


# ----------------- ROOT CONFIG -----------------
root = tk.Tk()
root.configure(bg="black")
root.config(cursor="none")

canvas = tk.Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

API_KEY = ""        # YOUR API KEY
IPINFO_API = "http://ip-api.com/json/"
LAT, LON, CITY, REGION = 0, 0, "", ""

CLOCK_SIZE = 120        # MAIN CLOCK FONT SIZE
FONT_FAMILY = "Calibri"         # FONT OF THE OVERALL GUI
TEMP_FONT = (FONT_FAMILY, 32)       # Replace FONT_FAMILY HERE FOR DIFFERENT FONT FOR TEMPERATURE
DATE_FONT = (FONT_FAMILY, 30)       # Replace FONT_FAMILY HERE FOR DIFFERENT FONT FOR DATE

DATE_COLOR = "white"        # COLOR OF THE DATE ABOVE THE CLOCK    
WEATHER_COLOR = "white"     # COLOR OF THE WEATHER UNDER THE CLOCK
CLOCK_COLOR = "white"       # COLOR OF THE CLOCK
AM_COLOR = "#a2a8ff"       # COLOR FOR AFTER MERIDIAN
PM_COLOR = "#37c0f7"       # COLOR FOR POST MERIDIAN


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
    sys.exit()          # CHANGE THIS TO - run_screensaver = True //FOR TESTING
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
    now = time.strftime("%I:%M")
    ampm = time.strftime("%p")
    date = time.strftime("%a, %d %b")

    x = root.winfo_screenwidth() // 2
    y = root.winfo_screenheight() // 2

    canvas.create_text(
        x, y - 90, 
        text=date, 
        fill=DATE_COLOR,
        font=DATE_FONT, 
        tags="clock"
    )

    time_id = canvas.create_text(0, 0, text=now, font=(FONT_FAMILY, CLOCK_SIZE), tags="measure")
    ampm_id = canvas.create_text(0, 0, text=ampm, font=(FONT_FAMILY, CLOCK_SIZE), tags="measure")

    bbox_time = canvas.bbox(time_id)
    bbox_ampm = canvas.bbox(ampm_id)

    time_w = bbox_time[2] - bbox_time[0] if bbox_time else 0
    ampm_w = bbox_ampm[2] - bbox_ampm[0] if bbox_ampm else 0

    canvas.delete("measure")

    total_w = time_w + 20 + ampm_w

    start_x = x - total_w // 2

    canvas.create_text(
        start_x, y,
        text=now, 
        fill=CLOCK_COLOR,
        font=(FONT_FAMILY, CLOCK_SIZE),
        anchor="w", 
        tags="clock"
    )
    if ampm == "AM":
        canvas.create_text(
            start_x + time_w + 20, y,
            text=ampm, 
            fill=AM_COLOR,
            font=(FONT_FAMILY, CLOCK_SIZE),
            anchor="w", 
            tags="clock"
        )
    elif ampm == "PM":
        canvas.create_text(
            start_x + time_w + 20, y,
            text=ampm, 
            fill=PM_COLOR,
            font=(FONT_FAMILY, CLOCK_SIZE),
            anchor="w", 
            tags="clock"
        )

    if current_weather != "Weather N/A":
        text_width = canvas.create_text(0, 0, text=current_weather, font=TEMP_FONT, tags="measure")
        bbox = canvas.bbox(text_width)
        canvas.delete("measure")
        text_w = bbox[2] - bbox[0] if bbox else 0
        icon_w = weather_icon.width()
        total_w = icon_w + 10 + text_w
        start_x = x - total_w // 2
        canvas.create_image(start_x + icon_w // 2, y + 110,
                            image=weather_icon,
                            tags="clock")
        canvas.create_text(start_x + icon_w + 10, y + 110, 
                           text=current_weather, 
                           fill=WEATHER_COLOR, 
                           font=TEMP_FONT, 
                           anchor="w", 
                           tags="clock")
    else:
        canvas.create_text(x, y + 90, text="Weather N/A", fill=WEATHER_COLOR, font=TEMP_FONT, tags="clock")
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