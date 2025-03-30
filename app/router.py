import shutil
import tempfile
import time
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
from typing import Optional

from app import html as index

import os
from pathlib import Path

# Получаем абсолютный путь к папке проекта
BASE_DIR = Path(__file__).parent.parent  # Поднимаемся на уровень выше из app/

# Путь к ffmpeg
FFMPEG_PATH = BASE_DIR / "ffmpeg" / "bin" / "ffmpeg.exe"

# Проверка существования
if not FFMPEG_PATH.exists():
    raise RuntimeError(f"FFmpeg не найден по пути: {FFMPEG_PATH}")

# Добавляем в переменные окружения
os.environ["PATH"] = f"{BASE_DIR / 'ffmpeg' / 'bin'}{os.pathsep}{os.environ['PATH']}"
os.environ["FFMPEG_PATH"] = str(FFMPEG_PATH)

router = APIRouter()
router.mount("/static", StaticFiles(directory="static"), name="static")

# Проверка и настройка FFmpeg
ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + os.path.abspath(os.path.dirname(ffmpeg_path))
    os.environ["FFMPEG_PATH"] = os.path.abspath(ffmpeg_path)

@router.get('/')
async def show_base_page():
    return HTMLResponse(index)

@router.get('/video-info')
async def get_video_info(url: str = Query(...)):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return {
                "title": info.get('title', ''),
                "thumbnail": info.get('thumbnail', ''),
                "duration": info.get('duration', 0),
                "views": info.get('view_count', 0),
                "url": url,
                "formats": info.get('formats', [])
            }
            
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

# 1. Настройка путей
BASE_DIR = Path(__file__).parent.parent
FFMPEG_PATH = BASE_DIR / "ffmpeg" / "bin" / "ffmpeg.exe"

# 2. Проверка FFmpeg
if not FFMPEG_PATH.exists():
    raise RuntimeError(f"FFmpeg не найден по пути: {FFMPEG_PATH}")

os.environ["PATH"] = f"{FFMPEG_PATH.parent}{os.pathsep}{os.environ['PATH']}"

@router.get('/download')
async def download_video(
    url: str = Query(...),
    format_type: str = Query('video'),
    quality: str = Query('720p')
):
    temp_dir = BASE_DIR / "temp_downloads"
    temp_dir.mkdir(exist_ok=True, parents=True)
    download_filename = None  # Будет определено позже
    
    try:
        ydl_opts = {
            'ffmpeg_location': str(FFMPEG_PATH.parent),
            'outtmpl': str(temp_dir / '%(title)s.%(ext)s'),
            'restrictfilenames': True,
            'windowsfilenames': True,
            'quiet': True,
        }

        if format_type == 'video':
            ydl_opts['format'] = f'bestvideo[height<={quality[:-1]}]+bestaudio/best'
            ext = 'mp4'
        else:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
            ext = 'mp3'

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            original_filename = ydl.prepare_filename(info)
            
            # Для аудио файл будет переименован в .mp3
            if format_type != 'video':
                original_filename = os.path.splitext(original_filename)[0] + '.mp3'
                if not os.path.exists(original_filename):
                    raise HTTPException(500, "Аудиофайл не был создан")

            safe_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in info['title'])
            download_filename = f"{safe_name}.{ext}"
            temp_filepath = temp_dir / download_filename
            
            shutil.copy2(original_filename, temp_filepath)
            
            # Проверяем, что файл действительно скопировался
            if not os.path.exists(temp_filepath):
                raise HTTPException(500, "Не удалось создать временный файл для отправки")

            response = FileResponse(
                temp_filepath,
                media_type='video/mp4' if format_type == 'video' else 'audio/mpeg',
                filename=download_filename
            )
            
            # Удаляем оригинальный файл
            try:
                os.remove(original_filename)
            except:
                pass
                
            return response
            
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        # Очистка старых временных файлов
        if download_filename:
            for file in temp_dir.glob('*'):
                if file.name != download_filename:
                    try:
                        file.unlink()
                    except:
                        pass