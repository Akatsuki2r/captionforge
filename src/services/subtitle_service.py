class SubtitleService:
    @staticmethod
    def chunk_transcription(transcription, words_per_chunk=3):
        """
        Groups the transcription segments into chunks of words.
        """
        chunks = []
        
        for segment in transcription:
            words = segment['text'].split()
            # Split words into groups
            for i in range(0, len(words), words_per_chunk):
                word_group = words[i:i + words_per_chunk]
                chunks.append({
                    "start": segment['start'], 
                    "end": segment['end'],
                    "text": " ".join(word_group)
                })
        return chunks

    @staticmethod
    def export_srt(chunks, output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(chunks):
                f.write(f"{i + 1}\n")
                f.write(f"{SubtitleService._format_time_srt(chunk['start'])} --> {SubtitleService._format_time_srt(chunk['end'])}\n")
                f.write(f"{chunk['text']}\n\n")

    @staticmethod
    def export_ass(chunks, output_path):
        header = "[Script Info]\nTitle: CaptionForge\nScriptType: v4.00+\n\n[V4+ Styles]\nStyle: Default,Arial,24,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,1,1,2,10,10,10,1\n\n[Events]\nFormat: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text\n"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(header)
            for chunk in chunks:
                start = SubtitleService._format_time_ass(chunk['start'])
                end = SubtitleService._format_time_ass(chunk['end'])
                f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{chunk['text']}\n")

    @staticmethod
    def _format_time_srt(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{int(seconds):02},{milliseconds:03}"

    @staticmethod
    def _format_time_ass(seconds):
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = seconds % 60
        return f"{hours}:{minutes:02}:{seconds:05.2f}"
