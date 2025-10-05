# SCREENSAVER FOR WINDOWS

Simple screensaver for windows that is built using tkinter and uses ip-api to get the local approx coordiates and uses that coordinates on openweathermap api to get local weather details

## Installation

1.Clone the project
```bash
git clone https://github.com/Sharwin-sriram/ScreenSaver
```

2.Create a virtual Environment
```bash
python -m venv env
env\scripts\activate
```

3.Install Dependencies
```bash
pip install -r requirements.txt
```

4.Replace with your api key

> go to openweathermap and get a **free api key** and paste it in line 9 of the project
> ```python
> API_KEY = ""
> ```

[https://openweathermap.org/](https://openweathermap.org/)


5.Make Additional Customisations (optional)
```python

CLOCK_SIZE = 120
FONT_FAMILY = "Calibri"
TEMP_FONT = (FONT_FAMILY, 32)
DATE_FONT = (FONT_FAMILY, 30)

DATE_COLOR = "white"
WEATHER_COLOR = "white"
CLOCK_COLOR = "white"
AM_COLOR = "#a2a8ff"
PM_COLOR = "#37c0f7"

```

6.Build Command
```bash
pyinstaller --onefile --noconsole --clean --noupx screensaver.py
```

7.Installation

> The file would be avilabe in:
>
> ```bash
> dist/screensaver.exe
> ```
rename the .exe file into .scr file and paste it into


```bash
C:\Windows\System32\
```


8.Activation

Now:
> hit the windows key search screensaver and you should see something called screensaver


NOTE: Windows might tag the file as a malware as the .exe is not signed 
