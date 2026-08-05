import ffmpeg

class FFmpegService:
    @staticmethod
    def burn_subtitles(video_path, subtitle_path, output_path, font_size=24, font_color="white"):
        # The subtitle filter in ffmpeg accepts ASS files and applies the styles defined within the ASS file.
        # Alternatively, we can pass style overrides here if needed.
        
        # Ensure paths are escaped correctly for ffmpeg
        # In a real scenario, this might need more robust path escaping
        escaped_subtitle_path = subtitle_path.replace(":", "\\:").replace("'", "\\'")
        
        try:
            (
                ffmpeg
                .input(video_path)
                .output(output_path, vf=f"subtitles='{escaped_subtitle_path}'")
                .run(overwrite_output=True)
            )
        except ffmpeg.Error as e:
            print(f"FFmpeg error: {e.stderr.decode()}")
            raise e
