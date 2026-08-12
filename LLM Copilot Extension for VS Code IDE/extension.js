const vscode = require('vscode');
const axios = require('axios');
require('dotenv').config();

const TOGETHER_AI_API_KEY = process.env.TOGETHER_API_KEY;
const GROQ_AI_API_KEY = process.env.GROQ_API_KEY;
const LLAMA_API_KEY = process.env.LLAMA_API_KEY;

function assertKeysConfigured() {
    const missing = [];
    if (!TOGETHER_AI_API_KEY) missing.push('TOGETHER_API_KEY');
    if (!GROQ_AI_API_KEY) missing.push('GROQ_API_KEY');
    if (!LLAMA_API_KEY) missing.push('LLAMA_API_KEY');
    return missing;
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
        const missingKeys = assertKeysConfigured();
        if (missingKeys.length > 0) {
            vscode.window.showErrorMessage(
                `Missing API key(s) in your .env file: ${missingKeys.join(', ')}. See .env.example for setup.`
            );
            return;
        }
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
