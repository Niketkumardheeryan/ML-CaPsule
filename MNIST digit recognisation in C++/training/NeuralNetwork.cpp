#include "neuralnetwork.h"
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <fstream>
#include <stdexcept>

using namespace std;

static double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

static double sigmoidDerivative(double x) {
    return x * (1.0 - x);
}

NeuralNetwork::NeuralNetwork(int inputNodes, int hiddenNodes, int outputNodes, double learningRate)
    : inputNodes(inputNodes), hiddenNodes(hiddenNodes), outputNodes(outputNodes), learningRate(learningRate) {

    srand((unsigned int) time(nullptr));

    weightsInputHidden.resize(hiddenNodes, vector<double>(inputNodes));
    for (int i = 0; i < hiddenNodes; i++) {
        for (int j = 0; j < inputNodes; j++) {
            weightsInputHidden[i][j] = ((double) rand() / RAND_MAX) - 0.5;
        }
    }

    weightsHiddenOutput.resize(outputNodes, vector<double>(hiddenNodes));
    for (int i = 0; i < outputNodes; i++) {
        for (int j = 0; j < hiddenNodes; j++) {
            weightsHiddenOutput[i][j] = ((double) rand() / RAND_MAX) - 0.5;
        }
    }

    biasHidden.resize(hiddenNodes);
    for (int i = 0; i < hiddenNodes; i++) {
        biasHidden[i] = ((double) rand() / RAND_MAX) - 0.5;
    }

    biasOutput.resize(outputNodes);
    for (int i = 0; i < outputNodes; i++) {
        biasOutput[i] = ((double) rand() / RAND_MAX) - 0.5;
    }
}

void NeuralNetwork::feedForwardDetailed(const vector<double>& inputs, vector<double>& hidden, vector<double>& outputs) {
    for (int i = 0; i < hiddenNodes; i++) {
        double sum = biasHidden[i];
        for (int j = 0; j < inputNodes; j++) {
            sum += weightsInputHidden[i][j] * inputs[j];
        }
        hidden[i] = sigmoid(sum);
    }

    for (int i = 0; i < outputNodes; i++) {
        double sum = biasOutput[i];
        for (int j = 0; j < hiddenNodes; j++) {
            sum += weightsHiddenOutput[i][j] * hidden[j];
        }
        outputs[i] = sigmoid(sum);
    }
}

void NeuralNetwork::train(const vector<double>& inputs, const vector<double>& targets) {
    vector<double> hidden(hiddenNodes);
    vector<double> outputs(outputNodes);
    feedForwardDetailed(inputs, hidden, outputs);

    vector<double> outputErrors(outputNodes);
    for (int i = 0; i < outputNodes; i++) {
        outputErrors[i] = targets[i] - outputs[i];
    }

    vector<double> outputGradients(outputNodes);
    for (int i = 0; i < outputNodes; i++) {
        outputGradients[i] = outputErrors[i] * sigmoidDerivative(outputs[i]);
        biasOutput[i] += learningRate * outputGradients[i];
    }

    vector<double> hiddenErrors(hiddenNodes, 0.0);
    for (int i = 0; i < hiddenNodes; i++) {
        for (int j = 0; j < outputNodes; j++) {
            hiddenErrors[i] += weightsHiddenOutput[j][i] * outputGradients[j];
        }
    }
    
    for (int i = 0; i < outputNodes; i++) {
        for (int j = 0; j < hiddenNodes; j++) {
            double delta = learningRate * outputGradients[i] * hidden[j];
            weightsHiddenOutput[i][j] += delta;
        }
    }

    vector<double> hiddenGradients(hiddenNodes);
    for (int i = 0; i < hiddenNodes; i++) {
        hiddenGradients[i] = hiddenErrors[i] * sigmoidDerivative(hidden[i]);
        biasHidden[i] += learningRate * hiddenGradients[i];
    }

    for (int i = 0; i < hiddenNodes; i++) {
        for (int j = 0; j < inputNodes; j++) {
            double delta = learningRate * hiddenGradients[i] * inputs[j];
            weightsInputHidden[i][j] += delta;
        }
    }
}

void NeuralNetwork::saveModel(const string& filename) {
    ofstream file(filename, ios::binary);
    if (!file.is_open()) throw runtime_error("Cannot open file for saving: " + filename);

    file.write((char*)&inputNodes, sizeof(inputNodes));
    file.write((char*)&hiddenNodes, sizeof(hiddenNodes));
    file.write((char*)&outputNodes, sizeof(outputNodes));
    file.write((char*)&learningRate, sizeof(learningRate));

    for (auto& row : weightsInputHidden)
        file.write((char*)row.data(), row.size() * sizeof(double));
    for (auto& row : weightsHiddenOutput)
        file.write((char*)row.data(), row.size() * sizeof(double));

    file.write((char*)biasHidden.data(), biasHidden.size() * sizeof(double));
    file.write((char*)biasOutput.data(), biasOutput.size() * sizeof(double));

    file.close();
    cout << "Model saved to " << filename << endl;
}