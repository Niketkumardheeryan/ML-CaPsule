# 🔍 Autonomous Research AI Agent

An intelligent AI-powered research assistant that autonomously searches the web, analyzes information, and generates comprehensive, cited responses to user queries.

Built as part of the ML-CaPsule open-source project.

---

##  Features

✅ Autonomous web research using ReAct workflow  
✅ Real-time web search integration  
✅ Fast LLM inference using Groq API  
✅ Interactive Streamlit interface  
✅ Modular architecture for easy extension  
✅ Source-backed responses  

---

##  Workflow

The agent follows the ReAct (Reasoning + Acting) framework:

1. User submits a query
2. Agent analyzes intent
3. Agent decides what information is needed
4. Agent performs web search
5. Agent synthesizes results
6. Agent generates a final response with citations

---

##  Tech Stack

| Technology | Purpose |
|------------|----------|
| Python | Core development |
| LangChain | Agent orchestration |
| LangGraph | Workflow management |
| Groq API | LLM inference |
| DuckDuckGo Search | Web search |
| Streamlit | Frontend UI |

---

##  Installation

### Clone repository

```bash
git clone https://github.com/Niketkumardheeryan/ML-CaPsule.git
cd ML-CaPsule
```

### Create virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

Get a free API key from:

https://console.groq.com

---

##  Run Application

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

##  Project Structure

```text
Autonomous-Research-AI-Agent/
│
├── src/
│   ├── agent.py
│   ├── tools.py
│   ├── workflow.py
│   └── llm.py
│
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Example Usage

Query:

```text
What are the latest developments in multi-agent AI systems?
```

Output:

```text
The agent searches the web, gathers information from multiple sources,
analyzes findings, and generates a synthesized answer with references.
```

---

## Future Improvements

- Memory support
- Multi-agent collaboration
- PDF report generation
- Vector database integration
- Research history tracking

---

## Acknowledgements

- Groq for high-speed inference
- LangChain ecosystem
- DuckDuckGo Search
- ML-CaPsule open-source contributors

---

Made with ❤️ for GSSoC 2026