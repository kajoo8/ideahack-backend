import re

def determine_orcid_browse_type(link: str) -> str:
    """Insert type info based on the string link"""
    pattern = r"https?://orcid\.org/\d{4}-\d{4}-\d{4}-\d{4}"
    if re.match(pattern, link):
        return "profile"
    else:
        return "unknown"