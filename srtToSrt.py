'''
Author: Diana Tang
Date: 2025-02-20 22:34:05
LastEditors: Diana Tang
Description: some description
FilePath: /add-srt-compress-video/srtToSrt.py
'''
import re

def remove_srt_timestamps_and_sequence(input_file, output_file):
    # Open the input SRT file
    with open(input_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    # Regular expression to match the sequence numbers and timestamps
    pattern = r'(\d+\s*\n|\d{2}:\d{2}:\d{2},\d{3}\s*-->.*\n)'
    
    # Remove the matched sequences (numbers and timestamps)
    cleaned_content = re.sub(pattern, '', srt_content)
    
    # Write the cleaned content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_content.strip())

# Example usage
input_file = './videos/[3.1]--前端工程化Linux预备知识.srt'  # Replace with the path to your input SRT file
output_file = './output.srt'  # Replace with the path for the output file

remove_srt_timestamps_and_sequence(input_file, output_file)
