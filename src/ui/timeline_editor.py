import wave
import struct
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRect, QSize
from PySide6.QtGui import QPainter, QPen, QColor

class TimelineEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 150)
        self.audio_data = []
        self.subtitle_blocks = [] # List of dicts: {'start', 'end', 'text', 'rect'}

    def load_audio(self, audio_path):
        # Simplistic waveform extraction using wave
        with wave.open(audio_path, 'rb') as wav:
            frames = wav.readframes(wav.getnframes())
            # Unpack frames to integers (assuming 16-bit mono)
            self.audio_data = struct.unpack(f"{len(frames)//2}h", frames)[::100] # Downsample
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#1e1e1e"))
        
        # Draw Waveform
        if not self.audio_data: return
        
        pen = QPen(QColor("#404040"), 1)
        painter.setPen(pen)
        
        mid = self.height() // 2
        max_val = max(abs(x) for x in self.audio_data) if self.audio_data else 1
        
        for i, val in enumerate(self.audio_data):
            x = (i / len(self.audio_data)) * self.width()
            h = (val / max_val) * mid
            painter.drawLine(int(x), mid - int(h), int(x), mid + int(h))

        # Draw Subtitle Blocks
        pen = QPen(QColor("#007acc"), 2)
        painter.setPen(pen)
        brush = QColor(0, 122, 204, 100)
        painter.setBrush(brush)
        
        for block in self.subtitle_blocks:
            # Need to map time to x-coordinates
            # For now, placeholder drawing
            rect = QRect(int(block['start'] * 10), 10, int((block['end'] - block['start']) * 10), 30)
            block['rect'] = rect
            painter.drawRect(rect)
