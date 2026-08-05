from PySide6.QtCore import QThread, Signal
from src.services.ffmpeg_service import FFmpegService

class BurnThread(QThread):
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, video_path, subtitle_path, output_path):
        super().__init__()
        self.video_path = video_path
        self.subtitle_path = subtitle_path
        self.output_path = output_path

    def run(self):
        try:
            FFmpegService.burn_subtitles(self.video_path, self.subtitle_path, self.output_path)
            self.finished.emit(self.output_path)
        except Exception as e:
            self.error.emit(str(e))
