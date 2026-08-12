# LLM Copilot Extension for VS Code

## 1. Overview

LLM Copilot is a VS Code extension that queries multiple language model providers — 
**Together.ai (Llama)**, **Groq**, and a **LLaMA** endpoint — from directly inside the editor. 
Enter a prompt once, and responses from all three providers are returned.

> OpenAI and Gemini are mentioned as intended future providers but are not yet implemented 
> in the code.

## 2. Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) v1.92.0 or higher
- [Node.js](https://nodejs.org/) (LTS recommended)
- API keys for [Together.ai](https://together.ai), [Groq](https://groq.com), and a LLaMA-hosted endpoint

## 3. Installation & Setup

### Step 1 — Clone the repository
```bash
git clone <repository-url>
cd "LLM Copilot Extension for VS Code IDE"
```

### Step 2 — Install dependencies
```bash
npm install
```

### Step 3 — Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your real API keys:

| Variable            | Required | Description                     |
|---------------------|----------|----------------------------------|
| `TOGETHER_API_KEY`  | Yes      | API key for Together.ai (Llama) |
| `GROQ_API_KEY`       | Yes      | API key for Groq                |
| `LLAMA_API_KEY`      | Yes      | API key for the LLaMA endpoint  |

Never commit your `.env` file — it's excluded via `.gitignore`.

### Step 4 — Run the extension
Press **F5** in VS Code to launch a new Extension Development Host window.

## 4. Usage

1. Open the command palette (`Ctrl+Shift+P` / `Cmd+Shift+P`).
2. Run **Hello World** (command id: `my-ext.helloWorld`).
3. Enter your prompt when asked.
4. Responses from Together.ai, Groq, and LLaMA appear as separate notification messages.
   If a required key is missing from `.env`, an error message names which one.

## 5. Project Structure
```
LLM Copilot Extension for VS Code IDE/
├── .vs-code/
│ ├── extensions.json
│ └── launch.json
├── test/
│ └── extension.test.js
├── extension.js
├── package.json
├── package-lock.json
├── jsconfig.json
├── .eslintrc.json
├── .vscode-test.mjs
├── .vscodeignore
├── .env.example
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## 6. Architecture Notes

- **`extension.js`** — entry point. `activate()` registers `my-ext.helloWorld`, checks that 
  all required env vars are set, prompts the user, and calls all three provider functions.
- **API calls** — made via `axios`, with keys loaded through `dotenv` from `process.env`.
- **Tests** — in `test/extension.test.js`.

## 7. Contributing

- Never commit API keys or `.env` files.
- Run `npm test` before submitting a PR.
- If adding a new provider, add its key to `.env.example` and this README's table.