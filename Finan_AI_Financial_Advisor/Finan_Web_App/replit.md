# F₹nan AI — Financial Advisor

## Project Overview
An AI-powered financial advisor web app built for India. Uses a Flask backend with scikit-learn ML models (SVC + Random Forest) trained on an Indian finance dataset, and Google Gemini API for personalised financial advice. Firebase Gmail authentication, chat interface with black/green theme.

## Stack
- **Backend:** Python/Flask, scikit-learn (SVC + RandomForest), langextract, google-genai (gemini-2.5-flash)
- **Frontend:** Vanilla JS, Firebase Auth (client-side SDK v11), localStorage for persistence
- **Theme:** Black background, green (#00e676) text, Prata font
- **Data:** `Finan_AI Financial Advisor/indian_finance_ml_dataset_balanced_final (1).csv`
- **Workflow:** `python app.py` on port 5000

## Key Files
- `app.py` — Flask backend, ML model training, /analyze endpoint
- `templates/index.html` — Full UI with Firebase auth, chat interface
- `static/style.css` — Black/green theme, animations
- `static/app.js` — Chat logic, Firebase auth actions, budget/chat management
- `static/` — Static assets

## GitHub
- Remote: `https://github.com/medhya-verma-28/finan_ai_financial_advisor`
- Push uses `GITHUB_TOKEN` secret via: `git push https://x-access-token:$GITHUB_TOKEN@github.com/medhya-verma-28/finan_ai_financial_advisor main`

## User Preferences
- **Always ask the user before pushing to GitHub.** Never push automatically.
- Firebase authorized domains: user needs to add their Replit dev URL to Firebase Console → Authentication → Authorized Domains for Gmail sign-in to work in production.
