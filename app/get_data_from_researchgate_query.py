from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI()

API_KEY = open('api_key').read()
CSE_ID = open('search_engine_id').read()


class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    displayLink: str
    formattedUrl: str
    browse_type: str

def determine_researchgate_browse_type(link: str) -> str:
    """Insert type info based on the string link"""
    if "profile" in link:
        return "profile"
    elif "publication" in link:
        return "publication"
    elif "journal" in link:
        return "journal"
    else:
        return "unknown"

@app.get("/search", response_model=list[SearchResult])
async def search(query: str = Query(..., min_length=1, description="Query for browser")):
    """
    Browse for results in google with structure: LinkedIn: keywords...'
    """
    full_query = f"ResearchGate: {query}"

    try:
        # Query to Google Custom Search JSON API
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": API_KEY,
                "cx": CSE_ID,
                "q": full_query,
            }
        )
        response.raise_for_status()  # error handling

        data = response.json()

        # get results
        results = []
        for item in data.get("items", []):
            link = item.get("link", "No link")
            result = SearchResult(
                title=item.get("title", "No title"),
                link=link,
                snippet=item.get("snippet", "No snippet"),
                displayLink=item.get("displayLink", "No displaylink"),
                formattedUrl=item.get("formattedUrl", "No formattedurl"),
                browse_type=determine_researchgate_browse_type(link),
            )
            results.append(result)
        return results

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Following error while browsing happened: {str(e)}")


# testing endpoint
@app.get("/")
def home():
    return {"message": "API działa. Użyj /search?q=twoje_zapytanie"}
