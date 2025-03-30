from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
FFMPEG_DIR = BASE_DIR / "ffmpeg" / "bin"

ydl_opts = {
    'ffmpeg_location': str(FFMPEG_DIR),
    'outtmpl': str(BASE_DIR / 'downloads' / '%(title)s.%(ext)s'),
    'restrictfilenames': True,
    'windowsfilenames': True,
    'quiet': True,
    'no_warnings': True,
}

def progress_hook(d):
    if d['status'] == 'downloading':
        percentage = d['_percent_str']
        print(f"Скачивание: {percentage}")

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Максимальное разрешение
    'merge_output_format': 'mp4',
    'progress_hooks': [progress_hook],
    'socket_timeout': 60,
    'retries': 5,
    'nocheckcertificates': True
}

