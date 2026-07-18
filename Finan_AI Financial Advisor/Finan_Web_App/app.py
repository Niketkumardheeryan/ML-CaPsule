import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from flask import Flask, render_template, request, jsonify
import textwrap
import langextract as lx
from google.genai import Client

app = Flask(__name__)

DATA_PATH = "Finan_Web_App/indian_finance_ml_dataset_balanced_final (1).csv"

print("Loading dataset and training models...")

df = pd.read_csv(DATA_PATH)

classes_X1 = ['Monthly Income (INR)', 'Cost of Living Expenditure (INR)',
               'Other Important Investments (INR)', 'Consumerist Expenditure (INR)',
               'Crisis Shock Expenditure (INR)', 'Total Monthly Expenditure (INR)',
               'Debt Status']
X = df[classes_X1].copy()
y = df['Financial State Category']

numeric_features = X.select_dtypes(include=['int64', 'float64']).columns
categorical_features = ['Debt Status']

numeric_transformer_X = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer_X = LabelEncoder()
categorical_transformer_y = LabelEncoder()

numeric_transformer_X.fit(X[numeric_features])
X[numeric_features] = numeric_transformer_X.transform(X[numeric_features])
categorical_transformer_X.fit(X[categorical_features].values.ravel())
X[categorical_features] = categorical_transformer_X.transform(X[categorical_features].values.ravel()).reshape(-1, 1)
y_transformed = categorical_transformer_y.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_transformed, test_size=0.2, random_state=42)
model = SVC(kernel='linear', C=1.0, random_state=42, class_weight='balanced')
model.fit(X_train, y_train)

X2 = df[['Monthly Income (INR)', 'Cost of Living Expenditure (INR)', 'Other Important Investments (INR)',
          'Consumerist Expenditure (INR)', 'Crisis Shock Expenditure (INR)',
          'Total Monthly Expenditure (INR)', 'Debt Status', 'Financial State Category']].copy()
y1 = df['Current Monthly Income Enough for Next Few Months']
y2 = df['Current Expenditure Worth It']

numeric_features_X2 = X2.select_dtypes(include=['int64', 'float64']).columns
numeric_transformer_X2 = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
categorical_transformer_X2_debt = LabelEncoder()
catergorical_transformer_X2_financial_state = LabelEncoder()

numeric_transformer_X2.fit(X2[numeric_features_X2])
X2[numeric_features_X2] = numeric_transformer_X2.transform(X2[numeric_features_X2])
categorical_transformer_X2_debt.fit(X2['Debt Status'].values.ravel())
X2['Debt Status'] = categorical_transformer_X2_debt.transform(X2['Debt Status'].values.ravel()).reshape(-1, 1)
catergorical_transformer_X2_financial_state.fit(X2['Financial State Category'].values.ravel())
X2['Financial State Category'] = catergorical_transformer_X2_financial_state.transform(X2['Financial State Category'].values.ravel()).reshape(-1, 1)

le1 = LabelEncoder()
le2 = LabelEncoder()
y1_transformed = le1.fit_transform(y1)
y2_transformed = le2.fit_transform(y2)

X_train1, X_test1, y_train1, y_test1 = train_test_split(X2, y1_transformed, test_size=0.2, random_state=42)
X_train2, X_test2, y_train2, y_test2 = train_test_split(X2, y2_transformed, test_size=0.2, random_state=42)
model1 = SVC(kernel='linear', C=1.0, random_state=42, class_weight='balanced')
model2 = SVC(kernel='linear', C=1.0, random_state=42, class_weight='balanced')
model1.fit(X_train1, y_train1)
model2.fit(X_train2, y_train2)

df_rf = pd.read_csv(DATA_PATH)
df_rf['Savings_Margin_Ratio'] = (df_rf['Monthly Income (INR)'] - df_rf['Total Monthly Expenditure (INR)']) / df_rf['Monthly Income (INR)']
df_rf['Essential_Cost_Ratio'] = df_rf['Cost of Living Expenditure (INR)'] / df_rf['Total Monthly Expenditure (INR)']
df_rf['Current_Investment_Allocation_Rate'] = df_rf['Other Important Investments (INR)'] / df_rf['Monthly Income (INR)']
df_rf['Current_Crisis_Allocation_Rate'] = df_rf['Crisis Shock Expenditure (INR)'] / df_rf['Monthly Income (INR)']

feature_names = [
    'Monthly Income (INR)', 'Cost of Living Expenditure (INR)', 'Other Important Investments (INR)',
    'Consumerist Expenditure (INR)', 'Crisis Shock Expenditure (INR)', 'Total Monthly Expenditure (INR)',
    'Savings_Margin_Ratio', 'Essential_Cost_Ratio', 'Current_Investment_Allocation_Rate', 'Current_Crisis_Allocation_Rate'
]

X3 = df_rf[feature_names]
y3 = df_rf['Suggested Budget - Cost of Living']
y4 = df_rf['Suggested Budget - Other Important Investments']
y5 = df_rf['Suggested Budget - Consumerist Expenditure']
y6 = df_rf['Suggested Budget - Crisis Shocks']

numeric_transformer_X3 = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])
X3_transformed = numeric_transformer_X3.fit_transform(X3)

X_train3, X_test3, y_train3, y_test3 = train_test_split(X3_transformed, y3, test_size=0.2, random_state=42)
X_train4, X_test4, y_train4, y_test4 = train_test_split(X3_transformed, y4, test_size=0.2, random_state=42)
X_train5, X_test5, y_train5, y_test5 = train_test_split(X3_transformed, y5, test_size=0.2, random_state=42)
X_train6, X_test6, y_train6, y_test6 = train_test_split(X3_transformed, y6, test_size=0.2, random_state=42)

model3 = RandomForestRegressor(n_estimators=100, random_state=42)
model4 = RandomForestRegressor(n_estimators=100, random_state=42)
model5 = RandomForestRegressor(n_estimators=100, random_state=42)
model6 = RandomForestRegressor(n_estimators=100, random_state=42)
model3.fit(X_train3, y_train3)
model4.fit(X_train4, y_train4)
model5.fit(X_train5, y_train5)
model6.fit(X_train6, y_train6)

print("All models trained successfully!")

lx_prompt = textwrap.dedent("""
    Extract financial information from the text.
    Identify if the following fields exist and extract them: 'Monthly Income (INR)', 'Cost of Living Expenditure (INR)', 'Other Important Investments (INR)', 'Consumerist Expenditure (INR)', 'Crisis Shock Expenditure (INR)', 'Total Monthly Expenditure (INR)', 'Debt Status'.
    For all monetary amounts, convert to plain integers in INR regardless of the format used:
    - Indian shorthand: 1L or 1 lakh or 1 lac = 100000, 2.5L or 2.5 lakh = 250000, 1K or 1k or 1 thousand = 1000, 25K = 25000, 1 crore or 1cr = 10000000
    - Written words: one lakh = 100000, fifty thousand = 50000, two crore = 20000000
    - Symbols/prefixes: ₹, Rs, INR followed by a number — strip the symbol and keep the integer
    - Comma-formatted: 1,40,000 = 140000, 1,00,000 = 100000
    - Decimal notation: 1.5 lakh = 150000, 2.5 crore = 25000000
    Always output the extracted_text as a plain integer (no symbols, no words, no commas).
    For Debt Status extract 'In Debt' or 'Not in Debt'.
""")

lx_examples = [
    lx.data.ExampleData(
        text="Hey, I need some honest financial advice. I am currently working as a software engineer in Bengaluru, and my monthly in-hand salary is ₹1,40,000. Lately, I feel like my money is just vanishing. My fixed overheads are quite high—between my house rent, society maintenance, maid, electricity, and groceries, my core cost of living comes out to exactly ₹45,000 every month. On top of that, I am upskilling myself to transition into a management role, so I am paying a monthly EMI of ₹15,000 for an executive data science certification course from an IIM. I've also been overspending a bit on lifestyle choices; between dining out at pubs, weekend trips, and ordering from Swiggy/Zomato, my discretionary consumerist spending hits around ₹25,000 monthly. To make matters worse, my father had a minor medical emergency back home last month, so I've had to commit a fixed ₹15,000 monthly towards his ongoing healthcare and medicine costs for the foreseeable future. If you calculate it all, my total monthly expenditure has ballooned to ₹1,00,000, leaving me with very little savings. As for my overall debt status, I currently owe ₹3,50,000 on an active personal loan that I took out for relocation and furnishing last year. Looking at this breakdown, do you think my current level of expenditure is actually worth it, or am I jeopardizing my long-term financial health for short-term comfort?",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="140000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="45000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="15000", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="25000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="15000", attributes={}),
            lx.data.Extraction(extraction_class="Total Monthly Expenditure (INR)", extraction_text="100000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="In Debt", attributes={})
        ]
    ),
    lx.data.ExampleData(
        text="Hey, I need some honest financial advice. I am currently working as a software engineer in Bengaluru, and my monthly in-hand salary is ₹1,40,000. My fixed overheads—rent, maintenance, maid, electricity, groceries—cost ₹45,000 monthly. I pay ₹15,000 for an IIM executive certification. My lifestyle spending is ₹25,000, and ₹15,000 goes to my father's healthcare. Total expenditure is ₹1,00,000. I have no debts. Is my spending balanced?",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="140000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="45000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="15000", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="25000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="15000", attributes={}),
            lx.data.Extraction(extraction_class="Total Monthly Expenditure (INR)", extraction_text="100000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="Not in Debt", attributes={})
        ]
    ),
    lx.data.ExampleData(
        text="Monthly income 2 lakh, cost of living 60 thousand, important investments of 40 thousand, consumerism of 25 K and crisis expenses of 30 K. No loans pending. Is my current monthly income enough and is spending worth it?",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="200000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="60000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="40000", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="25000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="30000", attributes={}),
            lx.data.Extraction(extraction_class="Total Monthly Expenditure (INR)", extraction_text="155000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="Not in Debt", attributes={})
        ]
    ),
    lx.data.ExampleData(
        text="My salary is 2.5L per month. Rent and groceries cost me about 80K. I invest 20 thousand in mutual funds. I spend around 15K on entertainment. Emergency fund contribution is 10K monthly. Total spending is 1.25 lakh. I have a car loan of 5 lakh outstanding.",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="250000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="80000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="20000", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="15000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="10000", attributes={}),
            lx.data.Extraction(extraction_class="Total Monthly Expenditure (INR)", extraction_text="125000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="In Debt", attributes={})
        ]
    ),
    lx.data.ExampleData(
        text="I earn Rs 75000 a month. Living costs are fifty thousand. No investments currently. I spend five thousand on leisure. I keep ten thousand aside for emergencies. Total outgo is sixty-five thousand. I have no loans.",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="75000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="50000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="0", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="5000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="10000", attributes={}),
            lx.data.Extraction(extraction_class="Total Monthly Expenditure (INR)", extraction_text="65000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="Not in Debt", attributes={})
        ]
    ),
    lx.data.ExampleData(
        text="Income: 1.2 crore per annum so about 10 lakh a month. House EMI is 2.5L. Kids' school and groceries together are 1L. I put 1.5 lakh in stocks and SIPs. Dining and travel cost me 50K. I keep 25K for medical emergencies. No outstanding debts. Am I saving enough?",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="1000000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="100000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="150000", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="50000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="25000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="Not in Debt", attributes={})
        ]
    ),
    lx.data.ExampleData(
        text="Monthly income 200000, cost of living 60000, important investments of 40000, consumerism of 25000 and crisis expenses of 30000. No loans pending. Is my current monthly income enough and is spending worth it?",
        extractions=[
            lx.data.Extraction(extraction_class="Monthly Income (INR)", extraction_text="200000", attributes={}),
            lx.data.Extraction(extraction_class="Cost of Living Expenditure (INR)", extraction_text="60000", attributes={}),
            lx.data.Extraction(extraction_class="Other Important Investments (INR)", extraction_text="40000", attributes={}),
            lx.data.Extraction(extraction_class="Consumerist Expenditure (INR)", extraction_text="25000", attributes={}),
            lx.data.Extraction(extraction_class="Crisis Shock Expenditure (INR)", extraction_text="30000", attributes={}),
            lx.data.Extraction(extraction_class="Total Monthly Expenditure (INR)", extraction_text="155000", attributes={}),
            lx.data.Extraction(extraction_class="Debt Status", extraction_text="Not in Debt", attributes={})
        ]
    ),
]

lx_classes = ['Monthly Income (INR)', 'Cost of Living Expenditure (INR)', 'Other Important Investments (INR)',
               'Consumerist Expenditure (INR)', 'Crisis Shock Expenditure (INR)',
               'Total Monthly Expenditure (INR)', 'Debt Status']


@app.route('/')
def index():
    return render_template(
        'index.html',
        firebase_api_key=os.environ.get('FIREBASE_API_KEY', ''),
        firebase_project_id=os.environ.get('FIREBASE_PROJECT_ID', ''),
        firebase_app_id=os.environ.get('FIREBASE_APP_ID', ''),
    )


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    query = data.get('query', '').strip()
    if not query:
        return jsonify({'error': 'Please provide a financial query.'}), 400

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'GEMINI_API_KEY is not configured.'}), 500

    try:
        result = lx.extract(
            text_or_documents=query,
            prompt_description=lx_prompt,
            examples=lx_examples,
            model_id="gemini-2.5-flash",
        )

        import re as _re

        def clean_int(val):
            """Parse any Indian currency format and return a plain integer in INR."""
            s = str(val).lower().strip()
            # Remove currency prefixes/symbols
            s = _re.sub(r'(₹|rs\.?|inr)\s*', '', s).strip()
            # Remove commas (Indian formatting: 1,40,000)
            s = s.replace(',', '')
            # Crore
            m = _re.match(r'^([\d.]+)\s*(?:crore|crores|cr)\b', s)
            if m:
                return int(float(m.group(1)) * 10_000_000)
            # Lakh / lac / L
            m = _re.match(r'^([\d.]+)\s*(?:lakh|lakhs|lac|lacs|l)\b', s)
            if m:
                return int(float(m.group(1)) * 100_000)
            # Thousand / k
            m = _re.match(r'^([\d.]+)\s*(?:thousand|thousands|k)\b', s)
            if m:
                return int(float(m.group(1)) * 1_000)
            # Hundred
            m = _re.match(r'^([\d.]+)\s*(?:hundred|hundreds)\b', s)
            if m:
                return int(float(m.group(1)) * 100)
            # Plain number (possibly decimal)
            cleaned = _re.sub(r'[^\d.]', '', s)
            return int(float(cleaned)) if cleaned else 0

        def normalize_debt(val):
            """Normalise any debt string to the two labels seen in training."""
            v = str(val).lower().strip()
            if 'not' in v or 'no debt' in v or v in ('', 'none'):
                return 'Not in Debt'
            return 'In Debt'

        # Build a dict keyed by extraction class (handles any ordering)
        extracted_map = {}
        for ex in result.extractions:
            extracted_map[ex.extraction_class] = ex.extraction_text

        numeric_keys = lx_classes[:-1]  # 6 financial columns
        debt_status = normalize_debt(extracted_map.get('Debt Status', 'Not in Debt'))

        # Ordered list: 6 ints + 1 debt string
        numeric_vals = [clean_int(extracted_map.get(k, 0)) for k in numeric_keys]
        X_validation = numeric_vals + [debt_status]

        # --- Model 1: Financial State Category ---
        X_val_df = pd.DataFrame(
            {col: [numeric_vals[i]] for i, col in enumerate(numeric_keys)}
        )
        X_val_df['Debt Status'] = [debt_status]
        X_val_df[numeric_keys] = X_val_df[numeric_keys].astype(float)

        X_val_df[numeric_keys] = numeric_transformer_X.transform(X_val_df[numeric_keys])
        X_val_df['Debt Status'] = categorical_transformer_X.transform(
            X_val_df['Debt Status'].values.ravel()).reshape(-1, 1)

        y_pred_cat = model.predict(X_val_df)
        financial_state_category = categorical_transformer_y.inverse_transform(y_pred_cat)[0]

        # --- Models 1b/2: Income sufficiency & Expenditure worth ---
        # Use string financial_state_category (not the raw int) so the LabelEncoder can encode it
        X2_cols = lx_classes + ['Financial State Category']
        X2_val_df = pd.DataFrame(
            {col: [numeric_vals[i]] for i, col in enumerate(numeric_keys)}
        )
        X2_val_df['Debt Status'] = [debt_status]
        X2_val_df['Financial State Category'] = [financial_state_category]
        X2_val_df[numeric_keys] = X2_val_df[numeric_keys].astype(float)

        X2_val_df[numeric_features_X2] = numeric_transformer_X2.transform(
            X2_val_df[numeric_features_X2])
        X2_val_df['Debt Status'] = categorical_transformer_X2_debt.transform(
            X2_val_df['Debt Status'].values.ravel()).reshape(-1, 1)
        X2_val_df['Financial State Category'] = catergorical_transformer_X2_financial_state.transform(
            X2_val_df['Financial State Category'].values.ravel()).reshape(-1, 1)

        y_pred1 = model1.predict(X2_val_df)
        y_pred2 = model2.predict(X2_val_df)
        current_monthly_income_enough = le1.inverse_transform(y_pred1)[0]
        current_expenditure_worth_it = le2.inverse_transform(y_pred2)[0]

        # --- Models 3-6: Budget suggestions ---
        X3_validation_df = pd.DataFrame(
            {col: [float(numeric_vals[i])] for i, col in enumerate(numeric_keys)}
        )
        _income = X3_validation_df['Monthly Income (INR)'].iloc[0]
        _total_exp = X3_validation_df['Total Monthly Expenditure (INR)'].iloc[0]

        X3_validation_df['Savings_Margin_Ratio'] = (
            (_income - _total_exp) / _income if _income > 0 else 0.0
        )
        X3_validation_df['Essential_Cost_Ratio'] = (
            X3_validation_df['Cost of Living Expenditure (INR)'].iloc[0] / _total_exp
            if _total_exp > 0 else 0.0
        )
        X3_validation_df['Current_Investment_Allocation_Rate'] = (
            X3_validation_df['Other Important Investments (INR)'].iloc[0] / _income
            if _income > 0 else 0.0
        )
        X3_validation_df['Current_Crisis_Allocation_Rate'] = (
            X3_validation_df['Crisis Shock Expenditure (INR)'].iloc[0] / _income
            if _income > 0 else 0.0
        )

        # Safety: replace any remaining inf/NaN with 0 before scaling
        X3_validation_df.replace([np.inf, -np.inf], 0.0, inplace=True)
        X3_validation_df.fillna(0.0, inplace=True)

        X3_transformed_val = numeric_transformer_X3.transform(X3_validation_df)

        y_pred3 = model3.predict(X3_transformed_val)
        y_pred4 = model4.predict(X3_transformed_val)
        y_pred5 = model5.predict(X3_transformed_val)
        y_pred6 = model6.predict(X3_transformed_val)

        monthly_income = X_validation[0]

        client = Client(api_key=api_key)
        prompt = f"""
You are Finan, an informative and supportive ai financial advisor.
Give financial advice based on the following user query, extracted financial information and predicted financial information:
User Query: {query}
Monthly Income (INR): {X_validation[0]}
Cost of Living Expenditure (INR): {X_validation[1]}
Other Important Investments (INR): {X_validation[2]}
Consumerist Expenditure (INR): {X_validation[3]}
Crisis Shock Expenditure (INR): {X_validation[4]}
Total Monthly Expenditure (INR): {X_validation[5]}
Debt Status: {X_validation[6]}
Predicted Financial State Category: {financial_state_category}
Is Current Monthly Income Enough for Next Few Months? {current_monthly_income_enough}
Is Current Expenditure Worth It? {current_expenditure_worth_it}
Suggested Budget for Cost of Living Expenditure (INR): {(y_pred3[0] * monthly_income):.2f}
Suggested Budget for Other Important Investments (INR): {(y_pred4[0] * monthly_income):.2f}
Suggested Budget for Consumerist Expenditure (INR): {(y_pred5[0] * monthly_income):.2f}
Suggested Budget for Crisis Shock Expenditure (INR): {(y_pred6[0] * monthly_income):.2f}

Format for financial advice:
1. Greet user, tell your name as Finan, an informative and supportive ai financial advisor.
2. Acknowledge the user's financial situation with empathy and without judgment.
3. Provide a clear summary of user's financial situation by summarising all information extracted from user query.
4. Reveal user's predicted financial state category and explain what it means in simple terms.
5. Inform user whether their current monthly income is likely to be sufficient for the next few months and their current expenditure is likely to be worth it based on the model's prediction.
6. Display the suggested budgets values in INR for each expenditure category.
7. Explain how suggested budgets can help improve user's financial health.
8. Based on the predicted financial state category, provide personalized financial advice on how to manage income based on indian economic context, how to optimize expenditure, and how to approach investments. Handle any other queries user has based on indian economic landscape. Avoid generic advice and focus on actionable steps user can take.
End the response with a support note for user and wish them well for future and avoid using any technical terms in that note.
"""
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        return jsonify({
            'advice': response.text,
            'extracted': {
                'monthly_income': X_validation[0],
                'cost_of_living': X_validation[1],
                'investments': X_validation[2],
                'consumerist': X_validation[3],
                'crisis_shock': X_validation[4],
                'total_expenditure': X_validation[5],
                'debt_status': X_validation[6],
            },
            'predictions': {
                'financial_state': financial_state_category,
                'income_sufficient': current_monthly_income_enough,
                'expenditure_worth_it': current_expenditure_worth_it,
            },
            'budgets': {
                'cost_of_living': round(y_pred3[0] * monthly_income, 2),
                'investments': round(y_pred4[0] * monthly_income, 2),
                'consumerist': round(y_pred5[0] * monthly_income, 2),
                'crisis_shock': round(y_pred6[0] * monthly_income, 2),
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
