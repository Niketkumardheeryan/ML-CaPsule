## Logistic Regression model to predict diabetes

### Description
To predict the presense of diabetes or pre-diabetes, this model uses a 50-50 binary split dataset. The entire dataset has about 70,000 instances.
To account for  computational power, the dataset has been reduced to about 7000 instances, in a random scaling. 
The trained parameters of the model are stored in a file which is then retrieved to predict the onset of diabetes. 
Additionally, the certain features have been omitted in favour of feasibility for the user.

### Data for the model
Features used for this model are
* Diabetes_binary - 0 for no diabetes and 1 for diabetes or prediabetes
* HighBP - 0 for not high and 1 for high BP
* HighChol - 0 for not high cholestrol and 1 for high cholestrol
* CholCheck - 0 for not checked cholestrol in last 5 years and 1 for checked.
* BMI - body mass index
* Smoker - 1 for smoker and 0 for not smoker
* Stroke - (Ever told) you had a stroke. 0 = no 1 = yes
* HeartDiseaseOrAttack - coronary heart disease (CHD) or myocardial infarction (MI) 0 = no 1 = yes
* PhysActicity - physical activity in past 30 days - not including job 0 = no 1 = yes
* Fruits - Consume Fruit 1 or more times per day 0 = no 1 = yes
* Veggies - Consume Vegetables 1 or more times per day 0 = no 1 = yes
* HvyAlcoholConsmp - (adult men >=14 drinks per week and adult women>=7 drinks per week) 0 = no 1 = yes
* AnyHealthCare - Have any kind of health care coverage, including health insurance, prepaid plans such as HMO, etc. 0 = no 1 = yes
* NoDocbcCost - Was there a time in the past 12 months when you needed to see a doctor but could not because of cost? 0 = no 1 = yes
* GenHlth - Would you say that in general your health is: scale 1-5 1 = excellent 2 = very good 3 = good 4 = fair 5 = poor
* MentHealth - days of poor mental health scale 1-30 days
* PhysHealth - physical illness or injury days in past 30 days scale 1-30
* DiffWalk - Do you have serious difficulty walking or climbing stairs? 0 = no 1 = yes

### Source of Dataset 
Binary split

https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset?select=diabetes_binary_5050split_health_indicators_BRFSS2015.csv

Actual dataset 

https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset?select=diabetes_012_health_indicators_BRFSS2015.csv

### Libraries used
* Numpy
* Matplotlib
* Pandas
* Sklearn
* Streamlit

### Software used
* Jupyter notebook
* Python


