import warnings
import pandas as pd
import numpy as np
import os
import joblib
from  sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
warnings.filterwarnings('ignore')


def load_data(data_path = os.path.join('data','Data.csv')):
    """Load data from CSV file"""
    df = pd.read_csv(data_path)
    
    #Data Shape and columns 
    print(f"[+] Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"    Columns: {', '.join(df.columns)}")
    
    # Sample Data
    print("Sample Data:")
    print(df.sample(n=5))
    
    return df
 

def clean_data(df,n=50):
   
   print("Information about the columns")
   print(df.info())
   
   
   print("="*n)
   print("Describing Data :")
   print(df.describe())
   
   
   print("="*n)
   print("Null values present in data")
   miss_df = pd.DataFrame(df.isnull().sum(),columns=['Missing Values']) 
   print(miss_df[miss_df['Missing Values'] > 0])
   print(f"Replacing null values with {np.round(df['age'].mean(), 0)}")
   df['age'] = df['age'].fillna(np.round(df['age'].mean(), 0))
   
   
   print("="*n)
   print(f"Dropping the row with age {df['age'].max()}")
   df = df[df['age'] != df['age'].max()]
   
   
   print("="*n)
   print("Object columns and their unique values")
   for col in df.select_dtypes('object').columns:
    print(f' column names :- {col}\n')
    print(f' Unique values: \n {df[col].unique().tolist()} \n')
    print('-----------------------------------------------------------------------')
    
    
   print("="*n)
   print("Replace the Relation with '?' values as maximum frequency mode")
   df['relation'] = df['relation'].replace('?',df['relation'].mode()[0])
   print(df['relation'].unique())
   
   print("Replace the ethnicity values with others value")
   df['ethnicity'] = df['ethnicity'].replace('?','Others')
   df['ethnicity'] = df['ethnicity'].replace('others','Others')
   print(df['ethnicity'].unique())
   print("="*n)
   return df

def preprocessing_data(df, test_size=0.25,n=50):
   
   print("Dropping 'age_desc' and 'used_app_before' columns")
   df = df.drop(['age_desc', 'used_app_before'], axis=1)
   
   print("="*n)
   print("Splitting data into Features and Labels")
   x = df.drop(['Class/ASD'],axis=1)
   y = df['Class/ASD']
   X = pd.get_dummies(x)
   Y = y.replace({"YES": int(1), "NO": int(0)}).astype(int)
   print(f"Shape of feature matrix : {X.shape[0]} rows, {X.shape[1]} columns")
   print(f"Shape of of label matrix :  {Y.shape[0]} rows, 1 columns")
   print("Feature matrix columns type")
   print(X.info())
   
   print("Saving feature column names")
   if not os.path.exists('saved_others'):
      os.mkdir('saved_others')
   
   joblib.dump(
      X.columns.to_list(),
      os.path.join('saved_others','feature_columns.pkl') 
      )
   
   print(f"Saved feature column names  : {os.path.join('saved_others','feature_columns.pkl')} ")
   print("="*n)
   print("Splitting into Train and Test data ")
   X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=test_size)
   
   print("Dataset with testsize of 25%")
   print(f"Shape of X Training dataset = {np.shape(X_train)}")
   print(f"Shape of Y Training dataset = {np.shape(y_train)}")
   print(f"Shape of X Testing dataset = {np.shape(X_test)}")
   print(f"Shape of Y Testing dataset = {np.shape(y_test)}\n")
   
   
   return X_train,X_test,y_train,y_test
   

def scaling_data(X_train,X_test, n=50):
   print("="*n)
   print("Scaling Train and Test Data")
   
   scaler = StandardScaler()
   
   scaler.fit(X_train)
   
   X_train = scaler.transform(X_train)
   X_test = scaler.transform(X_test)
   
   print("Saving Scaler for further usage")
   
   if not os.path.exists('saved_others'):
      os.mkdir('saved_others')
      
   joblib.dump(
      scaler,
      os.path.join('saved_others','scaler.pkl')
      )
   
   print(f"Scaling and Saving scaler completed Path : {os.path.join('saved_others','scaler.pkl')}")
   return X_train, X_test
   
   

def preprocessing_result():
   print("Staring Loading Data and Preprocessing")
   
   main_df = load_data()
   
   cleaned_df = clean_data(main_df)
   
   X_train,X_test,y_train,y_test = preprocessing_data(cleaned_df)
   
   X_train,X_test = scaling_data(X_train=X_train,X_test=X_test)
   
   print("Completed Preprocessing")
   
   return X_train,X_test,y_train,y_test

if __name__ == "__main__":
   preprocessing_result()
