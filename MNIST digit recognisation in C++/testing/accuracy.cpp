#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <stdexcept>
#include <iomanip>
#include <algorithm>
#include "neuralnetwork.h"

using namespace std;

static int reverseInt(int i) {
    unsigned char c1, c2, c3, c4;
    c1 = i & 255;
    c2 = (i >> 8) & 255;
    c3 = (i >> 16) & 255;
    c4 = (i >> 24) & 255;
    return ((int)c1 << 24) + ((int)c2 << 16) + ((int)c3 << 8) + c4;
}

vector<vector<double>> loadImages(string filename, int num_images) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        throw runtime_error("Error: Cannot open image file " + filename);
    }

    int magic_number = 0;
    int number_of_images = 0;
    int n_rows = 0;
    int n_cols = 0;

    file.read((char*)&magic_number, sizeof(magic_number));
    magic_number = reverseInt(magic_number);
    if (magic_number != 2051) {
        throw runtime_error("Error: Invalid magic number in image file " + filename);
    }

    file.read((char*)&number_of_images, sizeof(number_of_images));
    number_of_images = reverseInt(number_of_images);
    
    int num_to_load = min(number_of_images, num_images);

    file.read((char*)&n_rows, sizeof(n_rows));
    n_rows = reverseInt(n_rows);
    file.read((char*)&n_cols, sizeof(n_cols));
    n_cols = reverseInt(n_cols);

    int image_size = n_rows * n_cols;
    vector<vector<double>> dataset(num_to_load, vector<double>(image_size));
    
    for (int i = 0; i < num_to_load; ++i) {
        for (int j = 0; j < image_size; ++j) {
            unsigned char pixel = 0;
            file.read((char*)&pixel, sizeof(pixel));
            dataset[i][j] = (double)pixel / 255.0;
        }
    }

    file.close();
    cout << "Loaded " << num_to_load << " images from " << filename << endl;
    return dataset;
}

vector<int> loadLabels(string filename, int num_labels) {
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        throw runtime_error("Error: Cannot open label file " + filename);
    }

    int magic_number = 0;
    int number_of_labels = 0;

    file.read((char*)&magic_number, sizeof(magic_number));
    magic_number = reverseInt(magic_number);
    if (magic_number != 2049) {
        throw runtime_error("Error: Invalid magic number in label file " + filename);
    }

    file.read((char*)&number_of_labels, sizeof(number_of_labels));
    number_of_labels = reverseInt(number_of_labels);

    int num_to_load = min(number_of_labels, num_labels);

    vector<int> dataset(num_to_load);
    for (int i = 0; i < num_to_load; ++i) {
        unsigned char label = 0;
        file.read((char*)&label, sizeof(label));
        dataset[i] = (int)label;
    }

    file.close();
    cout << "Loaded " << num_to_load << " labels from " << filename << endl;
    return dataset;
}

int main() {
    string testImagesPath  = "../data/t10k-images.idx3-ubyte";
    string testLabelsPath  = "../data/t10k-labels.idx1-ubyte";
    string modelPath       = "../mnist_model.dat";

    NeuralNetwork nn(784, 128, 10, 0.1);

    try {
        cout << "Starting Accuracy Test Mode..." << endl;
        nn.loadModel(modelPath);

        cout << "Testing accuracy on 10,000 images..." << endl;
        auto test_images = loadImages(testImagesPath, 10);
        auto test_labels = loadLabels(testLabelsPath, 10);

        double correctCount = 0;
        for (int i = 0; i < test_images.size(); i++) {
            vector<double> out = nn.feedForward(test_images[i]);
            int predicted = max_element(out.begin(), out.end()) - out.begin();
            if (predicted == test_labels[i]) {
                correctCount++;
            }
        }
        double accuracy = (correctCount / test_images.size()) * 100.0;
        cout << "--- Test Complete ---" << endl;
        cout << "Correct Predictions: " << correctCount << "/" << test_images.size() << endl;
        cout << "Accuracy: " << fixed << setprecision(2) << accuracy << "%" << endl;
    }
    catch (const exception& e) {
        cerr << "An error occurred: " << e.what() << endl;
        return 1;
    }

    return 0;
}