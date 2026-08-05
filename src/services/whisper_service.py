from faster_whisper import WhisperModel
import os

class WhisperService:
    def __init__(self, model_size="small"):
        # Initializing the model. Using 'int8' for better performance on CPU
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Transcribe the audio
        segments, info = self.model.transcribe(audio_path, beam_size=5)
        
        # Return segments as a list of dictionaries for easier handling
        transcription = []
        for segment in segments:
            transcription.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            })
        return transcription
