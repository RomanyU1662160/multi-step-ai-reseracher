from pydantic import BaseModel


class SearchResult(BaseModel):
    title: str
    href: str
    summary: str
