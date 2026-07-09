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
    weightsHiddenOutput.resize(outputNodes, vector<double>(hiddenNodes));
    biasHidden.resize(hiddenNodes);
    biasOutput.resize(outputNodes);
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

vector<double> NeuralNetwork::feedForward(const vector<double>& inputs) {
    vector<double> hidden(hiddenNodes);
    vector<double> outputs(outputNodes);
    feedForwardDetailed(inputs, hidden, outputs);
    return outputs;
}

void NeuralNetwork::loadModel(const string& filename) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) throw runtime_error("Cannot open model file: " + filename);

    int in, hid, out;
    double lr;
    file.read((char*)&in, sizeof(in));
    file.read((char*)&hid, sizeof(hid));
    file.read((char*)&out, sizeof(out));
    file.read((char*)&lr, sizeof(lr));

    if (in != inputNodes || hid != hiddenNodes || out != outputNodes)
        throw runtime_error("Model structure does not match current network");

    for (auto& row : weightsInputHidden)
        file.read((char*)row.data(), row.size() * sizeof(double));
    for (auto& row : weightsHiddenOutput)
        file.read((char*)row.data(), row.size() * sizeof(double));

    file.read((char*)biasHidden.data(), biasHidden.size() * sizeof(double));
    file.read((char*)biasOutput.data(), biasOutput.size() * sizeof(double));

    file.close();
    cout << "Model loaded from " << filename << endl;
}