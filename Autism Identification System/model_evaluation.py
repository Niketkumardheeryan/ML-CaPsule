import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Tuple, Any, List

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
    roc_curve
)

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    """
    Builds a reusable scikit-learn ColumnTransformer based on the data types and unique counts
    of the input features in X.

    - Numeric features (int/float with > 2 unique values) are imputed (median) and standardized.
    - Categorical features (object/category) are imputed (most frequent) and one-hot encoded.
    - Binary/Indicator features (numeric with <= 2 unique values) are imputed (most frequent)
      and passed through without scaling to maintain binary interpretability.

    Args:
        X: pd.DataFrame containing only the feature columns.

    Returns:
        ColumnTransformer ready to be integrated into a Pipeline.
    """
    if X is None or X.empty:
        raise ValueError("Input feature DataFrame X is empty or None.")

    logger.info("Building ColumnTransformer preprocessor dynamically from inputs...")

    categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Separate numeric columns into binary/indicator features and continuous features
    numeric_dtypes = X.select_dtypes(include=['number']).columns.tolist()
    numeric_cols = []
    binary_cols = []
    
    for col in numeric_dtypes:
        if X[col].nunique() <= 2:
            binary_cols.append(col)
        else:
            numeric_cols.append(col)
            
    logger.info(f"Numeric features to scale: {numeric_cols}")
    logger.info(f"Categorical features to one-hot encode: {categorical_cols}")
    logger.info(f"Binary features to pass through: {binary_cols}")

    # Pipeline for scaling continuous numeric features
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # Pipeline for encoding categorical features
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Pipeline for binary indicator features (no scaling required, but imputer handles any NaNs)
    binary_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent'))
    ])

    transformers = []
    if numeric_cols:
        transformers.append(('num', numeric_transformer, numeric_cols))
    if categorical_cols:
        transformers.append(('cat', categorical_transformer, categorical_cols))
    if binary_cols:
        transformers.append(('bin', binary_transformer, binary_cols))

    preprocessor = ColumnTransformer(
        transformers=transformers,
        remainder='drop'  # drop any other column types that we don't specify
    )
    
    return preprocessor

def build_model_pipelines(preprocessor: ColumnTransformer, param_grid: Dict[str, Any] = None) -> Dict[str, Pipeline]:
    """
    Creates a dictionary of scikit-learn Pipelines combining the shared preprocessor
    with standard classification models.

    The supported models are:
    - LogisticRegression
    - SVC (with probability=True)
    - RandomForestClassifier
    - DummyClassifier (baseline)

    Args:
        preprocessor: ColumnTransformer built by build_preprocessor().
        param_grid: Optional dictionary mapping model name to the hyperparameters.
                    Example:
                    {
                        'LogisticRegression': {'C': 1.0},
                        'SVC': {'C': 1.0, 'kernel': 'rbf'},
                        'RandomForestClassifier': {'n_estimators': 100, 'max_depth': 5}
                    }

    Returns:
        A dictionary mapping model names (str) to their scikit-learn Pipeline objects.
    """
    if param_grid is None:
        param_grid = {}

    logger.info("Initializing model pipelines with custom hyperparameters...")

    # Logistic Regression
    lr_params = param_grid.get('LogisticRegression', {}).copy()
    if 'random_state' not in lr_params:
        lr_params['random_state'] = 42
    if 'max_iter' not in lr_params:
        lr_params['max_iter'] = 1000
    lr_model = LogisticRegression(**lr_params)

    # Support Vector Classifier
    svc_params = param_grid.get('SVC', {}).copy()
    if 'random_state' not in svc_params:
        svc_params['random_state'] = 42
    svc_params['probability'] = True  # Required for predicting probabilities (needed for ROC-AUC)
    svc_model = SVC(**svc_params)

    # Random Forest Classifier
    rf_params = param_grid.get('RandomForestClassifier', {}).copy()
    if 'random_state' not in rf_params:
        rf_params['random_state'] = 42
    rf_model = RandomForestClassifier(**rf_params)

    # Dummy Classifier (Baseline)
    dummy_params = param_grid.get('DummyClassifier', {}).copy()
    if 'strategy' not in dummy_params:
        dummy_params['strategy'] = 'prior'
    dummy_model = DummyClassifier(**dummy_params)

    pipelines = {
        'LogisticRegression': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', lr_model)]),
        'SVC': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', svc_model)]),
        'RandomForestClassifier': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', rf_model)]),
        'DummyClassifier': Pipeline(steps=[('preprocessor', preprocessor), ('classifier', dummy_model)])
    }

    return pipelines

def evaluate_models(
    pipelines: Dict[str, Pipeline],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series
) -> Tuple[pd.DataFrame, Dict[str, str], Dict[str, np.ndarray], Dict[str, Dict[str, Any]]]:
    """
    Trains each pipeline on the train sets and evaluates them on the test sets, computing
    reusable metrics, classification reports, confusion matrices, and ROC data.

    Args:
        pipelines: Dict of model name to Pipeline.
        X_train: Train features.
        X_test: Test features.
        y_train: Train labels.
        y_test: Test labels.

    Returns:
        metrics_df: pd.DataFrame comparing scores (Accuracy, Precision, Recall, F1, ROC-AUC).
        reports_dict: Dict mapping model name to classification report string.
        confusion_matrices: Dict mapping model name to 2x2 confusion matrix array.
        roc_data: Dict mapping model name to dictionary with 'fpr', 'tpr', 'auc' keys for plotting curves.
    """
    logger.info("Starting model training and evaluation...")

    # Ensure y is binary-integer coded for metric calculations (e.g. YES/NO mapping)
    def sanitize_labels(y: pd.Series) -> pd.Series:
        if y.dtype == object or isinstance(y.iloc[0], str):
            # Strip whitespace and convert to uppercase
            y_clean = y.astype(str).str.strip().str.upper()
            if set(y_clean.unique()).issubset({"YES", "NO", "1", "0", "1.0", "0.0"}):
                return y_clean.map({"YES": 1, "NO": 0, "1": 1, "0": 0, "1.0": 1, "0.0": 0})
        return y

    y_train_clean = sanitize_labels(y_train)
    y_test_clean = sanitize_labels(y_test)

    metrics_list = []
    reports_dict = {}
    confusion_matrices = {}
    roc_data = {}

    for name, pipeline in pipelines.items():
        logger.info(f"Training model: {name}...")
        try:
            # Fit pipeline
            pipeline.fit(X_train, y_train_clean)
            
            # Predict labels
            y_pred = pipeline.predict(X_test)
            # Ensure predictions are numeric 0/1 to align with y_test_clean
            if len(y_pred) > 0 and isinstance(y_pred[0], str):
                y_pred = pd.Series(y_pred).str.strip().str.upper().map({"YES": 1, "NO": 0, "1": 1, "0": 0}).values

            # Predict probabilities/decision scores for ROC-AUC
            y_prob = None
            if hasattr(pipeline.named_steps['classifier'], "predict_proba"):
                y_prob = pipeline.predict_proba(X_test)[:, 1]
            elif hasattr(pipeline.named_steps['classifier'], "decision_function"):
                y_prob = pipeline.decision_function(X_test)

            # Compute standard metrics
            accuracy = accuracy_score(y_test_clean, y_pred)
            precision = precision_score(y_test_clean, y_pred, zero_division=0)
            recall = recall_score(y_test_clean, y_pred, zero_division=0)
            f1 = f1_score(y_test_clean, y_pred, zero_division=0)
            
            roc_auc = np.nan
            if y_prob is not None:
                try:
                    roc_auc = roc_auc_score(y_test_clean, y_prob)
                    fpr, tpr, thresholds = roc_curve(y_test_clean, y_prob)
                    roc_data[name] = {
                        'fpr': fpr.tolist(),
                        'tpr': tpr.tolist(),
                        'auc': roc_auc
                    }
                except Exception as e:
                    logger.warning(f"Failed to calculate ROC-AUC for {name}: {e}")

            metrics_list.append({
                'Model': name,
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1,
                'ROC-AUC': roc_auc
            })

            # Store classification report
            report = classification_report(y_test_clean, y_pred, zero_division=0, target_names=["No ASD", "ASD"])
            reports_dict[name] = report

            # Store confusion matrix
            cm = confusion_matrix(y_test_clean, y_pred)
            confusion_matrices[name] = cm

        except Exception as e:
            logger.error(f"Error evaluating model {name}: {e}", exc_info=True)
            # Add an empty row for the metrics DataFrame to indicate failure
            metrics_list.append({
                'Model': name,
                'Accuracy': np.nan,
                'Precision': np.nan,
                'Recall': np.nan,
                'F1-Score': np.nan,
                'ROC-AUC': np.nan
            })

    metrics_df = pd.DataFrame(metrics_list)
    return metrics_df, reports_dict, confusion_matrices, roc_data

def plot_confusion_matrix(cm: np.ndarray, labels: List[str], normalize: bool = False) -> plt.Figure:
    """
    Plots a confusion matrix heatmap using Seaborn.

    Args:
        cm: 2x2 Numpy confusion matrix.
        labels: String representation of labels, e.g. ['No ASD', 'ASD'].
        normalize: Whether to calculate percentage rates instead of counts.

    Returns:
        Matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=(5, 4))
    
    if normalize:
        cm_display = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        # Handle nan elements if any division-by-zero occurs
        cm_display = np.nan_to_num(cm_display)
        fmt = '.2%'
        title = 'Normalized Confusion Matrix'
    else:
        cm_display = cm
        fmt = 'd'
        title = 'Absolute Confusion Matrix'

    sns.heatmap(
        cm_display, 
        annot=True, 
        fmt=fmt, 
        cmap='Blues', 
        xticklabels=labels, 
        yticklabels=labels, 
        ax=ax,
        cbar=True,
        annot_kws={"size": 11}
    )
    
    ax.set_ylabel('Actual Label', fontsize=10, fontweight='bold')
    ax.set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    plt.tight_layout()
    
    return fig

def plot_comparison(metrics_df: pd.DataFrame) -> plt.Figure:
    """
    Plots a grouped bar chart comparing performance metrics across models.

    Args:
        metrics_df: pd.DataFrame containing metrics generated by evaluate_models.

    Returns:
        Matplotlib Figure object.
    """
    # Exclude rows with NaNs (failed runs) and drop the ROC-AUC if it contains NaNs
    clean_df = metrics_df.dropna(subset=['Accuracy'])
    
    # Melt the metrics DataFrame for Seaborn compatibility
    value_vars = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    if 'ROC-AUC' in clean_df.columns and not clean_df['ROC-AUC'].isna().all():
        value_vars.append('ROC-AUC')
        
    melted_df = clean_df.melt(
        id_vars='Model', 
        value_vars=value_vars,
        var_name='Metric', 
        value_name='Score'
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Using modern, high-contrast palette
    sns.barplot(
        data=melted_df, 
        x='Model', 
        y='Score', 
        hue='Metric', 
        palette='muted', 
        ax=ax,
        edgecolor='black',
        linewidth=0.5
    )
    
    ax.set_ylim(0, 1.1)
    ax.set_ylabel('Score', fontsize=11, fontweight='bold')
    ax.set_xlabel('Model', fontsize=11, fontweight='bold')
    ax.set_title('Comparative Performance Evaluation', fontsize=13, fontweight='bold', pad=15)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values on top of the bars
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(
                f'{height:.2f}',
                (p.get_x() + p.get_width() / 2., height),
                ha='center', 
                va='center',
                xytext=(0, 6),
                textcoords='offset points',
                fontsize=8,
                fontweight='semibold'
            )
            
    ax.legend(title='Metrics', loc='lower right', framealpha=0.9, facecolor='white', edgecolor='gray')
    plt.tight_layout()
    
    return fig
