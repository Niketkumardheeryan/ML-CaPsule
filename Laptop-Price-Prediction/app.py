import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load files
df = pickle.load(open('df.pkl', 'rb'))
pipe = pickle.load(open('pipe.pkl', 'rb'))

st.title("💻 Laptop Price Predictor")

st.write("Enter Laptop Specifications")

# Company
company = st.selectbox(
    'Brand',
    sorted(df['Company'].unique())
)

# Type
type_name = st.selectbox(
    'Type',
    sorted(df['TypeName'].unique())
)

# RAM
ram = st.selectbox(
    'RAM (GB)',
    [2, 4, 6, 8, 12, 16, 24, 32, 64]
)

# Weight
weight = st.number_input(
    'Weight of Laptop (kg)',
    min_value=0.5,
    max_value=5.0,
    value=1.5,
    step=0.1
)

# Touchscreen
touchscreen = st.selectbox(
    'Touchscreen',
    ['No', 'Yes']
)

# IPS
ips = st.selectbox(
    'IPS Display',
    ['No', 'Yes']
)

# Screen Size
inches = st.number_input(
    'Screen Size (Inches)',
    min_value=10.0,
    max_value=20.0,
    value=15.6
)

# Resolution
resolution = st.selectbox(
    'Screen Resolution',
    [
        '1920x1080',
        '1366x768',
        '1600x900',
        '3840x2160',
        '2560x1440',
        '2560x1600',
        '2880x1800',
        '2304x1440'
    ]
)

# CPU
cpu = st.selectbox(
    'CPU Brand',
    sorted(df['Cpu Brand'].unique())
)

# HDD
hdd = st.selectbox(
    'HDD (GB)',
    [0, 128, 256, 500, 1000, 2000]
)

# SSD
ssd = st.selectbox(
    'SSD (GB)',
    [0, 8, 128, 256, 512, 1024, 2048]
)

# Hybrid
hybrid = st.selectbox(
    'Hybrid Storage (GB)',
    [0, 128, 256, 512, 1000]
)

# Flash Storage
flash_storage = st.selectbox(
    'Flash Storage (GB)',
    [0, 8, 16, 32, 64, 128, 256, 512]
)

# GPU
gpu = st.selectbox(
    'GPU Brand',
    sorted(df['Gpu Brand'].unique())
)

# OS
os = st.selectbox(
    'Operating System',
    sorted(df['OS'].unique())
)

if st.button('Predict Price'):

    touchscreen = 1 if touchscreen == 'Yes' else 0
    ips = 1 if ips == 'Yes' else 0

    X_res = int(resolution.split('x')[0])
    Y_res = int(resolution.split('x')[1])

    ppi = ((X_res**2 + Y_res**2)**0.5) / inches

    query = pd.DataFrame(
        [[
            company,
            type_name,
            inches,
            ram,
            weight,
            cpu,
            touchscreen,
            ips,
            ppi,
            hdd,
            ssd,
            hybrid,
            flash_storage,
            gpu,
            os
        ]],
        columns=[
            'Company',
            'TypeName',
            'Inches',
            'Ram',
            'Weight',
            'Cpu Brand',
            'Touchscreen',
            'IPS',
            'ppi',
            'HDD',
            'SSD',
            'Hybrid',
            'Flash_Storage',
            'Gpu Brand',
            'OS'
        ]
    )

    prediction = np.exp(pipe.predict(query)[0])

    st.success(f"Estimated Price: ₹ {int(prediction):,}")