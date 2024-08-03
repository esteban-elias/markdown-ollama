import subprocess
import re
import sys

command = sys.argv[1:]

def colorize_markdown(text):
    # Define markdown syntax patterns and their corresponding color codes
    patterns = {
        r'\*\*(.*?)\*\*': '\033[1m' + r'\1' + '\033[0m',  # Bold
        r'\*(.*?)\*': '\033[3m' + r'\1' + '\033[0m',  # Italic
        r'`(.*?)`': '\033[4m' + r'\1' + '\033[0m',  # Inline code
    }

    # Apply each pattern
    for pattern, color_code in patterns.items():
        text = re.sub(pattern, color_code, text)

    return text

# Start the subprocess with line buffering
process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

# Loop over the lines from the subprocess's stdout
for line in process.stdout:
    line = line.strip()
    print(colorize_markdown(line))

# Wait for the subprocess to finish
process.wait()
