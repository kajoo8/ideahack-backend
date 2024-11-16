def determine_linkedin_browse_type(link: str) -> str:
    """Insert type info based on the string link"""
    if "company" in link:
        return "company"
    elif "posts" in link:
        return "post"
    elif "in" in link:
        return "profile"
    elif "pulse" in link:
        return "pulse"
    else:
        return "unknown"