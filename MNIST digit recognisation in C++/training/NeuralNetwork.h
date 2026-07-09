#ifndef NEURALNETWORK_H
#define NEURALNETWORK_H

#include <vector>
#include <string>
using namespace std;

class NeuralNetwork {
private:
    int inputNodes;
    int hiddenNodes;
    int outputNodes;

    vector<vector<double>> weightsInputHidden;
    vector<vector<double>> weightsHiddenOutput;

    vector<double> biasHidden;
    vector<double> biasOutput;
    
    double learningRate;
    
    void feedForwardDetailed(const vector<double>& inputs, vector<double>& hidden, vector<double>& outputs);

public:
    NeuralNetwork(int inputNodes, int hiddenNodes, int outputNodes, double learningRate);
    void train(const vector<double>& inputs, const vector<double>& targets);
    void saveModel(const string& filename);
};

#endif