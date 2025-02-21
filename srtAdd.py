import re

def add_punctuation_to_text(input_file, output_file):
    # Open the input SRT file
    with open(input_file, 'r', encoding='utf-8') as file:
        srt_content = file.read()
    
    # Regular expression to match the sequence numbers and timestamps
    pattern = r'(\d+\s*\n|\d{2}:\d{2}:\d{2},\d{3}\s*-->.*\n)'
    
    # Remove the matched sequences (numbers and timestamps)
    cleaned_content = re.sub(pattern, '', srt_content)
    
    # Split the content into lines and clean up any extra spaces
    lines = [line.strip() for line in cleaned_content.split('\n') if line.strip()]

    # Add punctuation to each line (comma for most, period for the last line)
    for i in range(len(lines)):
        if i < len(lines) - 1:
            lines[i] += ','  # Add comma for all except the last line
        else:
            lines[i] += '.'  # Add period for the last line
    
    # Join the lines back together into a string
    final_content = '\n\n'.join(lines)
    
    # Write the final content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(final_content)

# Example usage
input_file = './output.srt'  # Replace with the path to your input SRT file
output_file = 'output_with_punctuation.srt'  # Replace with the path for the output file

add_punctuation_to_text(input_file, output_file)
