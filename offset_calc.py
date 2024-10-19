import re
import datetime

def synchronize_srt(file1, file2, output_file):
    # Read the files
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    # Parse timestamps
    def parse_timestamp(line):
        match = re.search(r'\d+:\d+:\d+,\d+', line)
        return match.group(0) if match else None

    # Compare and adjust timestamps
    offset = 0
    adjusted_lines = []
    for line1, line2 in zip(lines1, lines2):
        timestamp1 = parse_timestamp(line1)
        timestamp2 = parse_timestamp(line2)
        if timestamp1 and timestamp2:
            diff = (datetime.datetime.strptime(timestamp1, '%H:%M:%S,%f') - datetime.datetime.strptime(timestamp2, '%H:%M:%S,%f')).total_seconds() * 1000
            offset += diff
            adjusted_timestamp = datetime.datetime.strptime(timestamp1, '%H:%M:%S,%f') + datetime.timedelta(milliseconds=offset)
            adjusted_line = re.sub(r'\d+:\d+:\d+,\d+', adjusted_timestamp.strftime('%H:%M:%S,%f'), line2)
            adjusted_lines.append(adjusted_line)
        else:
            adjusted_lines.append(line2)

    # Write the synchronized file
    with open(output_file, 'w') as f:
        f.writelines(adjusted_lines)

    # Print the offset difference
    print(f"Offset difference: {offset} milliseconds")

# Usage example
file1 = 'incorrect.srt'     #incorrect wala
file2 = 'subtitles.srt'     #jo assembly ai se aa rha tha
output_file = 'synchronized.srt'     #final wala
synchronize_srt(file1, file2, output_file)
