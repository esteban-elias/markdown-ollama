import subprocess
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt


def append_human_message(message: str, history: str):
    return history + 'HUMAN: ' + message + '\n'


def append_ai_message(message: str, history: str):
    return history + 'AI: ' + message + '\n'


history = '''
Guidelines for this conversation:
- Provide short, precise and concise answers.
- If you do not find information, please be
honest and do not hallucinate information.
- You are "AI" an I am "HUMAN".
Now, let's start the conversation.
'''

command = sys.argv[1:-1]
first_prompt = sys.argv[-1]

history = append_human_message(first_prompt, history)

console = Console()

while True:
    try:
        # Start the subprocess with line buffering
        process = subprocess.Popen(
            command+[history], stdout=subprocess.PIPE, text=True)

        stdout, _ = process.communicate()

        print()
        console.print(Markdown(stdout))

        history = append_ai_message(stdout, history=history)

        prompt = Prompt.ask("[bold green]\n>>>[/bold green]")
        history = append_human_message(prompt, history=history)

    except (KeyboardInterrupt, EOFError):
        print('Goodbye!')
        break
