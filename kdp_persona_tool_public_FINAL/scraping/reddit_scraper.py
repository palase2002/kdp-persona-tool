
def search_reddit_posts(keyword):
    print(f"[DEBUG] Simulazione ricerca Reddit per: {keyword}")
    return [f"Reddit post 1 about {keyword}", f"Reddit post 2 about {keyword}"]

def format_posts_for_prompt(posts):
    return "\n".join(posts)
