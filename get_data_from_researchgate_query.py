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