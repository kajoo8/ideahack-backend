def determine_linkedin_browse_type(link: str) -> str:
    """Insert type info based on the string link"""
    if "linkedin.com/company/" in link:
        return "company"
    elif "linkedin.com/posts/" in link:
        return "post"
    elif "linkedin.com/in/" in link:
        return "profile"
    elif "linkedin.com/pulse/" in link:
        return "pulse"
    else:
        return "unknown"
    
def fetch_linkedin_profile_data(results):
    # List for data
    profile_data = []   

    for result in results:
        title = result.get("title")
        linktype = result.get("browse_type")
        dirLink = result.get("link")
        if linktype == "post":
            if " on LinkedIn" in title:
                name_part = title.split(" on LinkedIn")[0]
                profile_data.append({"name": name_part, "type": "post", "directLink": dirLink})
        elif linktype == "company":
            if " | LinkedIn" in title:
                company_name = title.split(" | LinkedIn")[0]
                profile_data.append({"name": company_name, "type": "company", "directLink": dirLink})
        elif linktype == "profile":
            if " - " in title:
                # Split by " - " and get the first part
                name_part = title.split(" - ")[0]
                profile_data.append({"name": name_part, "type": "profile", "directLink": dirLink})

    return profile_data