document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const videoUrlInput = document.getElementById('video-url');
    const fetchBtn = document.getElementById('fetch-btn');
    const videoInfoSection = document.getElementById('video-info');
    const videoThumbnail = document.getElementById('video-thumbnail');
    const videoTitle = document.getElementById('video-title');
    const videoDuration = document.getElementById('video-duration');
    const videoViews = document.getElementById('video-views');
    const videoQualityOptions = document.getElementById('video-quality-options');
    const videoQualityButtons = document.getElementById('video-quality-buttons');
    const audioQualityOptions = document.getElementById('audio-quality-options');
    const audioQualityButtons = document.getElementById('audio-quality-buttons');
    const downloadBtn = document.getElementById('download-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const formatTabs = document.querySelectorAll('.format-tab');

    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('theme') || 'light';
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        updateThemeIcon(true);
    }
    themeToggle.addEventListener('click', function() {
        const isDark = document.body.classList.toggle('dark-theme');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        updateThemeIcon(isDark);
    });

    function updateThemeIcon(isDark) {
        const icon = themeToggle.querySelector('i');
        if (isDark) {
            icon.classList.remove('fa-moon');
            icon.classList.add('fa-sun');
        } else {
            icon.classList.remove('fa-sun');
            icon.classList.add('fa-moon');
        }
    }
    
    // Current selected format and quality
    let currentFormat = 'video';
    let currentQuality = null;
    let videoData = null;
    
    // Event Listeners
    fetchBtn.addEventListener('click', fetchVideoInfo);
    downloadBtn.addEventListener('click', downloadVideo);
    
    // Format tab switching
    formatTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            formatTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            currentFormat = this.dataset.format;
            
            if (currentFormat === 'video') {
                videoQualityOptions.style.display = 'block';
                audioQualityOptions.style.display = 'none';
                if (videoData && videoData.videoQualities.length > 0) {
                    currentQuality = videoData.videoQualities[1].quality; // Default to 720p
                    updateQualityButtons();
                }
            } else {
                videoQualityOptions.style.display = 'none';
                audioQualityOptions.style.display = 'block';
                if (videoData && videoData.audioQualities.length > 0) {
                    currentQuality = videoData.audioQualities[0].quality;
                    updateQualityButtons();
                }
            }
            updateDownloadButton();
        });
    });
    
    // Fetch video info from YouTube
    async function fetchVideoInfo() {
        const url = videoUrlInput.value.trim();
        
        if (!url) {
            alert('Пожалуйста, введите URL YouTube видео');
            return;
        }
        
        if (!isValidYouTubeUrl(url)) {
            alert('Пожалуйста, введите корректный URL YouTube видео');
            return;
        }
        
        showLoading(true);
        
        try {
            const response = await fetch(`/video-info?url=${encodeURIComponent(url)}`);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Ошибка сервера');
            }
            
            const data = await response.json();
            
            // Формируем список доступных качеств
            const videoQualities = [
                { quality: "1080p", format: "MP4" },
                { quality: "720p", format: "MP4" },
                { quality: "480p", format: "MP4" }
            ];
            
            videoData = {
                ...data,
                videoQualities: videoQualities,
                audioQualities: [
                    { quality: "Высокое", format: "MP3" },
                    { quality: "Среднее", format: "MP3" }
                ]
            };
            
            displayVideoInfo(videoData);
            videoInfoSection.style.display = 'block';
            
            currentFormat = 'video';
            currentQuality = '720p'; // качество по умолчанию
            updateQualityButtons();
            updateDownloadButton();
            
        } catch (error) {
            console.error('Error fetching video info:', error);
            alert(error.message);
        } finally {
            showLoading(false);
        }
    }
    
    // Display video information
    function displayVideoInfo(data) {
        videoThumbnail.src = data.thumbnail;
        videoTitle.textContent = data.title;
        videoDuration.textContent = formatDuration(data.duration);
        videoViews.textContent = formatViews(data.views);
        
        // Populate video quality options
        videoQualityButtons.innerHTML = '';
        data.videoQualities.forEach(quality => {
            const button = document.createElement('button');
            button.className = 'quality-btn';
            button.textContent = `${quality.quality} (${quality.format})`;
            button.dataset.quality = quality.quality;
            button.addEventListener('click', () => {
                currentQuality = quality.quality;
                updateQualityButtons();
                updateDownloadButton();
            });
            videoQualityButtons.appendChild(button);
        });
        
        // Populate audio quality options
        audioQualityButtons.innerHTML = '';
        data.audioQualities.forEach(quality => {
            const button = document.createElement('button');
            button.className = 'quality-btn';
            button.textContent = `${quality.quality} (${quality.format})`;
            button.dataset.quality = quality.quality;
            button.addEventListener('click', () => {
                currentQuality = quality.quality;
                updateQualityButtons();
                updateDownloadButton();
            });
            audioQualityButtons.appendChild(button);
        });
    }
    
    // Update quality buttons to show selected state
    function updateQualityButtons() {
        const buttons = document.querySelectorAll('.quality-btn');
        buttons.forEach(button => {
            if (button.dataset.quality === currentQuality) {
                button.classList.add('selected');
            } else {
                button.classList.remove('selected');
            }
        });
    }
    
    // Enable/disable download button based on selection
    function updateDownloadButton() {
        downloadBtn.disabled = !currentQuality;
    }
    
    // Download video
    async function downloadVideo() {
        if (!videoData || !currentQuality) return;
        
        showLoading(true, "Идет загрузка...");
        
        try {
            const params = new URLSearchParams({
                url: videoData.url,
                format_type: currentFormat,
                quality: currentQuality
            });
            
            // Открываем в новой вкладке для скачивания
            window.open(`/download?${params.toString()}`, '_blank');
            
        } catch (error) {
            console.error('Error downloading video:', error);
            alert('Ошибка при загрузке: ' + error.message);
        } finally {
            showLoading(false);
        }
    }
    
    // Helper functions
    function isValidYouTubeUrl(url) {
        const pattern = /^(https?:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$/;
        return pattern.test(url);
    }
    
    function formatDuration(seconds) {
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }
    
    function formatViews(views) {
        return views.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }
    
    function showLoading(show, message = "Загрузка...") {
        if (message) {
            loadingOverlay.querySelector('p').textContent = message;
        }
        loadingOverlay.style.display = show ? 'flex' : 'none';
    }
});