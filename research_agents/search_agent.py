from agents import Agent, function_tool
import requests
from bs4 import BeautifulSoup
from typing import List

SEARCH_AGENT_PROMT = """
You are a research assistant. Given a URL and its title, you will analyze the content of the URL
and produce a concise summary of the information. The summary must be 2-3 paragraphs.
Capture the main points. Write succinctly, no need to have complete sentences or perfect 
grammar. This will be consumed by someone synthesizing a report,
so it's vital you capture the essence and ignore any fluff. Do not include any additional commentary other than the summary "
itself.
"""


@function_tool
def url_to_text(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return ""
    cleaned_text = ""
    soup = BeautifulSoup(
        response.text, "html.parser"
    )  # Parse the HTML content using BeautifulSoup
    for script in soup(
        ["script", "style"]
    ):  # Removes all <script> and <style> tags since they contain code/styling rather than readable content
        script.extract()
        text = soup.get_text(
            separator=" ", strip=True
        )  # Extracts the text from the HTML, using a space as a separator and stripping leading/trailing whitespace
        splitted_lines = text.splitlines()  # Splits the text into individual lines
        chunks = []
        for line in splitted_lines:
            for phrase in line.split(
                "  "
            ):  # Further splits each line into phrases based on double spaces
                if phrase:
                    chunks.append(phrase.strip())
        cleaned_text = " ".join(
            chunk for chunk in chunks if chunk
        )  # Joins the cleaned phrases back into a single string with newlines separating them
    return cleaned_text[:1000] if len(cleaned_text) > 1000 else cleaned_text


search_agent = Agent(
    model="gpt-5-nano",
    name="Search Agent",
    instructions=SEARCH_AGENT_PROMT,
    tools=[url_to_text],
)
