from PySide6.QtCore import QThread, Signal
from src.services.whisper_service import WhisperService

class TranscriptionThread(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, audio_path):
        super().__init__()
        self.audio_path = audio_path
        self.whisper = WhisperService()

    def run(self):
        try:
            result = self.whisper.transcribe(self.audio_path)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
