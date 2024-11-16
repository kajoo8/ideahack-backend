from fastapi import FastAPI, Query, HTTPException, Depends
from get_data_from_researchgate_query import determine_researchgate_browse_type
from get_data_from_linkedin_query import determine_linkedin_browse_type
from get_data_from_orcid_query import determine_orcid_browse_type
from pydantic import BaseModel
import requests
from openai import OpenAI

app = FastAPI()

API_KEY_GOOGLESEARCHENGINE = open('api_key').read()
CSE_ID_GOOGLESEARCHENGINE = open('search_engine_id').read()

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    displayLink: str
    formattedUrl: str
    browse_type: str


#==================== GOOGLE SEARCH ENGINE ENDPOINTS ====================#
@app.get("/researchgatesearch", response_model=list[SearchResult])
async def researchgate_search(query: str = Query(..., min_length=1, description="Search query for ResearchGate")):
    full_query = f"ResearchGate: {query}"

    try:
        # Query to Google Custom Search JSON API
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": API_KEY_GOOGLESEARCHENGINE,
                "cx": CSE_ID_GOOGLESEARCHENGINE,
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


@app.get("/linkedinsearch", response_model=list[SearchResult])
async def linkedin_search(query: str = Query(..., min_length=1, description="Search query for LinkedIn")):
    full_query = f"LinkedIn: {query}"

    try:
        # Query to Google Custom Search JSON API
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": API_KEY_GOOGLESEARCHENGINE,
                "cx": CSE_ID_GOOGLESEARCHENGINE,
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
                browse_type=determine_linkedin_browse_type(link),
            )
            results.append(result)
        return results

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Following error while browsing happened: {str(e)}")


@app.get("/orcidsearch", response_model=list[SearchResult])
async def orcid_search(query: str = Query(..., min_length=1, description="Search query for ORCID")):
    full_query = f"Orcid: {query}"

    try:
        # Query to Google Custom Search JSON API
        response = requests.get(
            "https://www.googleapis.com/customsearch/v1",
            params={
                "key": API_KEY_GOOGLESEARCHENGINE,
                "cx": CSE_ID_GOOGLESEARCHENGINE,
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
                browse_type=determine_orcid_browse_type(link),
            )
            results.append(result)
        return results

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Following error while browsing happened: {str(e)}")


#==================== LLM ENDPOINTS ====================#
def get_chatgpt_response(prompt: str) -> str:
    client = OpenAI(api_key=open('chatgpt_api_key').read(),)

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user", "content": prompt,
                }
            ],
            model="gpt-4o",
        )
        content = chat_completion.choices[0].message.content
        return content

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred while asking LLM for a keywords: {e}")

# Class for validating input data for post method
class PromptRequest(BaseModel):
    prompt: str

# POST METHOD FOR PROMPTING
@app.post("/chatgpt/")
async def chatgpt(
    request: PromptRequest
):
    # Get the answer in a string
    answer = get_chatgpt_response(request.prompt)
    
    # Format the answer from LLM
    formatted_query = answer.replace(",", "").replace(" ", "+")

    try:
        orcid_results = await orcid_search(query=formatted_query)
        linkedin_results = await linkedin_search(query=formatted_query)
        researchgate_results = await researchgate_search(query=formatted_query)
        
        # print(orcid_results)
        # print(linkedin_results)
        # print(researchgate_results)
        return {
            "orcid": orcid_results,
            "linkedin": linkedin_results,
            "researchgate": researchgate_results,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error occurred during searches: {e}")


#==================== TEST ENDPOINTS ====================#
@app.get("/")
def home():
    return {"message": "API is running. Use /researchgatesearch?query=, /linkedinsearch?query= or /orcidsearch?query= to query."}
