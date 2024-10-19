import re
from datetime import datetime, timedelta

class SubtitleSync:
    def __init__(self):
        # Regular expression for matching SRT timestamp format (HH:MM:SS,mmm)
        self.time_pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})')
    
    def parse_time(self, time_str):
        """Convert SRT time string to timedelta object"""
        match = self.time_pattern.match(time_str)
        if match:
            hours, minutes, seconds, milliseconds = map(int, match.groups())
            return timedelta(hours=hours, minutes=minutes, 
                           seconds=seconds, milliseconds=milliseconds)
        return None

    def format_time(self, td):
        """Convert timedelta to SRT time format"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

    def parse_srt(self, srt_path):
        """Parse SRT file and return list of subtitle entries"""
        with open(srt_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        subtitles = []
        blocks = content.split('\n\n')
        
        for block in blocks:
            lines = block.split('\n')
            if len(lines) >= 3:
                times = lines[1].split(' --> ')
                start_time = self.parse_time(times[0])
                end_time = self.parse_time(times[1])
                text = '\n'.join(lines[2:])
                subtitles.append({
                    'index': int(lines[0]),
                    'start': start_time,
                    'end': end_time,
                    'text': text
                })
        
        return subtitles

    def apply_offset(self, subtitles, offset_seconds):
        """Apply time offset to subtitles"""
        offset = timedelta(seconds=offset_seconds)
        for subtitle in subtitles:
            subtitle['start'] += offset
            subtitle['end'] += offset
        return subtitles

    def write_srt(self, subtitles, output_path):
        """Write synchronized subtitles to new SRT file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitles, 1):
                f.write(f"{i}\n")
                f.write(f"{self.format_time(subtitle['start'])} --> {self.format_time(subtitle['end'])}\n")
                f.write(f"{subtitle['text']}\n\n")

    def sync_subtitles(self, input_srt_path, output_srt_path, offset_seconds):
        """Main function to synchronize subtitles with a given offset"""
        # Parse subtitle file
        subtitles = self.parse_srt(input_srt_path)
        
        # Apply offset to subtitles
        synced_subtitles = self.apply_offset(subtitles, offset_seconds)
        
        # Write synchronized subtitles to new file
        self.write_srt(synced_subtitles, output_srt_path)
        
        return offset_seconds

def main():
    # Example usage
    syncer = SubtitleSync()
    
    # Input and output paths
    input_srt = "input_subtitles.srt"
    output_srt = "synchronized_subtitles.srt"
    
    # Offset in seconds (positive for delay, negative for advance)
    offset_seconds = 2.5  # Example: delay subtitles by 2.5 seconds
    
    try:
        syncer.sync_subtitles(input_srt, output_srt, offset_seconds)
        print(f"Subtitles synchronized successfully!")
        print(f"Applied offset: {offset_seconds} seconds")
        print(f"Output written to: {output_srt}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()