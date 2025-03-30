# UVD — YouTube Video & Audio Downloader API
### 🚀 Быстрый и легкий API для скачивания видео и аудио с YouTube

UVD — это высокопроизводительный REST API, построенный на FastAPI и yt-dlp, который позволяет легко загружать видео и аудио с YouTube в различных форматах.

### 🔥 Возможности
✅ Скачивание видео в MP4(HD, Full HD) \
✅ Извлечение аудио в MP3 \
✅ Простое API с минимальными зависимостями \
✅ Асинхронная загрузка с высокой скоростью 

### 📦 Установка

#### 1. Клонируйте репозиторий:
```bash
git clone https://github.com/NZT-48-Z/UVD.git
cd uvd
```
#### 2. Установка FFmpeg

#### Для Windows:
1. Скачайте [FFmpeg](https://www.gyan.dev/ffmpeg/builds/)
2. Распакуйте архив в папку `ffmpeg` в корне проекта
3. Добавьте путь `.\ffmpeg\bin` в системную переменную PATH

#### Для Linux/macOS:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y ffmpeg

# macOS (с Homebrew)
brew install ffmpeg
```
#### 3. Установите зависимости:
```bash
pip install -e .
```

#### 4. Запустите main.py:
```bash
python main.py
```
