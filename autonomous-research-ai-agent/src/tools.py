from ddgs import DDGS

def search_web(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found."
        output = ""
        for r in results:
            output += f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}\n\n"
        return output