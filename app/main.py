from fastapi import FastAPI, Query, HTTPException
from get_data_from_researchgate_query import get_researchgate_data
from get_data_from_linkedin_query import get_linkedin_data
from get_data_from_orcid_query import get_orcid_data
from pydantic import BaseModel

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

@app.get("/researchgatesearch", response_model=dict)
async def researchgate_search(query: str = Query(..., description="Search query for ResearchGate")):
    try:
        data = get_researchgate_data(query)
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching ResearchGate data: {str(e)}")

@app.get("/linkedinsearch", response_model=dict)
async def linkedin_search(query: str = Query(..., description="Search query for LinkedIn")):
    try:
        data = get_linkedin_data(query)
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching LinkedIn data: {str(e)}")

@app.get("/orcidsearch", response_model=dict)
async def orcid_search(query: str = Query(..., description="Search query for ORCID")):
    try:
        data = get_orcid_data(query)
        return data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error while fetching ORCID data: {str(e)}")

# Example test endpoint
@app.get("/")
def home():
    return {"message": "API is running. Use /researchgate, /linkedin or /orcid to query."}
