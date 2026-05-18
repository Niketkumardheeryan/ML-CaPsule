import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
import warnings
import time

warnings.filterwarnings('ignore')

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Crypto AI Dashboard",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed" if 'authenticated' not in st.session_state or not st.session_state.authenticated else "expanded"
)

# --- CUSTOM CSS (Premium Dark Theme & Glassmorphism) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a 40%, #020617 100%);
        color: #f8fafc;
    }
    
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    
    div[data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    
    div[data-testid="metric-container"] label {
        color: #94a3b8 !important;
        font-weight: 400;
        font-size: 1.1rem;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-weight: 700;
        font-size: 2.2rem;
    }

    div[data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }

    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: opacity 0.3s ease;
    }
    .stButton>button:hover {
        opacity: 0.9;
    }
    
    /* Login Form styling trick */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #a78bfa !important;
        border-bottom: 2px solid #a78bfa;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# --- DATA & ML FUNCTIONS ---
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('BTC-USD.csv')
        data['Date'] = pd.to_datetime(data['Date'])
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

def compute_features(data):
    df = data.copy()
    df['MA7'] = df['Close'].rolling(window=7).mean()
    df['MA30'] = df['Close'].rolling(window=30).mean()
    
    diff = df['Close'].diff(1).dropna()
    gain = (diff.where(diff > 0, 0)).rolling(window=14).mean()
    loss = (-diff.where(diff < 0, 0)).rolling(window=14).mean()
    RS = gain / loss
    df['RSI'] = 100 - (100 / (1 + RS))
    
    df['12EMA'] = df['Close'].ewm(span=12).mean()
    df['26EMA'] = df['Close'].ewm(span=26).mean()
    df['MACD'] = df['12EMA'] - df['26EMA']
    df['Signal_Line'] = df['MACD'].ewm(span=9).mean()
    df = df.drop(['26EMA', '12EMA'], axis=1)
    
    df['Pct_Change'] = df['Close'].pct_change() * 100
    df = df.fillna(method='ffill').fillna(method='bfill')
    return df

@st.cache_resource
def train_model(data_training):
    scaler = MinMaxScaler()
    training_data = scaler.fit_transform(data_training[['Close']])
    
    X_train, y_train = [], []
    for i in range(60, training_data.shape[0]):
        X_train.append(training_data[i-60:i])
        y_train.append(training_data[i, 0])
        
    X_train, y_train = np.array(X_train), np.array(y_train)
    
    model = Sequential()
    model.add(LSTM(units=50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    model.add(LSTM(units=60, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=3, batch_size=32, verbose=0)
    
    return model, scaler

# --- LOGIN PAGE ---
def login_page():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; background: -webkit-linear-gradient(#3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Crypto AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>Premium Intelligence Dashboard</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="admin")
            submit = st.form_submit_button("Access Dashboard 🚀", use_container_width=True)
            
            if submit:
                if username == "admin" and password == "admin":
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Authentication successful!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Use admin/admin")

# --- MAIN DASHBOARD ---
def main_dashboard():
    # Top Navbar
    nav_col1, nav_col2, nav_col3 = st.columns([8, 1, 1])
    with nav_col1:
        st.markdown(f"### 🌌 Crypto AI Dashboard")
    with nav_col2:
        if st.button("🏠 Home", use_container_width=True):
            st.rerun()
    with nav_col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
            
    st.markdown("---")

    # Sidebar
    st.sidebar.markdown(f"### 👋 Welcome, {st.session_state.username}")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navigation", ["Global Dashboard", "AI Predictions", "Deep Analytics"])
    st.sidebar.markdown("---")

    data = load_data()
    if data.empty:
        st.error("Data source 'BTC-USD.csv' missing.")
        return
        
    df = compute_features(data)
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    price_change = latest['Close'] - prev['Close']
    pct_change = (price_change / prev['Close']) * 100
    vol_change = ((latest['Volume'] - prev['Volume']) / prev['Volume']) * 100 if prev['Volume'] != 0 else 0

    if menu == "Global Dashboard":
        st.markdown("<h2 style='font-weight: 600; margin-bottom: 2rem;'>Executive Dashboard</h2>", unsafe_allow_html=True)
        
        # Top KPI Cards
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Bitcoin (BTC)", f"${latest['Close']:,.2f}", f"{pct_change:+.2f}%")
        c2.metric("24h Volume", f"${latest['Volume']/1e9:,.2f}B", f"{vol_change:+.2f}%")
        c3.metric("RSI (14)", f"{latest['RSI']:.2f}", f"{latest['RSI'] - prev['RSI']:+.2f}")
        c4.metric("MACD", f"{latest['MACD']:.2f}", f"{latest['MACD'] - prev['MACD']:+.2f}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Main Chart
        st.markdown("### 📈 Market Trajectory")
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=df['Date'].tail(90),
                open=df['Open'].tail(90),
                high=df['High'].tail(90),
                low=df['Low'].tail(90),
                close=df['Close'].tail(90),
                name='BTC'))
        
        fig.add_trace(go.Scatter(x=df['Date'].tail(90), y=df['MA30'].tail(90), line=dict(color='#8b5cf6', width=2), name='MA 30'))
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis_rangeslider_visible=False,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)
        
    elif menu == "AI Predictions":
        st.markdown("<h2 style='font-weight: 600; margin-bottom: 2rem;'>AI Forecasting Engine</h2>", unsafe_allow_html=True)
        
        st.info("Neural Network (LSTM) trained on historical patterns prior to 2020 to predict subsequent price action.")
        
        data_training = df[df['Date'] < '2020-01-01'].copy()
        data_test = df[df['Date'] >= '2020-01-01'].copy()
        
        with st.spinner('Initializing Neural Network...'):
            model, scaler = train_model(data_training)
            
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("### Prediction Parameters")
            days_to_predict = st.slider("Forecast Horizon (Days)", 10, 90, 30)
            run_pred = st.button("Generate Forecast", use_container_width=True)
            
        with col2:
            if run_pred:
                with st.spinner("Synthesizing Future Trajectories..."):
                    past_60 = data_training.tail(60)
                    df_test_prep = pd.concat([past_60, data_test]).reset_index(drop=True)
                    inputs = scaler.transform(df_test_prep[['Close']])
                    
                    X_test = []
                    for i in range(60, 60 + days_to_predict):
                        X_test.append(inputs[i-60:i])
                    X_test = np.array(X_test)
                    
                    y_pred = model.predict(X_test)
                    y_pred = y_pred * (1 / scaler.scale_[0])
                    
                    dates = data_test['Date'].values[:days_to_predict]
                    actuals = data_test['Close'].values[:days_to_predict]
                    
                    fig_pred = go.Figure()
                    fig_pred.add_trace(go.Scatter(x=dates, y=actuals, name="Actual Price", line=dict(color='#ef4444', width=2)))
                    fig_pred.add_trace(go.Scatter(x=dates, y=y_pred.flatten(), name="AI Prediction", line=dict(color='#10b981', width=3, dash='dot')))
                    
                    fig_pred.update_layout(
                        template='plotly_dark',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        title="LSTM Model Output vs Reality",
                        height=450
                    )
                    st.plotly_chart(fig_pred, use_container_width=True)
            else:
                st.markdown("<div style='text-align: center; padding: 4rem; color: #64748b; border: 1px dashed #334155; border-radius: 12px;'>Select parameters and click Generate Forecast to visualize AI predictions.</div>", unsafe_allow_html=True)
                
    elif menu == "Deep Analytics":
        st.markdown("<h2 style='font-weight: 600; margin-bottom: 2rem;'>Technical Indicators</h2>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["RSI Momentum", "MACD Convergence"])
        
        with tab1:
            fig_rsi = go.Figure()
            fig_rsi.add_trace(go.Scatter(x=df['Date'].tail(180), y=df['RSI'].tail(180), name="RSI", line=dict(color='#a855f7')))
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="#ef4444")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="#10b981")
            fig_rsi.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
            st.plotly_chart(fig_rsi, use_container_width=True)
            
        with tab2:
            fig_macd = go.Figure()
            fig_macd.add_trace(go.Scatter(x=df['Date'].tail(180), y=df['MACD'].tail(180), name="MACD", line=dict(color='#3b82f6')))
            fig_macd.add_trace(go.Scatter(x=df['Date'].tail(180), y=df['Signal_Line'].tail(180), name="Signal", line=dict(color='#f59e0b')))
            fig_macd.add_bar(x=df['Date'].tail(180), y=(df['MACD'] - df['Signal_Line']).tail(180), name="Histogram", marker_color='#64748b')
            fig_macd.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400)
            st.plotly_chart(fig_macd, use_container_width=True)

# --- APP ROUTING ---
if not st.session_state.authenticated:
    login_page()
else:
    main_dashboard()
