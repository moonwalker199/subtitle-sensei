# srt_extractor.py
import assemblyai as aai
from moviepy.editor import VideoFileClip
import os

def extract_subtitles(input_video_path, output_srt_path):
    """
    Extract subtitles from a video file using AssemblyAI
    
    Args:
        input_video_path (str): Path to input video file
        output_srt_path (str): Path where the SRT file should be saved
    """
    try:
        # Create temporary audio file path
        temp_dir = os.path.dirname(output_srt_path)
        temp_audio_path = os.path.join(temp_dir, 'temp_audio.wav')
        
        # Extract audio from video
        video = VideoFileClip(input_video_path)
        audio = video.audio
        audio.write_audiofile(temp_audio_path)
        
        # Configure AssemblyAI
        aai.settings.api_key = "c4e1282837f84e369a2a6a95a5209aa7"
        
        # Transcribe audio
        transcript = aai.Transcriber().transcribe(temp_audio_path)
        subtitles = transcript.export_subtitles_srt()
        
        # Write subtitles to file
        with open(output_srt_path, "w", encoding='utf-8') as f:
            f.write(subtitles)
        
        # Clean up temporary audio file
        try:
            os.remove(temp_audio_path)
        except Exception as e:
            print(f"Warning: Could not remove temporary audio file: {e}")
            
        # Close video file to free up resources
        video.close()
        
        return True
        
    except Exception as e:
        print(f"Error in extract_subtitles: {str(e)}")
        raise e


# If running directly (for testing)
# if __name__ == "__main__":
#     input_video = 'gladiator.mp4'
#     output_srt = 'subtitles.srt'
#     extract_subtitles(input_video, output_srt)