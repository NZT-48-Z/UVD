import yt_dlp
import os

def download_video(url):
    ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
    os.environ["PATH"] += os.pathsep + os.path.abspath(os.path.dirname(ffmpeg_path))

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Максимальное разрешение
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
        'socket_timeout': 60,
        'retries': 5,
        'nocheckcertificates': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        print(f"Скачивание: {percentage}")

url = input("Введите ссылку на видео YouTube: ")
download_video(url)