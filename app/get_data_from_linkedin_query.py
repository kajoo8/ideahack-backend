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