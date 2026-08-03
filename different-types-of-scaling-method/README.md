
# Different Types Of Scaling For Machine Learning Model

# What is feature Scaling?

![Scaling](https://user-images.githubusercontent.com/69664057/122173223-2de47180-ce9f-11eb-9035-ae2d9b4a8f4c.png)


Feature scaling in machine learning is one of the most critical steps during the pre-processing of data before creating a machine learning model. 

Scaling can make a difference between a weak machine learning model and a better one.

The most common techniques of feature scaling are Normalization and Standardization.
Normalization is used when we want to bound our values between two numbers, typically, between [0,1] or [-1,1]. While Standardization transforms the data to have zero mean and a variance of 1, they make our data unitless. Refer to the below diagram, which shows how data looks after scaling in the X-Y plane.

![Feature scaling](https://user-images.githubusercontent.com/69664057/122173553-7865ee00-ce9f-11eb-9f54-7d4a0e7e7641.png)



# Why do we need Feature Transformation and Scaling?

Oftentimes, we have datasets in which different columns have different units – like one column can be in kilograms, while another column can be in centimeters. Furthermore, we can have columns like income which can range from 20,000 to 100,000, and even more; while an age column which can range from 0 to 100(at the most). Thus, Income is about 1,000 times larger than age.

But how can we be sure that the model treats both these variables equally? When we feed these features to the model as is, there is every chance that the income will influence the result more due to its larger value. But this doesn’t necessarily mean it is more important as a predictor. So, to give importance to both Age, and Income, we need feature scaling.

Another reason why feature scaling is applied is that few algorithms like Neural network gradient descent converge much faster with feature scaling than without it.

![Scaline3](https://user-images.githubusercontent.com/69664057/122173727-b236f480-ce9f-11eb-830d-23f4400a92d4.png)





## Few key points to note :

- Mean centering does not affect the covariance matrix
- Scaling of variables does affect the covariance matrix
- Standardizing affects the covariance

## How to Perform Scaling?

Below are the few ways we can do feature scaling.
- Min Max Scaler
- Standard Scaler
- Max Abs Scaler
- Robust Scaler
- Quantile Transformer Scaler
- Power Transformer Scaler
- Unit Vector Scaler

  
