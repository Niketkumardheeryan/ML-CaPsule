LLM Copilot Extension in VS Code 
----------------------------------

1. Introduction:
----------------
Welcome to the documentation for the VS Code Copilot Extension, which I created. This 
extension was developed to enhance coding efficiency by integrating advanced language 
models like Llama 3.1, OpenAI’s GPT-3.5-turbo, and Gemini 1.5. These models offer powerful 
code generation, suggestion capabilities, and the ability to solve complex coding problems. The 
extension is designed with a user-friendly interface and can be easily integrated into your 
existing workflow.

2. Prerequisites:
-----------------
Before using this extension, we need to ensure that we have the following installed on our 
system:
- Visual Studio Code (version 1.92.0 or higher)
- Node.js (for running the extension)
- TypeScript (for compiling TypeScript files)
Additionally, we need to make sure that we have access to API keys from Together.ai, Groq, 
OpenAI, or other supported providers to interact with the language models.

3. Installation:
------------------
- First we clone this repository 
- We then run “npm install” to install all necessary dependencies.
- Thereafter , we use the command npm run compile to compile the TypeScript files.
- Now to test the extension,we need to press F5 in VS Code to open a new window with 
the extension running or run the following command in terminal window :
code --extensionDevelopmentPath=D:\Extension\extension\ ( according to our 
exact file location path)

4. Overview of package.json
----------------------------
The package.json file is crucial as it defines the extension’s metadata, dependencies, 
and commands. Key elements include:
- Name and Version: The extension is named codesuggestion with version 0.0.1.
- Engines: Specifies compatibility with VS Code version 1.92.0 or higher.
- Contributes: Defines the command extension.openChat to open the chat interface.
- Scripts: Includes commands for compiling TypeScript, linting, and testing.
- Dependencies: Includes axios for API calls and development dependencies for 
TypeScript, linting, and testing.

5. Setting Up the Command in extension.ts:
------------------------------------------
The extension.ts file contains the core logic:
- Imports: Includes necessary modules like vscode and axios.
- Activate Function: The entry point when the extension is activated, where the 
command extension.openChat is registered.
- Webview Setup: The command triggers a Webview panel that displays the chat 
interface, allowing users to interact with the AI.

6. Making API Calls to AI Models:
---------------------------------
The getCodeSnippet function is central to the extension’s operation:
- Functionality: Sends a POST request to the selected AI model's API, passing the user’s 
query.
- Response Handling: The response is processed and the code snippet is returned and displayed in the Webview.

7. User Interface:
-------------------
The user interface is designed using HTML, CSS, and JavaScript:
- Chat Interface: Users can input queries and select the desired AI model from a 
dropdown menu.
- Response Display: The AI’s response is displayed in a code block format for easy 
copying and pasting.

8. Features:
------------

- Model Integration: Supports switching between Llama 3.1, GPT-3.5-turbo, and Gemini models.
- Code Generation: Generates code snippets, solves LeetCode & DSA problems, and supports autocompletion
- User-Friendly Interface: Simplified design for ease of use, allowing users to interact with the AI seamlessly

Sample chat and prompt response demonstration:
-----------------------------------------
![sample_chat_interface](https://github.com/user-attachments/assets/43cab310-e93e-4040-bc4c-4390c99684f6)

Personalized chat interface to match your needs :
-----------------------------------------
![Personalized_response](https://github.com/user-attachments/assets/30071652-86ed-4eae-9da3-a59df866635c)

