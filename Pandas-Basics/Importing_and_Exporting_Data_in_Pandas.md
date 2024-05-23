# Importing_and_Exporting_Data_in_Pandas

>Created by Krishna Kaushik

- **Now we're able to create `Series` and `DataFrames` in pandas, but we usually do not do this , in practice we import the data which is in the form of .csv (Comma Seperated Values) , a spreadsheet file or something similar.**

- *Good news is that pandas allows for easy importing of data like this through functions such as ``pd.read_csv()`` and ``pd.read_excel()`` for Microsoft Excel files.*

## 1. Importing from a Google sheet to a pandas dataframe

*Let's say that you wanted to get the information from Google Sheet document into a pandas DataFrame.*.

*You could export it as a .csv file and then import it using ``pd.read_csv()``.*

*In this case, the exported .csv file is called `Titanic.csv`*


```python
## Importing Titanic Data set 
import pandas as pd

titanic_df= pd.read_csv("https://raw.githubusercontent.com/kRiShNa-429407/ML-CaPsule/master/Pandas-Basics/Datasets/Titanic.csv")
titanic_df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>pclass</th>
      <th>survived</th>
      <th>name</th>
      <th>sex</th>
      <th>age</th>
      <th>sibsp</th>
      <th>parch</th>
      <th>ticket</th>
      <th>fare</th>
      <th>cabin</th>
      <th>embarked</th>
      <th>boat</th>
      <th>body</th>
      <th>home.dest</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>Allen, Miss. Elisabeth Walton</td>
      <td>female</td>
      <td>29.00</td>
      <td>0</td>
      <td>0</td>
      <td>24160</td>
      <td>211.3375</td>
      <td>B5</td>
      <td>S</td>
      <td>2</td>
      <td>NaN</td>
      <td>St Louis, MO</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>Allison, Master. Hudson Trevor</td>
      <td>male</td>
      <td>0.92</td>
      <td>1</td>
      <td>2</td>
      <td>113781</td>
      <td>151.5500</td>
      <td>C22 C26</td>
      <td>S</td>
      <td>11</td>
      <td>NaN</td>
      <td>Montreal, PQ / Chesterville, ON</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>0</td>
      <td>Allison, Miss. Helen Loraine</td>
      <td>female</td>
      <td>2.00</td>
      <td>1</td>
      <td>2</td>
      <td>113781</td>
      <td>151.5500</td>
      <td>C22 C26</td>
      <td>S</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Montreal, PQ / Chesterville, ON</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>0</td>
      <td>Allison, Mr. Hudson Joshua Creighton</td>
      <td>male</td>
      <td>30.00</td>
      <td>1</td>
      <td>2</td>
      <td>113781</td>
      <td>151.5500</td>
      <td>C22 C26</td>
      <td>S</td>
      <td>NaN</td>
      <td>135.0</td>
      <td>Montreal, PQ / Chesterville, ON</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0</td>
      <td>Allison, Mrs. Hudson J C (Bessie Waldo Daniels)</td>
      <td>female</td>
      <td>25.00</td>
      <td>1</td>
      <td>2</td>
      <td>113781</td>
      <td>151.5500</td>
      <td>C22 C26</td>
      <td>S</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Montreal, PQ / Chesterville, ON</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1304</th>
      <td>3</td>
      <td>0</td>
      <td>Zabour, Miss. Hileni</td>
      <td>female</td>
      <td>14.50</td>
      <td>1</td>
      <td>0</td>
      <td>2665</td>
      <td>14.4542</td>
      <td>NaN</td>
      <td>C</td>
      <td>NaN</td>
      <td>328.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1305</th>
      <td>3</td>
      <td>0</td>
      <td>Zabour, Miss. Thamine</td>
      <td>female</td>
      <td>NaN</td>
      <td>1</td>
      <td>0</td>
      <td>2665</td>
      <td>14.4542</td>
      <td>NaN</td>
      <td>C</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1306</th>
      <td>3</td>
      <td>0</td>
      <td>Zakarian, Mr. Mapriededer</td>
      <td>male</td>
      <td>26.50</td>
      <td>0</td>
      <td>0</td>
      <td>2656</td>
      <td>7.2250</td>
      <td>NaN</td>
      <td>C</td>
      <td>NaN</td>
      <td>304.0</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1307</th>
      <td>3</td>
      <td>0</td>
      <td>Zakarian, Mr. Ortin</td>
      <td>male</td>
      <td>27.00</td>
      <td>0</td>
      <td>0</td>
      <td>2670</td>
      <td>7.2250</td>
      <td>NaN</td>
      <td>C</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1308</th>
      <td>3</td>
      <td>0</td>
      <td>Zimmerman, Mr. Leo</td>
      <td>male</td>
      <td>29.00</td>
      <td>0</td>
      <td>0</td>
      <td>315082</td>
      <td>7.8750</td>
      <td>NaN</td>
      <td>S</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>1309 rows × 14 columns</p>
</div>



The dataset I am using here for your reference is taken from the same folder i.e ``Pandas- Basics/Datasets`` (https://raw.githubusercontent.com/kRiShNa-429407/ML-CaPsule/master/Pandas-Basics/Datasets/Titanic.csv) I uploaded it you can use it from there.

**Now we've got the same data from the Google Spreadsheet , but now available as ``pandas DataFrame`` which means we can now apply all pandas functionality over it.**

#### Note: The quiet important thing i am telling is that ``pd.read_csv()`` takes the location of the file (which is in your current working directory) or the hyperlink of the dataset from the other source.

#### But if you want to import the data from Github you can't directly use its link , you have to first convert it to raw by clicking on the raw button present in the repo .

#### Also you can't use the data directly from `Kaggle` you have to use ``kaggle API``

## 2. The Anatomy of DataFrame

**Different functions use different labels for different things, and can get a little confusing.**

- Rows are refer as ``axis=0``
- columns are refer as ``axis=1``

## 3. Exporting Data

**OK, so after you've made a few changes to your data, you might want to export it and save it so someone else can access the changes.**

**pandas allows you to export ``DataFrame's`` to ``.csv`` format using ``.to_csv()``, or to a spreadsheet format using .to_excel().**

### Exporting a dataframe to a CSV

**We haven't made any changes yet to the ``titanic_df`` DataFrame but let's try to export it.**


```python
#Export the titanic_df DataFrame to csv
titanic_df.to_csv("exported_titanic.csv")  
```

Running this will save a file called ``exported_titanic.csv`` to the current folder.
