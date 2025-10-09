import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from coordinator import ResearchCoordinator

load_dotenv()

console = Console()


async def main() -> None:
    console.print("[bold cyan]Hello from deep-research![/bold cyan]")
    console.print(
        Panel(
            "[bold blue]This tool Performs in-depth research on any topic using Ai agents[/bold blue]"
        )
    )
    topic = Prompt.ask("[bold cyan]Enter a topic to research[/bold cyan]")
    if not topic.strip():
        console.print("[bold red]No topic provided. Exiting.[/bold red]")
        return
    console.print(f"[bold green]Researching topic:[/bold green] {topic}")

    research_coordinator = ResearchCoordinator(topic)
    report = await research_coordinator.research()
    for paragraph in report:
        console.print(paragraph)
        console.print()  # Add an extra newline for better readability


if __name__ == "__main__":
    asyncio.run(main())
