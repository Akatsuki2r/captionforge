from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QTableWidget, QTableWidgetItem, QFileDialog, 
                               QHeaderView, QProgressDialog, QMessageBox)
from PySide6.QtCore import Qt
import tempfile
import os
from src.services.subtitle_service import SubtitleService
from src.ui.transcription_thread import TranscriptionThread
from src.ui.burn_thread import BurnThread

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CaptionForge")
        self.setMinimumSize(900, 600)
        
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
            self.statusBar().showMessage(f"Loaded audio: {os.path.basename(file_path)}")

    def load_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4)")
        if file_path:
            self.current_video = file_path
            self.statusBar().showMessage(f"Loaded video: {os.path.basename(file_path)}")

    def generate_captions(self):
        if not self.current_audio:
            QMessageBox.warning(self, "Warning", "Please load an audio file first.")
            return
        
        self.progress = QProgressDialog("Transcribing... (This may take a while)", "Cancel", 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.show()
        
        self.transcription_thread = TranscriptionThread(self.current_audio)
        self.transcription_thread.finished.connect(self.on_transcription_finished)
        self.transcription_thread.error.connect(self.on_error)
        self.transcription_thread.start()

    def on_transcription_finished(self, transcription):
        self.progress.close()
        chunks = self.sub_service.chunk_transcription(transcription)
        self.table.setRowCount(len(chunks))
        for row, chunk in enumerate(chunks):
            self.table.setItem(row, 0, QTableWidgetItem(str(round(chunk['start'], 2))))
            self.table.setItem(row, 1, QTableWidgetItem(str(round(chunk['end'], 2))))
            self.table.setItem(row, 2, QTableWidgetItem(chunk['text']))
        self.statusBar().showMessage("Transcription completed.")

    def on_error(self, message):
        self.progress.close()
        QMessageBox.critical(self, "Error", message)

    def burn_subtitles(self):
        if not self.current_video or self.table.rowCount() == 0:
            QMessageBox.warning(self, "Warning", "Load a video and generate captions first.")
            return
            
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Video", "", "Video Files (*.mp4)")
        if not output_path:
            return

        # Extract data from table
        chunks = []
        for row in range(self.table.rowCount()):
            chunks.append({
                'start': float(self.table.item(row, 0).text()),
                'end': float(self.table.item(row, 1).text()),
                'text': self.table.item(row, 2).text()
            })
        
        # Create temporary ASS file
        self.temp_ass = tempfile.NamedTemporaryFile(suffix=".ass", delete=False)
        self.sub_service.export_ass(chunks, self.temp_ass.name)
            
        self.progress = QProgressDialog("Burning subtitles...", "Cancel", 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.show()
        
        self.burn_thread = BurnThread(self.current_video, self.temp_ass.name, output_path)
        self.burn_thread.finished.connect(self.on_burn_finished)
        self.burn_thread.error.connect(self.on_error)
        self.burn_thread.start()

    def on_burn_finished(self, output_path):
        self.progress.close()
        if os.path.exists(self.temp_ass.name):
            os.remove(self.temp_ass.name)
        QMessageBox.information(self, "Success", f"Video saved to {output_path}")
        self.statusBar().showMessage("Subtitle burning completed.")
