import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.svm import SVC
import joblib

import seaborn as sns
import matplotlib.pyplot as plt



try:
    df=pd.read_csv('../../data/flood.csv')
except FileNotFoundError:
    print("\nError: 'flood.csv' not found.")
    exit()

new_columns=[]
for col in df.columns:
    new_col=col.lower()
    new_col=re.sub(r'[^a-zA-Z0-9]+', '_', new_col)
    new_col=new_col.strip('_')
    new_columns.append(new_col)
df.columns=new_columns

#Training
feature_names=['rainfall','temperature_c','humidity','water_level_m','elevation_m']
target_name='flood_occurred'

X=df[feature_names]
y=df[target_name]

X_train,X_test,y_train,y_test=train_test_split(X, y,test_size=0.2,random_state=42)


# --- FOR DATA CORRELATION ANALYSIS ---
# print(df['floods'].value_counts())
# print(df.corr(numeric_only=True)['floods'].sort_values(ascending=False))


#FIT
scaler=StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#Train SVM Model
X_test_scaled=scaler.transform(X_test)
# svm_model=SVC(kernel='rbf',C=10,gamma='scale')
svm_model=SVC(kernel='linear',random_state=42)
svm_model.fit(X_train_scaled,y_train)
y_pred = svm_model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")


#confuion matrix
print("\nConfusion Matrix:")
#print(confusion_matrix(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)

sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("SVM Confusion Matrix")
plt.show()

#class distribution report
sns.countplot(x='flood_occurred', data=df)
plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

importance = svm_model.coef_[0]

feature_importance = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})

feature_importance = feature_importance.sort_values(
    by='Importance',
    ascending=False
)
print(feature_importance)

#Visualize feature importance
plt.figure(figsize=(8,5))

plt.bar(
    feature_importance['Feature'],
    feature_importance['Importance']
)

plt.xlabel("Features")
plt.ylabel("Importance")
plt.title("SVM Feature Importance")

plt.xticks(rotation=45)

plt.show()


#SAVES OF MODEL AND SCALER
joblib.dump(svm_model,'../../models/svm_model.joblib')
joblib.dump(scaler,'../../models/svm_scaler.joblib')



print("Model and scaler have been trained and saved successfully!")
print("Files created: svm_model.joblib, scaler.joblib")