## Activation Functions
In deep learning,the role of the Activation Function is to transform the summed weighted input from the node into an output value to be fed to the next hidden layer or as output. 
### Types of Activation Functions

- **Binary Step Function** :

  Binary step function decides whether a neuron should be activated or not based on a threshold value.The input fed to the activation function is compared to a certain threshold
    - if the input is greater than it, the neuron is activated
    - else it is deactivated, i.e. its output is not passed on to the next hidden layer.
  ```
    f(x)={0 for x<0
          1 for x>=0}
  ```
- **Linear Activation Function** :

  The linear activation function doesn't do anything to the weighted sum of the input.Here, the activation is proportional to the input.
  ```
    f(x)=x
  ```
- **Non-Linear Activation Function**:

  Non-linear activation functions allow backpropagation,the stacking of multiple layers of neurons.The output would now be a non-linear combination of input passed through multiple layers.

### Different Activation Functions

- Linear

![image](https://user-images.githubusercontent.com/72400676/169813324-e562eb26-5db5-4c84-acd6-1dfb4bd975dc.png)

- ReLU

![image](https://user-images.githubusercontent.com/72400676/169812862-4c58be24-9ef5-4bb6-8f39-6fb44ff5f6a2.png)

- **Sigmoid Activation Function**
  The Sigmoid or Logistic Activation Function takes any real value as input and outputs values in the range of 0 to 1. The larger the input, the closer the output value will be to 1, whereas the smaller the input, the closer the output will be to 0.
  ![image](https://user-images.githubusercontent.com/72400676/169812982-cff4a7da-5231-4161-943b-90d8cadd97d2.png)

- eLU

![image](https://user-images.githubusercontent.com/72400676/169813244-6b692873-ebe1-4ea6-817e-5edba572e9b4.png)

- Swish ReLU

![image](https://user-images.githubusercontent.com/72400676/169813413-5503076c-bf04-4d1a-968a-c7960ccfe025.png)


- Tan H

![image](https://user-images.githubusercontent.com/72400676/169813999-fb3c2117-d610-4809-829b-9337df37be0a.png)

- PReLU

![image](https://user-images.githubusercontent.com/72400676/169814069-3218aae9-cd70-45ea-8f43-1f4e722412ba.png)

- Leaky ReLU

![image](https://user-images.githubusercontent.com/72400676/169814188-0ddbd89a-d123-4a6d-83bc-8e152f5fa117.png)


### Applications

### References

The images used in this documentation have been referenced from this [medium article](https://towardsdatascience.com/activation-functions-neural-networks-1cbd9f8d91d6)

#### CONTRIBUTED BY

[Shreya Ghosh](https://github.com/shreya024)
