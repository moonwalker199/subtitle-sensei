import re
import datetime

def synchronize_srt(incorrect_srt_path, reference_srt_path, output_srt_path):
    """
    Synchronize subtitles by calculating and applying time offsets
    
    Args:
        incorrect_srt_path (str): Path to the SRT file that needs timing adjustment
        reference_srt_path (str): Path to the reference SRT file (from AssemblyAI)
        output_srt_path (str): Path where the synchronized SRT file should be saved
    """
    try:
        # Read the files
        with open(incorrect_srt_path, 'r', encoding='utf-8') as f1, \
             open(reference_srt_path, 'r', encoding='utf-8') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        # Parse timestamps from a line with both start and end timestamps
        def parse_timestamps(line):
            matches = re.findall(r'\d+:\d+:\d+,\d+', line)
            return matches if matches else None

        # Helper function to adjust timestamp with given offset
        def adjust_timestamp(timestamp, offset):
            time = datetime.datetime.strptime(timestamp, '%H:%M:%S,%f')
            adjusted_time = time + datetime.timedelta(milliseconds=offset)
            return adjusted_time.strftime('%H:%M:%S,%f')[:-3]

        # Adjust timestamps for each subtitle entry
        adjusted_lines = []
        
        for line1, line2 in zip(lines1, lines2):
            timestamps1 = parse_timestamps(line1)
            timestamps2 = parse_timestamps(line2)
            
            if timestamps1 and timestamps2 and len(timestamps1) == 2 and len(timestamps2) == 2:
                # Calculate time difference for start time
                start_time1 = datetime.datetime.strptime(timestamps1[0], '%H:%M:%S,%f')
                start_time2 = datetime.datetime.strptime(timestamps2[0], '%H:%M:%S,%f')
                diff_start = (start_time2 - start_time1).total_seconds() * 1000  # Difference in milliseconds
                
                # Calculate time difference for end time
                end_time1 = datetime.datetime.strptime(timestamps1[1], '%H:%M:%S,%f')
                end_time2 = datetime.datetime.strptime(timestamps2[1], '%H:%M:%S,%f')
                diff_end = (end_time2 - end_time1).total_seconds() * 1000  # Difference in milliseconds
                
                # Adjust start and end timestamps with calculated offsets
                adjusted_start_time = adjust_timestamp(timestamps1[0], diff_start)
                adjusted_end_time = adjust_timestamp(timestamps1[1], diff_end)
                adjusted_line = re.sub(
                    r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', 
                    f"{adjusted_start_time} --> {adjusted_end_time}",
                    line1
                )
                adjusted_lines.append(adjusted_line)
            else:
                adjusted_lines.append(line1)

        # Write the synchronized file
        with open(output_srt_path, 'w', encoding='utf-8') as f:
            f.writelines(adjusted_lines)

    except Exception as e:
        print(f"Error in synchronize_srt: {str(e)}")
        raise e