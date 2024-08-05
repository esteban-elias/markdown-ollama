import subprocess
import sys
from rich.console import Console
from rich.markdown import Markdown


def append_human_message(message: str, history: str):
    return history + 'HUMAN: ' + message + '\n'


def append_ai_message(message: str, history: str):
    return history + 'AI: ' + message + '\n'


history = ''

command = sys.argv[1:-1]
first_prompt = sys.argv[-1]

history = append_human_message(first_prompt, history)

console = Console()

while True:
    # write to history.txt
    with open('history.txt', 'w') as f:
        f.write(history)
    try:
        # Start the subprocess with line buffering
        process = subprocess.Popen(
            command+[history], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True)

        stdout = ''

        # Loop over the lines from the subprocess's stdout
        print()
        for line in process.stdout:
            line = line.strip()
            stdout += line + '\n'

        console.print(Markdown(stdout))

        # Wait for the subprocess to finish
        process.wait()

        history = append_ai_message(stdout, history=history)

        prompt = input('\n>>> ')
        history = append_human_message(prompt, history=history)

    except KeyboardInterrupt or EOFError:
        print('Goodbye!')
        break
