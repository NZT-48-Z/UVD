from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import uvicorn
import os
import subprocess

from app import router as page

app = FastAPI()

app.mount("/static",StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),name="static")

app.include_router(page)

def init_project():
    required_dirs = [
        "downloads",
        "temp_downloads",
        "ffmpeg/bin"
    ]
    
    for dir_name in required_dirs:
        os.makedirs(dir_name, exist_ok=True)

try:
    ffmpeg_check = subprocess.run(
        [os.path.join("ffmpeg", "bin", "ffmpeg.exe"), "-version"],
        capture_output=True,
        text=True
    )
    if ffmpeg_check.returncode == 0:
        print("FFmpeg успешно настроен!")
        print(ffmpeg_check.stdout.split('\n')[0])
    else:
        print("Ошибка FFmpeg:", ffmpeg_check.stderr)
except Exception as e:
    print("Ошибка при проверке FFmpeg:", str(e))

if __name__ == '__main__':
    uvicorn.run('main:app')