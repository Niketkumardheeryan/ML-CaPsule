from dotenv import load_dotenv
import os
import json
from groq import Groq
from ddgs import DDGS

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def search(query: str) -> str:
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=5))
        if not results:
            return "No results found."
        output = ""
        for r in results:
            output += f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}\n\n"
        return output

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for current information using DuckDuckGo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def run_query(query: str) -> str:
    messages = [{"role": "user", "content": query}]
    max_retries = 3
    for attempt in range(max_retries):
        try:
            while True:
                 response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    max_tokens=1024
                )    
                 msg = response.choices[0].message
                 msg_dict = {"role": "assistant", "content": msg.content}
                 if msg.tool_calls:
                      msg_dict["tool_calls"] = msg.tool_calls
                 messages.append(msg_dict)

                 if not msg.tool_calls:
                    return msg.content
                
                 for tool_call in msg.tool_calls:
                    args = json.loads(tool_call.function.arguments)
                    result = search(args["query"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result
                    })
        except Exception as e:
            if attempt == max_retries - 1:
                return f"Error after {max_retries} attempts: {str(e)}"
            messages = [{"role": "user", "content": query}]  # reset and retry
        
     

if __name__ == "__main__":
    response = run_query("What is LangChain and what are its latest features?")
    print("\nFinal Answer:", response)