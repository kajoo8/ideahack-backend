def determine_researchgate_browse_type(link: str) -> str:
    """Insert type info based on the string link"""
    if "researchgate.net/profile" in link:
        return "profile"
    elif "researchgate.net/publication" in link:
        return "publication"
    elif "journal" in link:
        return "journal"
    else:
        return "unknown"
    
def fetch_researchgate_profile_data(results):
    # List for data
    profile_data = []

    for result in results:
        if result.get("browse_type") == "profile":
            link = result.get("link")
            if "/profile/" in link:
                profile_data.append(link.split("/profile/")[-1].replace("-", " "))
            
    return profile_data