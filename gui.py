import speech_recognition as sr
from gtts import gTTS
from pathlib import Path
from tkinter import Entry, Tk, Canvas, Text, Button, PhotoImage
import os
import webbrowser
import subprocess
import requests

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\1. KULIAH\CATATAN KULIAH\SEMESTER 6\PENGENALAN UCAPAN DAN TEKS KE UCAPAN\TUGAS\TUGAS BESAR\GABUNGAN\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def detect_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="id-ID")
        display_text(text)
        respond(text)
    except sr.UnknownValueError:
        print("Gagal mengenali suara!")
    except sr.RequestError as e:
        print("Error memroses permintaan:", str(e))

def get_weather():
    api_key = ""  # Ganti dengan API key Anda dari OpenWeatherMap
    lat = "-6.898161107508915"  # Ganti dengan latitude koordinat yang diinginkan
    lon = "107.63491749929597"  # Ganti dengan longitude koordinat yang diinginkan
    lang = "id"
    units = "metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&lang={lang}&units={units}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data["weather"][0]["description"]
        name = data["name"]
        temperatureReal = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        return f"Cuaca saat ini di {name} adalah {weather_description}. " \
               f"Dengan suhu sekitar {temperatureReal:.1f} derajat celsius. " \
               f"Kelembapan {humidity}% dan kecepatan angin adalah {wind_speed} m/s."
    else:
        return "Gagal mendapatkan data cuaca."

def respond(text):
    if "halo" in text.lower():
        response = "Halo! Ada yang bisa saya bantu?"

    elif "siapa namamu" in text.lower():
        response = "Saya BoboiBot, asisten pribadi Anda."

    elif "bagaimana kabarmu" in text.lower():
        response = "Saya program komputer, jadi saya tidak memiliki perasaan. Bagaimana dengan Anda?"

    elif "saya baik-baik saja" in text.lower():
        response = "Syukurlah, semoga sehat selalu."

    elif "buka pintu" in text.lower():
        response = "Pintu terbuka!"
        entry_3.delete(0, "end")
        entry_3.insert("end", response)

    elif "tutup pintu" in text.lower():
        response = "Pintu tertutup!"
        entry_3.delete(0, "end")
        entry_3.insert("end", response)

    elif "bagaimana cuaca saat ini" in text.lower():
        response = get_weather()

    elif "putar" in text.lower():
        song_name = text.lower().replace("putar", "").strip()
        if song_name:
            response = f"Tentu! Memutar '{song_name}' di YouTube."
            play_music(song_name)
        else:
            response = "Mohon berikan nama lagu yang ingin Anda putar."
        

    elif "ok google" in text.lower():
        query = text.lower().replace("ok google", "").strip()
        if query:
            response = f"Mencari '{query}' di Google."
            search_google(query)
        else:
            response = "Mohon berikan kata kunci yang ingin Anda cari."

    else:
        response = "Maaf, saya tidak mengerti maksud Anda."

    text_to_speech(response)
    print("Chatbot:", response)
    display_response(response)

def display_text(text):
    entry_1.delete("1.0", "end")
    entry_1.insert("end", text)

def display_response(response):
    entry_2.delete("1.0", "end")
    entry_2.insert("end", response)

def play_music(song_name):
    search_query = "https://www.youtube.com/results?search_query=" + song_name.replace(" ", "+")
    webbrowser.open(search_query)

def search_google(query):
    search_query = "https://www.google.com/search?q=" + query.replace(" ", "+")
    webbrowser.open(search_query)

def text_to_speech(text):
    tts = gTTS(text=text, lang="id")
    file_path = OUTPUT_PATH / "response.mp3"  # Mengubah direktori penyimpanan file
    tts.save(file_path)
    os.startfile(file_path)  # Menggunakan os.startfile() untuk memainkan file mp3

def record_button_clicked():
    detect_speech()

def play_button_clicked():
    text = entry_2.get("1.0", "end").strip()
    if text:
        display_response(text)
        respond(text)

def clear_button_clicked():
    entry_1.delete("1.0", "end")
    entry_2.delete("1.0", "end")

def exit_button_clicked():
    window.destroy()

window = Tk()
window.geometry("1280x720")
window.configure(bg="#0C254A")

canvas = Canvas(
    window,
    bg="#0C254A",
    height=720,
    width=1280,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

canvas.create_text(
    195.0,
    94.0,
    anchor="nw",
    text="Speech Recognition",
    fill="#FFFFFF",
    font=("Inter Bold", 24)
)

canvas.create_text(
    863.0,
    94.0,
    anchor="nw",
    text="Text to Speech",
    fill="#FFFFFF",
    font=("Inter Bold", 24)
)

button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=record_button_clicked,
    relief="flat"
)
button_1.place(
    x=263.0,
    y=496.0,
    width=100.0,
    height=37.14288330078125
)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=clear_button_clicked,
    relief="flat"
)
button_2.place(
    x=686.0,
    y=496.0,
    width=100.0,
    height=37.14288330078125
)

button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=exit_button_clicked,
    relief="flat"
)
button_3.place(
    x=1116.0,
    y=496.0,
    width=100.0,
    height=37.14288330078125
)

entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    313.0,
    304.0,
    image=entry_image_1
)
entry_1 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=48.0,
    y=143.0,
    width=530.0,
    height=320.0
)
entry_1.config(font=("Inter Bold", 18))

entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    951.0,
    304.0,
    image=entry_image_2
)
entry_2 = Text(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=686.0,
    y=143.0,
    width=530.0,
    height=320.0
)
entry_2.config(font=("Inter Bold", 18))

canvas.create_text(
    475.0,
    42.0,
    anchor="nw",
    text="Virtual Assistant",
    fill="#FFFFFF",
    font=("Inter Bold", 32)
)

entry_image_3 = PhotoImage(file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    313.0,
    604.5,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    justify="center",
    highlightthickness=0
)
entry_3.place(
    x=48.0,
    y=582.0,
    width=530.0,
    height=43.0
)
entry_3.config(font=("Inter Bold", 18))

canvas.create_text(
    245.0,
    635.0,
    anchor="nw",
    text="Status Pintu",
    fill="#FFFFFF",
    font=("Inter Medium", 17)
)

window.resizable(False, False)
window.mainloop()
