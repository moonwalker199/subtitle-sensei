# offset_calc.py
import re
import datetime

def synchronize_srt(incorrect_srt_path, reference_srt_path, output_srt_path):
    """
    Synchronize subtitles by calculating and applying time offsets
    
    Args:
        incorrect_srt_path (str): Path to the SRT file that needs timing adjustment
        reference_srt_path (str): Path to the reference SRT file (from AssemblyAI)
        output_srt_path (str): Path where the synchronized SRT file should be saved
    
    Returns:
        float: The calculated offset in milliseconds
    """
    try:
        # Read the files
        with open(incorrect_srt_path, 'r', encoding='utf-8') as f1, \
             open(reference_srt_path, 'r', encoding='utf-8') as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()

        # Parse timestamps
        def parse_timestamp(line):
            match = re.search(r'\d+:\d+:\d+,\d+', line)
            return match.group(0) if match else None

        # Compare and adjust timestamps
        offset = 0
        adjusted_lines = []
        
        # Make sure we don't exceed the length of either file
        for line1, line2 in zip(lines1[:len(lines2)], lines2):
            timestamp1 = parse_timestamp(line1)
            timestamp2 = parse_timestamp(line2)
            
            if timestamp1 and timestamp2:
                # Calculate time difference
                time1 = datetime.datetime.strptime(timestamp1, '%H:%M:%S,%f')
                time2 = datetime.datetime.strptime(timestamp2, '%H:%M:%S,%f')
                diff = (time1 - time2).total_seconds() * 1000
                
                offset += diff
                
                # Apply offset to timestamp
                adjusted_time = time1 + datetime.timedelta(milliseconds=offset)
                adjusted_line = re.sub(
                    r'\d+:\d+:\d+,\d+', 
                    adjusted_time.strftime('%H:%M:%S,%f')[:-3], 
                    line2
                )
                adjusted_lines.append(adjusted_line)
            else:
                adjusted_lines.append(line2)

        # Write the synchronized file
        with open(output_srt_path, 'w', encoding='utf-8') as f:
            f.writelines(adjusted_lines)

        return offset

    except Exception as e:
        print(f"Error in synchronize_srt: {str(e)}")
        raise e

# If running directly (for testing)
# if __name__ == "__main__":
#     file1 = 'incorrect.srt'
#     file2 = 'subtitles.srt'
#     output_file = 'synchronized.srt'
#     offset = synchronize_srt(file1, file2, output_file)
#     print(f"Offset difference: {offset} milliseconds")