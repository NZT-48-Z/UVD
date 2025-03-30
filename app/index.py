html = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Video Downloader</title>
    <link rel="stylesheet" href="/static/css/styles.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
	
</head>
<body>
    <div class="container">
		<header>
			<div class="theme-icon" id="theme-toggle">
				<i class="fas fa-moon"></i>
			</div>
			<h1><i class="fab fa-youtube"></i> YouTube Video Downloader</h1>
			<p>Скачивайте видео и аудио с YouTube в высоком качестве</p>
		</header>

        <main>
            <div class="download-section">
                <div class="input-group">
                    <input type="text" id="video-url" placeholder="Введите URL YouTube видео..." required>
                    <button id="fetch-btn"><i class="fas fa-search"></i> Найти</button>
                </div>
                
                <div class="video-info" id="video-info" style="display: none;">
                    <div class="thumbnail-container">
                        <img id="video-thumbnail" src="" alt="Video Thumbnail">
                        <div class="video-details">
                            <h3 id="video-title"></h3>
                            <p><i class="far fa-clock"></i> <span id="video-duration"></span></p>
                            <p><i class="fas fa-eye"></i> <span id="video-views"></span> просмотров</p>
                        </div>
                    </div>
                    
                    <div class="download-options">
                        <h3><i class="fas fa-download"></i> Варианты загрузки:</h3>
                        
                        <div class="format-selection">
                            <div class="format-tabs">
                                <button class="format-tab active" data-format="video">Видео</button>
                                <button class="format-tab" data-format="audio">Только аудио</button>
                            </div>
                            
                            <div class="quality-options" id="video-quality-options">
                                <h4>Выберите качество:</h4>
                                <div class="quality-buttons" id="video-quality-buttons">
                                    <!-- Quality options will be populated by JS -->
                                </div>
                            </div>
                            
                            <div class="quality-options" id="audio-quality-options" style="display: none;">
                                <h4>Выберите качество аудио:</h4>
                                <div class="quality-buttons" id="audio-quality-buttons">
                                    <!-- Audio quality options will be populated by JS -->
                                </div>
                            </div>
                        </div>
                        
                        <button id="download-btn" disabled><i class="fas fa-cloud-download-alt"></i> Скачать</button>
                    </div>
                </div>
            </div>
            
            <div class="how-to-use">
                <h2><i class="fas fa-question-circle"></i> Как использовать:</h2>
                <ol>
                    <li>Вставьте URL YouTube видео в поле выше</li>
                    <li>Нажмите кнопку "Найти"</li>
                    <li>Выберите желаемый формат и качество</li>
                    <li>Нажмите "Скачать" для загрузки файла</li>
                </ol>
            </div>
        </main>
        
        <footer>
            <p>© 2025 YouTube Video Downloader. Это инструмент предназначен только для личного использования.</p>
        </footer>
    </div>
    
    <div class="loading-overlay" id="loading-overlay">
        <div class="loading-spinner"></div>
        <p>Обработка запроса...</p>
    </div>
    
    <script src="/static/js/script.js"></script>
</body>
</html>
'''