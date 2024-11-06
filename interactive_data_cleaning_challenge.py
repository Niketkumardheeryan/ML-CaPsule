import pandas as pd
import numpy as np

# Create a small dataset with missing values
data = {
    'Age': [25, np.nan, 30, 35, np.nan, 40, 45],
    'Salary': [50000, 55000, np.nan, 60000, 65000, np.nan, 70000],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio']
}

df = pd.DataFrame(data) # Convert the dataset into a DataFrame

def display_original_data(): # Show the original DataFrame with missing values
    print("Original DataFrame with Missing Values:")
    print(df)
    print("\nMissing values (True = Missing, False = Not Missing):")
    print(df.isnull())

def fill_missing_values(method='mean'): # Function to fill missing values in 'Age' and 'Salary' columns
    if method == 'mean':
        df['Age'] = df['Age'].fillna(df['Age'].mean())
        df['Salary'] = df['Salary'].fillna(df['Salary'].mean())
    elif method == 'median':
        df['Age'] = df['Age'].fillna(df['Age'].median())
        df['Salary'] = df['Salary'].fillna(df['Salary'].median())
    elif method == 'mode':
        df['Age'] = df['Age'].fillna(df['Age'].mode()[0])
        df['Salary'] = df['Salary'].fillna(df['Salary'].mode()[0])
    else:
        print("Invalid method! Please choose from 'mean', 'median', or 'mode'.")

def provide_feedback(): # Provide feedback based on missing values
    if df.isnull().sum().sum() == 0:
        print("\n✅ Well done! All missing values have been filled.")
    else:
        print("\n❌ Some missing values are still present. Make sure you have filled all missing values correctly.")

def interactive_challenge(): # Interactive challenge instructions
    print("Welcome to the Data Cleaning Challenge!")
    print("\nTask: Your goal is to fill the missing values in the 'Age' and 'Salary' columns.")
    print("You can fill missing values using one of the following methods: 'mean', 'median', or 'mode'.")
    
    display_original_data()   # Show the original data
    
    method = input("\nEnter the method to fill missing values ('mean', 'median', 'mode'): ").lower()   # Ask user to choose a method for filling missing values
    
    fill_missing_values(method)   # Fill missing values based on user's choice
    
    print("\nDataFrame after cleaning:") # Display the cleaned data and provide feedback
    print(df)
    provide_feedback()

if __name__ == "__main__":
    interactive_challenge()
