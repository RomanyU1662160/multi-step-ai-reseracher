import re
import time
from typing import final
from agents import Runner, trace
from rich.console import Console
from rich.panel import Panel
from models import SearchResult
from research_agents.report_agent import report_agent
from research_agents.search_agent import search_agent
from research_agents.query_agent import query_agent, QueryResponse
from ddgs import DDGS

console = Console()


class ResearchCoordinator:
    def __init__(self, query: str):
        self.query = query
        self.search_results: list[SearchResult] = []

    async def research(self) -> list[str]:
        with trace("Deep research"):
            query_agent_response = await self.call_query_agent_to_generate_queries()
            # Further steps would go here, such as using the generated queries to search for information
            search_queries = query_agent_response.queries
            await self.perform_search_for_queries(search_queries)
            final_report = await self.generate_report()
            return final_report

    async def call_query_agent_to_generate_queries(self) -> QueryResponse:
        with console.status(
            "[bold cyan] Analyzing Queries... [/bold cyan]", refresh_per_second=4
        ):
            result = await Runner.run(query_agent, input=self.query)
            console.print(Panel("[bold cyan] Query Analysis [/bold cyan]"))
            console.print(
                f"[bold yellow] Thoughts:: [/bold yellow] {result.final_output.thoughts}"
            )
            console.print("\n [yellow] Generated Search Queries:: [/yellow]")
            for i, query in enumerate(result.final_output.queries):
                console.print(f" - {i + 1}. {query}")
            return result.final_output

    async def perform_duck_duck_go_search(self, query: str) -> list[dict[str, str]]:
        try:
            results = DDGS().text(
                query, region="uk-en", safesearch="on", timelimit="n", max_results=2
            )
            return results

        except Exception as ex:
            console.print(f"[bold red] DuckDuckGo Search Error: {ex} [/bold red]")
            return []

    async def perform_search_for_queries(self, queries: list[str]):
        with console.status("[bold cyan] Performing Search... [/bold cyan]"):
            all_search_results = {}
            for query in queries:
                console.print(f"\n[bold cyan] Searching for: {query} [/bold cyan]")
                search_result = await self.perform_duck_duck_go_search(
                    query
                )  # will return list of dict with title, href, body according to the max_results param
                all_search_results[query] = search_result
                console.print(
                    f"\n[green] Found {len(search_result)} results for '{query}' [/green]"
                )

            for query in queries:
                console.print(
                    Panel(f"[bold cyan] Search Results for: {query} [/bold cyan]")
                )
                for result in all_search_results.get(query, []):
                    title = result.get("title", "No Title")
                    href = result.get("href", "No URL")
                    console.print(f" - {title}: {href}")
                    search_query_input = f"{title} {href}"
                    start_analysis_time = time.time()
                    # give the title and href to the search agent, to summarize the content of the page
                    agent_result = await Runner.run(
                        search_agent, input=search_query_input
                    )
                    end_analysis_time = time.time()
                    analysis_duration = end_analysis_time - start_analysis_time
                    console.print(
                        f"[dim] Analysis took {analysis_duration:.2f} seconds [/dim]"
                    )

                    #  print the final output of the search agent
                    console.print(f"[green]{agent_result.final_output}[/green]\n")

                    #  create a SearchResult object and append it to the search_results list
                    search_result = SearchResult(
                        title=title, href=href, summary=agent_result.final_output
                    )
                    self.search_results.append(search_result)
            console.print(
                f"[bold green] Research Complete! [/bold green], found {len(self.search_results)} total results across {len(queries)} queries."
            )

    async def generate_report(self) -> list[str]:
        original_topic = self.query
        topic_search_results = self.search_results
        collective_summary = "\n\n".join(
            [
                f"### {res.title}\n{res.summary}\nSource: [{res.title}]({res.href})"
                for res in topic_search_results
            ]
        )
        report_input = f"Original Topic: {original_topic}\n\nSearch Results Summaries:\n\n{collective_summary}"
        with console.status("[bold cyan] Generating Report... [/bold cyan]"):
            result = await Runner.run(report_agent, input=report_input)

            return result.final_output.split("\n\n")
