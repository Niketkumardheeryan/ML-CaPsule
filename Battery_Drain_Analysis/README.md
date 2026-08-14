# Battery Drain Analysis

## Overview

This project performs **exploratory data analysis (EDA)** on smartphone battery-drain data. The goal is to understand how device usage, system-resource utilization, environmental/device conditions, and categorical usage factors are associated with **battery drain per hour**.

## Objective

The main objective is to investigate patterns and relationships between:

- Screen-on time
- CPU usage
- Battery temperature
- Brightness level
- RAM usage
- App running
- Network type
- Charging state
- Usage mode

and the target variable:

**`Battery_Drop_Per_Hour`**

## Dataset

The notebook works with a dataset containing **2,503 records and 10 variables** before preprocessing.

### Variables

| Variable | Type | Description |
|---|---|---|
| `Screen_On_Time_min` | Numerical | Screen usage time |
| `CPU_Usage_%` | Numerical | CPU utilization |
| `Battery_Temperature_C` | Numerical | Battery temperature |
| `Battery_Drop_Per_Hour` | Numerical | Battery drain rate |
| `Brightness_Level_%` | Numerical | Screen brightness level |
| `RAM_Usage_MB` | Numerical | RAM utilization |
| `App_Running` | Categorical | Application running on the device |
| `Network_Type` | Categorical | Network connection type |
| `Charging_State` | Categorical | Device charging condition |
| `Usage_Mode` | Categorical | Device usage mode |

## Analysis Workflow

The notebook follows these major steps:

1. Import Python libraries
2. Load and inspect the dataset
3. Examine data types and dataset structure
4. Check for missing values
5. Remove rows containing missing values
6. Generate descriptive statistics
7. Analyze numerical-variable distributions
8. Identify potential outliers using box plots
9. Analyze relationships with `Battery_Drop_Per_Hour` using scatter plots
10. Compare battery drain across categorical variables using box/count plots
11. Use a pair plot for an overall view of numerical relationships
12. Draw conclusions from the exploratory analysis

## Data Cleaning

The dataset initially contains 2,503 observations.

Missing values were found in:

- `CPU_Usage_%`: 5 values
- `Battery_Temperature_C`: 5 values

The notebook removes rows containing missing values before continuing the analysis.

This results in approximately **2,493 observations** being used for the subsequent analysis.

Because the amount of missing data is very small relative to the original dataset, removing these records has limited impact on the overall dataset size.

# Key Findings

The following findings are supported by the analysis performed in the notebook:

1. **Battery drain is influenced by multiple usage-related factors.**  
   The analysis considers screen-on time, CPU usage, temperature, brightness, RAM usage, and categorical usage conditions rather than treating battery consumption as dependent on one variable.

2. **Screen-on time is an important variable to investigate.**  
   The scatter analysis between `Screen_On_Time_min` and `Battery_Drop_Per_Hour` helps examine whether longer screen usage is associated with greater battery consumption.

3. **CPU utilization is relevant to battery-consumption analysis.**  
   The relationship between `CPU_Usage_%` and `Battery_Drop_Per_Hour` provides insight into whether higher computational activity tends to occur alongside higher battery drain.

4. **Battery temperature provides useful contextual information.**  
   The comparison of `Battery_Temperature_C` with battery drain helps investigate how device operating conditions are associated with battery consumption.

5. **Brightness and RAM usage are additional factors worth considering.**  
   The notebook evaluates both variables against battery drain, allowing their relationships with battery consumption to be explored alongside the other numerical factors.

6. **Battery drain can vary across categorical conditions.**  
   Comparisons involving `App_Running`, `Network_Type`, `Charging_State`, and `Usage_Mode` allow differences in battery-drain distributions between usage conditions to be investigated.

7. **Correlation analysis is useful for identifying associations.**  
   The correlation heatmap provides a compact view of relationships among the numerical variables and helps identify which variables may deserve further investigation.

8. **The analysis is exploratory rather than causal.**  
   Correlation and visualization can identify associations, but they cannot establish that one variable directly causes battery drain. More rigorous statistical testing or predictive modeling would be required for causal or predictive claims.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Jupyter Notebook

## Project Structure

```text
Battery-Drain-Analysis/
│
├── Battery_Drain_Analysis.ipynb
├── requirements.txt
└── README.md
```

## How to Run

### 1. Clone/download the project

Place the notebook and dataset in the appropriate project directory.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Open the notebook

```bash
jupyter notebook Battery_Drain_Analysis.ipynb
```

You can also open the notebook directly in **JupyterLab** or **Google Colab**.

