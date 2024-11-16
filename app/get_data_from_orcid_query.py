import re
import requests

class SearchResult:
    def __init__(self, title, link, snippet, displayLink, formattedUrl, browse_type):
        self.title = title
        self.link = link
        self.snippet = snippet
        self.displayLink = displayLink
        self.formattedUrl = formattedUrl
        self.browse_type = browse_type

def determine_orcid_browse_type(link: str) -> str:
    """Insert type info based on the string link"""
    pattern = r"https?://orcid\.org/\d{4}-\d{4}-\d{4}-\d{4}"
    if re.match(pattern, link):
        return "profile"
    else:
        return "unknown"
    
def fetch_orcid_profile_data(results):
    # List for data
    profile_data = []

    for result in results:
        if result.get("browse_type") == "profile":
            url = result["link"] + "/public-record.json"

            try:
                response = requests.get(url)
                if response.status_code == 200:
                    profile_data.append(response.json().get("displayName"))  # assuming response is a json
                else:
                    print(f"Cannot get data from {url}, status: {response.status_code}")
            except Exception as e:
                print(f"Cannot get data from {url}: {e}")

    return profile_data