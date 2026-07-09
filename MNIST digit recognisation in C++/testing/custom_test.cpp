#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <stdexcept>
#include <iomanip>
#include <algorithm>
#include "neuralnetwork.h"

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

using namespace std;

vector<double> loadCustomImage(const string& filename) {
    int width, height, channels;
    unsigned char* data = stbi_load(filename.c_str(), &width, &height, &channels, 1);

    if (data == nullptr) {
        throw runtime_error("Error: Cannot load custom image " + filename);
    }
    if (width != 28 || height != 28) {
        stbi_image_free(data);
        throw runtime_error("Error: Image must be 28x28 pixels.");
    }

    vector<double> image_vector(784);
    
    bool is_inverted = ((double)data[0] / 255.0 > 0.5);
    if(is_inverted) {
        cout << "Detected white background. Inverting image..." << endl;
    } else {
        cout << "Detected black background. Loading image as is..." << endl;
    }

    for (int i = 0; i < 784; ++i) {
        double normalized_pixel = (double)data[i] / 255.0;
        image_vector[i] = is_inverted ? (1.0 - normalized_pixel) : normalized_pixel;
    }

    stbi_image_free(data);
    cout << "Loaded custom image: " << filename << endl;
    return image_vector;
}

int main() {
    string modelPath       = "../mnist_model.dat";
    string customImagePath = "../number_images/num8.png";

    NeuralNetwork nn(784, 128, 10, 0.1);

    try {
        cout << "Starting Custom Prediction Mode..." << endl;
        nn.loadModel(modelPath);
        
        vector<double> customImage = loadCustomImage(customImagePath);
        vector<double> out = nn.feedForward(customImage);
        int predicted = max_element(out.begin(), out.end()) - out.begin();

        cout << "\nConfidence Scores:" << endl;
        for(int i = 0; i < out.size(); ++i) {
            cout << "Digit " << i << ": " << fixed << setprecision(3) << out[i] * 100.0 << "%" << endl;
        }
        
        cout << "--- Prediction ---" << endl;
        cout << "The model predicts the digit is: " << predicted << endl << endl;
    }
    catch (const exception& e) {
        cerr << "An error occurred: " << e.what() << endl;
        return 1;
    }

    return 0;
}