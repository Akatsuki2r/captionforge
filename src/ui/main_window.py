from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, QLabel, QHeaderView)
from PySide6.QtCore import Qt
import tempfile
import os
from src.services.whisper_service import WhisperService
from src.services.subtitle_service import SubtitleService
from src.services.ffmpeg_service import FFmpegService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CaptionForge")
        self.setMinimumSize(900, 600)
        
        self.whisper = WhisperService()
        self.sub_service = SubtitleService()
        self.current_audio = None
        self.current_video = None

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Buttons layout
        self.button_layout = QHBoxLayout()
        self.load_audio_btn = QPushButton("Load Audio")
        self.load_audio_btn.clicked.connect(self.load_audio)
        self.load_video_btn = QPushButton("Load Video")
        self.load_video_btn.clicked.connect(self.load_video)
        self.generate_btn = QPushButton("Generate Captions")
        self.generate_btn.clicked.connect(self.generate_captions)
        self.burn_btn = QPushButton("Burn Subtitles")
        self.burn_btn.clicked.connect(self.burn_subtitles)
        
        self.button_layout.addWidget(self.load_audio_btn)
        self.button_layout.addWidget(self.load_video_btn)
        self.button_layout.addWidget(self.generate_btn)
        self.button_layout.addWidget(self.burn_btn)
        self.main_layout.addLayout(self.button_layout)

        # Caption editor table
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Start", "End", "Caption"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.table)

    def load_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Audio", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.current_audio = file_path
            print(f"Loaded audio: {file_path}")

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4)")
        if file_path:
            self.current_video = file_path
            print(f"Loaded video: {file_path}")

    def generate_captions(self):
        if not self.current_audio:
            return
        
        print("Generating captions...")
        transcription = self.whisper.transcribe(self.current_audio)
        chunks = self.sub_service.chunk_transcription(transcription)
        
        self.table.setRowCount(len(chunks))
        for row, chunk in enumerate(chunks):
            self.table.setItem(row, 0, QTableWidgetItem(str(round(chunk['start'], 2))))
            self.table.setItem(row, 1, QTableWidgetItem(str(round(chunk['end'], 2))))
            self.table.setItem(row, 2, QTableWidgetItem(chunk['text']))

    def burn_subtitles(self):
        if not self.current_video or self.table.rowCount() == 0:
            return
            
        print("Burning subtitles...")
        
        # Extract data from table
        chunks = []
        for row in range(self.table.rowCount()):
            chunks.append({
                'start': float(self.table.item(row, 0).text()),
                'end': float(self.table.item(row, 1).text()),
                'text': self.table.item(row, 2).text()
            })
        
        # Create temporary ASS file
        with tempfile.NamedTemporaryFile(suffix=".ass", delete=False) as temp_ass:
            temp_ass_path = temp_ass.name
            self.sub_service.export_ass(chunks, temp_ass_path)
            
        output_path = "output.mp4"
        
        # Burn subtitles
        FFmpegService.burn_subtitles(self.current_video, temp_ass_path, output_path)
        print(f"Video saved as {output_path}")
        
        # Cleanup
        os.remove(temp_ass_path)
