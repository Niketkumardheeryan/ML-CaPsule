# Learning Rules in Artificial Neural Networks (ANN)

## Introduction

Learning rules are essential components of Artificial Neural Networks (ANNs) that govern how the network updates its weights and biases. This document focuses on two fundamental learning rules: Hebbian Learning and Adaline (Adaptive Linear Neuron) Learning.

## 1. Hebbian Learning

Hebbian Learning, proposed by Donald Hebb in 1949, is one of the earliest and simplest learning rules in neural networks. It is based on the principle that neurons that fire together, wire together.

### Basic Principle

The strength of a connection between two neurons increases if both neurons are activated simultaneously.

### Mathematical Formulation

For neurons $i$ and $j$ with activation values $x_i$ and $x_j$, the weight update $\Delta w_{ij}$ is given by:

$$\Delta w_{ij} = \eta x_i x_j$$

Where:
- $\Delta w_{ij}$ is the change in weight between neurons $i$ and $j$
- $\eta$ is the learning rate
- $x_i$ is the output of the presynaptic neuron
- $x_j$ is the output of the postsynaptic neuron

### Variations

1. **Oja's Rule**: A modification of Hebbian learning that includes weight normalization:

   $$\Delta w_{ij} = \eta(x_i x_j - \alpha y_j^2 w_{ij})$$

   Where $y_j$ is the output of neuron $j$ and $\alpha$ is a forgetting factor.

2. **Generalized Hebbian Algorithm (GHA)**: Extends Oja's rule to multiple outputs:

   $$\Delta W = \eta(xy^T - \text{lower}(Wy^Ty))$$

   Where $\text{lower}()$ denotes the lower triangular part of a matrix.

## 2. Adaline Learning (Widrow-Hoff Learning Rule)

Adaline (Adaptive Linear Neuron) Learning, developed by Bernard Widrow and Marcian Hoff in 1960, is a single-layer neural network that uses linear activation functions.

### Basic Principle

Adaline learning aims to minimize the mean squared error between the desired output and the actual output of the neuron.

### Mathematical Formulation

For an input vector $\mathbf{x}$ and desired output $d$, the weight update is given by:

$$ \Delta \mathbf{w} = \eta(d - y)\mathbf{x} $$

Where:
- $\Delta \mathbf{w}$ is the change in weight vector
- $\eta$ is the learning rate
- $d$ is the desired output
- $y = \mathbf{w}^T\mathbf{x}$ is the actual output
- $\mathbf{x}$ is the input vector

### Learning Process

1. Initialize weights randomly
2. For each training example:
3. 
   a. Calculate the output:
   
    $y = \mathbf{w}^T\mathbf{x}$
   
   b. Update weights:
   
  $$w_{new} = w_{old} + \eta(d - y)x$$
   
5. Repeat step 2 until convergence or a maximum number of epochs is reached

### Comparison with Perceptron Learning

While similar to the perceptron learning rule, Adaline uses the actual output value for weight updates, not just the sign of the output. This allows for more precise weight adjustments.

## Conclusion

Both Hebbian and Adaline learning rules play crucial roles in the development of neural network theory:

- Hebbian Learning provides a biological inspiration for neural learning and is fundamental in unsupervised learning scenarios.
- Adaline Learning introduces the concept of minimizing error, which is a cornerstone of many modern learning algorithms, including backpropagation in deep neural networks.

Understanding these basic learning rules provides insight into more complex learning algorithms used in deep learning and helps in appreciating the historical development of neural network theory.


## How to Use This Repository

- Clone this repository to your local machine.

```bash
  git clone https://github.com/Niketkumardheeryan/ML-CaPsule/Learning Rules In ANN
```
- For Python implementations and visualizations:

1. Ensure you have Jupyter Notebook installed 

```bash
  pip install jupyter
```
2. Navigate to the project directory in your terminal.
3. Open learning_rules.ipynb.
