import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

st.set_page_config(
    page_title="Intelligent Network Intrusion Detection System",
    page_icon="🛡️",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #161b22;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #c9d1d9;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262d;
        color: #58a6ff;
        border-bottom: 2px solid #58a6ff;
    }
</style>
""", unsafe_allow_html=True)

# Helper to load artifacts
@st.cache_resource
def load_ml_artifacts():
    path = os.path.join(os.path.dirname(__file__), 'trained_artifacts.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None

@st.cache_resource
def load_shap_artifacts():
    path = os.path.join(os.path.dirname(__file__), 'shap_artifacts.pkl')
    if os.path.exists(path):
        with open(path, 'rb') as f:
            return pickle.load(f)
    return None

artifacts = load_ml_artifacts()
shap_art = load_shap_artifacts()

st.title("🛡️ Intelligent Network Intrusion Detection System")
st.subheader("Real-time network traffic classification, explainability, and performance analysis using ML")

if artifacts is None:
    st.warning("⚠️ Machine learning models are not yet trained. Please run training to enable the dashboard.")
    if st.button("🚀 Train Models Now (using train_models.py)"):
        with st.spinner("Training models (Random Forest, XGBoost, LightGBM, SVM)... This might take a minute."):
            try:
                import subprocess
                script_path = os.path.join(os.path.dirname(__file__), 'train_models.py')
                res = subprocess.run(["python", script_path], capture_output=True, text=True)
                st.success("Models trained successfully!")
                # Force reload
                st.rerun()
            except Exception as e:
                st.error(f"Error training models: {e}")
                st.text(res.stderr if 'res' in locals() else "")
    st.stop()

# Extract objects
scaler = artifacts['scaler']
label_encoder = artifacts['label_encoder']
models = artifacts['models']
results = artifacts['results']
feature_names = artifacts['feature_names']
corr_matrix = pd.DataFrame(artifacts['corr_matrix'])

# Tab Navigation
tab_overview, tab_shap, tab_simulation, tab_benchmarks = st.tabs([
    "📊 Model Performance Dashboard", 
    "🔍 SHAP Explainability Layer", 
    "⚡ Real-time Packet Simulation", 
    "📈 Inference Speed Benchmark"
])

# ----------------- Tab 1: Model Performance Dashboard -----------------
with tab_overview:
    st.header("Model Performance & Comparison")
    
    # Overview Cards
    col1, col2, col3, col4 = st.columns(4)
    best_acc_model = max(results, key=lambda k: results[k]['Accuracy'])
    best_f1_model = max(results, key=lambda k: results[k]['F1-Score'])
    fastest_model = min(results, key=lambda k: results[k]['Inference Speed (us/packet)'])
    
    col1.metric("Highest Accuracy", f"{results[best_acc_model]['Accuracy']*100:.2f}%", best_acc_model)
    col2.metric("Best F1-Score", f"{results[best_f1_model]['F1-Score']*100:.2f}%", best_f1_model)
    col3.metric("Fastest Classifier", f"{results[fastest_model]['Inference Speed (us/packet)']:.2f} us", f"{fastest_model}")
    col4.metric("Dataset Size", "6,000 Flows", "CICIDS2017 Schema")
    
    st.markdown("---")
    
    # Comparison table
    comp_data = []
    for m_name, metrics in results.items():
        comp_data.append({
            'Model': m_name,
            'Accuracy': f"{metrics['Accuracy']*100:.2f}%",
            'Precision': f"{metrics['Precision']*100:.2f}%",
            'Recall': f"{metrics['Recall']*100:.2f}%",
            'F1-Score': f"{metrics['F1-Score']*100:.2f}%",
            'ROC-AUC': f"{metrics['ROC-AUC']*100:.2f}%",
            'Training Time (s)': f"{metrics['Training Time (s)']:.3f}s",
            'Inference Speed (us/packet)': f"{metrics['Inference Speed (us/packet)']:.2f} us"
        })
    st.subheader("Model Comparison Summary")
    st.dataframe(pd.DataFrame(comp_data), use_container_width=True)
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        st.subheader("Model Performance Comparison")
        accs = [results[m]['Accuracy'] * 100 for m in results]
        f1s = [results[m]['F1-Score'] * 100 for m in results]
        names = list(results.keys())
        
        x = np.arange(len(names))
        width = 0.35
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0e1117')
        ax.set_facecolor('#161b22')
        rects1 = ax.bar(x - width/2, accs, width, label='Accuracy', color='#58a6ff')
        rects2 = ax.bar(x + width/2, f1s, width, label='F1-Score', color='#56d364')
        
        ax.set_ylabel('Percentage (%)', color='white')
        ax.set_title('Accuracy vs F1-Score', color='white')
        ax.set_xticks(x)
        ax.set_xticklabels(names, color='white')
        ax.legend()
        ax.tick_params(colors='white')
        plt.tight_layout()
        st.pyplot(fig)
        
    with col_plot2:
        st.subheader("Confusion Matrix Visualizer")
        selected_model_name = st.selectbox("Select Model for Confusion Matrix:", list(results.keys()))
        cm = np.array(results[selected_model_name]['Confusion Matrix'])
        
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0e1117')
        ax.set_facecolor('#161b22')
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
        ax.set_ylabel('True Label', color='white')
        ax.set_xlabel('Predicted Label', color='white')
        ax.tick_params(colors='white')
        plt.tight_layout()
        st.pyplot(fig)

# ----------------- Tab 2: SHAP Explainability Layer -----------------
with tab_shap:
    st.header("Explainability & Interpretability")
    st.markdown("""
        **SHAP (SHapley Additive exPlanations)** values quantify the contribution of each network feature 
        to the model's predictions. This gives security analysts clarity on *why* a particular flow was flagged.
    """)
    
    if shap_art is None:
        st.info("SHAP values are not precomputed. Computing SHAP values takes some time.")
    else:
        st.subheader("Global Feature Importance (Random Forest)")
        # Display static feature contributions
        st.image(os.path.join(os.path.dirname(__file__), '..', 'ml img.jpg') if os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'ml img.jpg')) else [], width=300, caption="SHAP Global Insights")
        
        st.markdown("### Interactive Local Explanation")
        st.markdown("Select a sample network flow to explain in detail:")
        
        # Load sample for local explanations
        X_sample = shap_art['X_sample']
        shap_values = shap_art['shap_values']
        sample_labels = shap_art['sample_labels']
        
        sample_id = st.slider("Select Sample Index:", 0, len(X_sample) - 1, 0)
        
        # Inverse transform scaled data to raw values for display
        raw_vals = scaler.inverse_transform(X_sample[sample_id].reshape(1, -1))[0]
        
        col_feats, col_waterfall = st.columns([1, 2])
        
        with col_feats:
            st.markdown(f"**True Label**: {label_encoder.inverse_transform([sample_labels[sample_id]])[0]}")
            feats_df = pd.DataFrame({
                'Feature': feature_names,
                'Value': raw_vals
            })
            st.dataframe(feats_df, use_container_width=True)
            
        with col_waterfall:
            st.markdown("#### Feature Influence Waterfall")
            # Create a simple matplotlib representation of SHAP waterfall/force for this prediction
            # Since SHAP objects might be complex, we can plot horizontal bar of SHAP values for the predicted class
            pred_probs = models['Random Forest'].predict_proba(X_sample[sample_id].reshape(1, -1))[0]
            pred_class = np.argmax(pred_probs)
            pred_class_label = label_encoder.classes_[pred_class]
            
            st.markdown(f"**Predicted Class**: `{pred_class_label}` (Confidence: {pred_probs[pred_class]*100:.1f}%)")
            
            # Get SHAP values for the predicted class
            # shap_values is a list of arrays (one per class) or a single array
            if isinstance(shap_values, list):
                class_shap = shap_values[pred_class][sample_id]
            else:
                class_shap = shap_values[sample_id, :, pred_class] if len(shap_values.shape) > 2 else shap_values[sample_id]
                
            fig, ax = plt.subplots(figsize=(6, 4), facecolor='#0e1117')
            ax.set_facecolor('#161b22')
            
            sorted_indices = np.argsort(np.abs(class_shap))[-8:]
            ax.barh(np.array(feature_names)[sorted_indices], class_shap[sorted_indices], color=['#56d364' if x > 0 else '#f85149' for x in class_shap[sorted_indices]])
            ax.set_title(f"Top Feature Contributions for class: {pred_class_label}", color='white')
            ax.tick_params(colors='white')
            plt.tight_layout()
            st.pyplot(fig)

# ----------------- Tab 3: Real-time Packet Simulation -----------------
with tab_simulation:
    st.header("Real-time Packet Classification Simulation")
    st.markdown("Simulate a stream of incoming network packets and watch the machine learning classifier analyze them in real-time.")
    
    col_sim_ctrl, col_sim_stats = st.columns([1, 2])
    
    selected_sim_model = col_sim_ctrl.selectbox("Select Active Model:", list(models.keys()))
    sim_speed = col_sim_ctrl.slider("Packet Frequency (s):", 0.1, 2.0, 0.5)
    
    # Custom packet insertion
    st.markdown("### Manual Packet Classifier")
    with st.expander("Or manually input values to test a single custom packet"):
        col_in1, col_in2, col_in3 = st.columns(3)
        dest_port = col_in1.number_input("Destination Port", min_value=0, max_value=65535, value=80)
        flow_duration = col_in2.number_input("Flow Duration (us)", min_value=1, value=1000)
        total_fwd_pkts = col_in3.number_input("Total Fwd Packets", min_value=1, value=5)
        
        col_in4, col_in5, col_in6 = st.columns(3)
        total_bwd_pkts = col_in4.number_input("Total Bwd Packets", min_value=0, value=5)
        tot_len_fwd = col_in5.number_input("Total Length of Fwd Packets", min_value=0, value=250)
        tot_len_bwd = col_in6.number_input("Total Length of Bwd Packets", min_value=0, value=500)
        
        if st.button("Predict Custom Packet"):
            # Prepare data
            # Destination Port, Flow Duration, Total Fwd Packets, Total Backward Packets, Total Length of Fwd Packets, Total Length of Bwd Packets, Fwd Packet Length Mean, Bwd Packet Length Mean, Flow Bytes/s, Flow Packets/s, Flow IAT Mean, Packet Length Mean, Packet Length Std, Init_Win_bytes_forward, Init_Win_bytes_backward
            fwd_mean = tot_len_fwd / total_fwd_pkts
            bwd_mean = tot_len_bwd / max(1, total_bwd_pkts)
            flow_sec = flow_duration / 1e6
            flow_bytes_s = (tot_len_fwd + tot_len_bwd) / max(0.000001, flow_sec)
            flow_pkts_s = (total_fwd_pkts + total_bwd_pkts) / max(0.000001, flow_sec)
            iat_mean = flow_duration / (total_fwd_pkts + total_bwd_pkts)
            
            all_lens = [fwd_mean] * int(total_fwd_pkts) + [bwd_mean] * int(total_bwd_pkts)
            pkt_len_mean = np.mean(all_lens)
            pkt_len_std = np.std(all_lens)
            
            custom_data = np.array([[
                dest_port, flow_duration, total_fwd_pkts, total_bwd_pkts, tot_len_fwd, tot_len_bwd,
                fwd_mean, bwd_mean, flow_bytes_s, flow_pkts_s, iat_mean, pkt_len_mean, pkt_len_std,
                8192, 8192
            ]])
            
            scaled_custom = scaler.transform(custom_data)
            pred_encoded = models[selected_sim_model].predict(scaled_custom)[0]
            pred_class = label_encoder.inverse_transform([pred_encoded])[0]
            
            if pred_class == 'BENIGN':
                st.success(f"Prediction: **{pred_class}** ✅")
            else:
                st.error(f"Prediction: **{pred_class}** 🚨 (Intrusion Detected!)")
                
    st.markdown("---")
    
    # Stream/Simulation block
    if 'sim_running' not in st.session_state:
        st.session_state.sim_running = False
    if 'sim_packets' not in st.session_state:
        st.session_state.sim_packets = []
        
    start_sim = st.button("▶️ Start Live Packet Stream Simulation")
    stop_sim = st.button("⏹️ Stop Simulation")
    
    if start_sim:
        st.session_state.sim_running = True
    if stop_sim:
        st.session_state.sim_running = False
        
    placeholder = st.empty()
    
    # Read sample CSV to stream from
    sample_df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'cicids2017_sample.csv'))
    
    # Statistics and packet list update loop
    if st.session_state.sim_running:
        st.info("Simulation running. Scroll down to see live classification list.")
        while st.session_state.sim_running:
            # Pick random index from sample
            idx = np.random.randint(0, len(sample_df))
            row = sample_df.iloc[idx].copy()
            true_label = row['Label']
            
            # Predict
            feats = row.drop('Label').values.reshape(1, -1)
            feats_scaled = scaler.transform(feats)
            pred_enc = models[selected_sim_model].predict(feats_scaled)[0]
            pred_label = label_encoder.inverse_transform([pred_enc])[0]
            
            # Append packet data
            packet_info = {
                'Time': time.strftime("%H:%M:%S"),
                'Destination Port': int(row['Destination Port']),
                'Duration (us)': int(row['Flow Duration']),
                'Fwd Packets': int(row['Total Fwd Packets']),
                'Bwd Packets': int(row['Total Backward Packets']),
                'True Label': true_label,
                'Predicted': pred_label,
                'Status': '✅ SECURE' if pred_label == 'BENIGN' else '🚨 ATTACK'
            }
            
            st.session_state.sim_packets.insert(0, packet_info)
            if len(st.session_state.sim_packets) > 50:
                st.session_state.sim_packets.pop()
                
            # Render stats
            with placeholder.container():
                # Show top level stats
                df_sim = pd.DataFrame(st.session_state.sim_packets)
                total_flowed = len(df_sim)
                attacks_detected = len(df_sim[df_sim['Status'] == '🚨 ATTACK'])
                
                c_s1, c_s2, c_s3 = st.columns(3)
                c_s1.metric("Packets Processed", total_flowed)
                c_s2.metric("Intrusions Blocked", attacks_detected)
                c_s3.metric("Current Active Model", selected_sim_model)
                
                st.dataframe(df_sim, use_container_width=True)
                
            time.sleep(sim_speed)

# ----------------- Tab 4: Inference Speed Benchmark -----------------
with tab_benchmarks:
    st.header("Comparative Inference Speed Benchmark")
    st.markdown("""
        In live intrusion detection, **inference speed** is crucial. If the ML classifier cannot keep up with
        high network throughput, it creates packets buffers or drops packets, exposing the network.
    """)
    
    benchmark_size = st.slider("Select Benchmark Sample Size (packets):", 100, 2000, 500)
    
    if st.button("🚀 Run Live Speed Benchmark"):
        # Select sample
        raw_sample = sample_df.drop(columns=['Label']).sample(n=benchmark_size, random_state=42).values
        scaled_sample = scaler.transform(raw_sample)
        
        bench_results = {}
        
        for name, model in models.items():
            times = []
            # Run multiple single predictions to measure distribution
            for i in range(min(benchmark_size, 100)):
                s_t = time.time()
                _ = model.predict(scaled_sample[i].reshape(1, -1))
                times.append((time.time() - s_t) * 1e6)  # microseconds
                
            bench_results[name] = times
            
        fig, ax = plt.subplots(figsize=(10, 5), facecolor='#0e1117')
        ax.set_facecolor('#161b22')
        
        # Plot boxplot or violin plot
        ax.boxplot([bench_results[name] for name in models], labels=list(models.keys()))
        ax.set_ylabel('Inference Time per Packet (microseconds)', color='white')
        ax.set_title('Inference Speed Distribution (Lower is Better)', color='white')
        ax.tick_params(colors='white')
        plt.yscale('log')  # Log scale for readability
        plt.tight_layout()
        st.pyplot(fig)
        
        # Average print
        for name in models:
            avg_t = np.mean(bench_results[name])
            st.write(f"- **{name}**: Average {avg_t:.2f} microseconds per packet ({1e6/avg_t:.1f} packets/sec throughput)")
