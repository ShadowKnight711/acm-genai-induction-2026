import subprocess
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt

from personas import PERSONAS

console = Console()
MODEL_NAME = "llama3.1:8b"
chat_history = []
 
def setup_ollama():
    
    console.print(f"[cyan]Checking/pulling Ollama model '{MODEL_NAME}'...[/cyan]")

    try:
        subprocess.run(["ollama", "pull", MODEL_NAME], check=True)
    except FileNotFoundError:
        console.print("[bold red]⚠️  Ollama Not Found[/bold red]")
        console.print("[bold red]Ollama is not installed or not on your PATH.[/bold red]")
        sys.exit(1)
    except subprocess.CalledProcessError:
        console.print("[bold red]Pull failed. 'ollama serve' running in another terminal[/bold red]")
        sys.exit(1)

    from langchain_ollama import ChatOllama
    return ChatOllama(model=MODEL_NAME, temperature=0.5)


def choose_persona():
    names = list(PERSONAS.keys())
    options = "\n".join(
        f"{i}. {name} - {PERSONAS[name]['tagline']}"
        for i, name in enumerate(names, start=1)
    )

    console.print("[bold magenta]Choose your persona mode[/bold magenta]")
    console.print(options)

    choice = Prompt.ask(
        "Enter choice",
        choices=[str(i) for i in range(1, len(names) + 1)],
        default="1",
    )
    return names[int(choice) - 1]


def build_messages(persona_name):
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

    messages = [SystemMessage(content=PERSONAS[persona_name]["system_prompt"])]
    for turn in chat_history:
        if turn["role"] == "user":
            messages.append(HumanMessage(content=turn["content"]))
        else:
            messages.append(AIMessage(content=turn["content"]))
    return messages


def is_exit_command(user_input):
    
    return user_input.strip().lower() in {"exit", "quit"}


def main():
    console.print("[bold cyan]India's Got Latent - Chatbot[/bold cyan]")
    console.print("[dim]Type 'exit' or 'quit' to leave the chat.[/dim]")

    llm = setup_ollama()
    persona_name = choose_persona()

    console.print(f"\n[bold green]{persona_name}![/bold green]\n")

    while True:
        user_input = Prompt.ask("[bold blue]You[/bold blue]")

        if is_exit_command(user_input):
            console.print("[yellow]Chat ended. 👋[/yellow]")
            break

        chat_history.append({"role": "user", "content": user_input})

        with console.status("[dim]Thinking ...[/dim]", spinner="dots"):
            response = llm.invoke(build_messages(persona_name))

        chat_history.append({"role": "assistant", "content": response.content})

        console.print(f"[bold green]{persona_name}[/bold green]")
        console.print(Markdown(response.content))
 
 
if __name__ == "__main__":
    main()