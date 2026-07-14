const vscode = require('vscode');
const axios = require('axios');

const TOGETHER_AI_API_KEY = process.env.TOGETHER_AI_API_KEY;
const GROQ_AI_API_KEY = process.env.GROQ_AI_API_KEY;
const LLAMA_API_KEY = process.env.LLAMA_API_KEY;
if (!TOGETHER_AI_API_KEY || !GROQ_AI_API_KEY || !LLAMA_API_KEY) {
    throw new Error(
        "❌ LLM Copilot Extension Error: Missing required API keys in your environment variables. " +
        "Please configure TOGETHER_AI_API_KEY, GROQ_AI_API_KEY, and LLAMA_API_KEY before running."
    );
}

async function getTogetherAIResponse(prompt) {
    const response = await axios.post('https://api.together.ai/v1/text/completion', {
        prompt: prompt
    }, {
        headers: {
            'Authorization': `Bearer ${TOGETHER_AI_API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    return response.data.text;
}

async function getGroqAIResponse(prompt) {
    const response = await axios.post('https://api.groq.com/v1/complete', {
        prompt: prompt
    }, {
        headers: {
            'Authorization': `Bearer ${GROQ_AI_API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    return response.data.text;
}

async function getLlamaResponse(prompt) {
    const response = await axios.post('https://api.llama.com/v1/complete', {
        prompt: prompt
    }, {
        headers: {
            'Authorization': `Bearer ${LLAMA_API_KEY}`,
            'Content-Type': 'application/json'
        }
    });
    return response.data.text;
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('my-ext.helloWorld', async () => {
        const prompt = await vscode.window.showInputBox({ prompt: 'Enter your prompt' });

        if (prompt) {
            try {
                const togetherAIResponse = await getTogetherAIResponse(prompt);
                const groqAIResponse = await getGroqAIResponse(prompt);
                const llamaResponse = await getLlamaResponse(prompt);

                vscode.window.showInformationMessage(`TogetherAI: ${togetherAIResponse}`);
                vscode.window.showInformationMessage(`GroqAI: ${groqAIResponse}`);
                vscode.window.showInformationMessage(`LLaMA: ${llamaResponse}`);
            } catch (error) {
                vscode.window.showErrorMessage('Error fetching response from LLMs');
            }
        }
    });

    context.subscriptions.push(disposable);
}

// @ts-ignore
exports.activate = activate;

function deactivate() {}

module.exports = {
    // @ts-ignore
    activate,
    deactivate
};
