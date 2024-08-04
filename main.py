import subprocess
import re
import sys

def append_human_message(message: str, history: str):
    return history + 'HUMAN: ' + message + '\n'

def append_ai_message(message: str, history: str):
    return history + 'AI: ' + message + '\n'

def colorize_markdown(text):
    patterns = {
        r'\*\*(.*?)\*\*': '\033[1m' + r'\1' + '\033[0m',  # Bold
        r'\*(.*?)\*': '\033[3m' + r'\1' + '\033[0m',  # Italic
        r'`(.*?)`': '\033[4m' + r'\1' + '\033[0m',  # Inline code
    }
    for pattern, color_code in patterns.items():
        text = re.sub(pattern, color_code, text)
    return text

history = ''

command = sys.argv[1:-1]
first_prompt =  sys.argv[-1]

history = append_human_message(first_prompt, history)

while True:
    try:
        # Start the subprocess with line buffering
        process = subprocess.Popen(command+[history], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

        stdout = ''

        # Loop over the lines from the subprocess's stdout
        print()
        for line in process.stdout:
            line = line.strip()
            stdout += line + '\n'
            print(colorize_markdown(line))

        # Wait for the subprocess to finish
        process.wait()

        history = append_ai_message(stdout, history=history)

        prompt = input('>>> ')
        history = append_human_message(prompt, history=history)

    except KeyboardInterrupt or EOFError:
        print('Goodbye!')
        break
