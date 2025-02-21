'''
Author: Diana Tang
Date: 2025-02-20 23:14:52
LastEditors: Diana Tang
Description: some description
FilePath: /add-srt-compress-video/batchSrt.py
'''
import re
import os

def remove_srt_timestamps_and_sequence(input_srt):
    """
    Removes sequence numbers and timestamps from SRT content.
    """
    pattern = r'(\d+\s*\n|\d{2}:\d{2}:\d{2},\d{3}\s*-->.*\n)'
    return re.sub(pattern, '', input_srt).strip()

def add_punctuation_to_text(cleaned_content):
    """
    Adds punctuation to each line of cleaned SRT content.
    Adds commas for all lines except the last, and a period for the last line.
    """
    lines = [line.strip() for line in cleaned_content.split('\n') if line.strip()]
    
    for i in range(len(lines)):
        if i < len(lines) - 1:
            lines[i] += ','  # Add comma for all except the last line
        else:
            lines[i] += '.'  # Add period for the last line
    
    return '\n\n'.join(lines)

def process_srt_file(input_file, output_file):
    """
    Processes an individual SRT file: removes timestamps/sequence and adds punctuation.
    """
    with open(input_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()

    # Remove timestamps and sequence numbers
    cleaned_content = remove_srt_timestamps_and_sequence(srt_content)
    
    # Add punctuation
    final_content = add_punctuation_to_text(cleaned_content)

    # Write the processed content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(final_content)

def batch_process_srt_files(input_folder, output_folder):
    """
    Processes all SRT files in a specified input folder and saves to the output folder.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate over all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.srt'):  # Process only .srt files
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)
            
            # Process the file and save the result to the output folder
            process_srt_file(input_file, output_file)
            print(f"Processed: {filename}")

# Example usage
input_folder = 'v1'  # Replace with the path to your input folder containing .srt files
output_folder = 'vv'  # Replace with the path to your output folder where processed files will be saved

batch_process_srt_files(input_folder, output_folder)
