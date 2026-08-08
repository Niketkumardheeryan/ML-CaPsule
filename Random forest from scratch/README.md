## 🥦 RANDOM FOREST TEST 🥦
-------------------------------------------------------------------------
### Introduction 
--------------------------------------------------------------------------
Random forest is a popular machine learning algorithm that belongs to the supervised learning technique.

It can be used for both classification and regression and is based on the concept of ensemble learning i.e. a process of

combining multiple classifiers to solve a complex problem and to improve the performance of the model.

Random forest makes use of the bagging technique.

✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨

### How Random Forest test algorithm do that job 🌿🌿 ?
In random forest, the models M1, M2...etc. are nothing but decision trees.
There are two phases namely 🌴:
  🍂. Creating the random forest by combining N decision trees
  🍂. Making predictions for each tree

✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨

#### what is the main steps that this forest test will follow :
🍃. Starts by selecting random samples from given dataset using the bootstrap technique.

🍃. This algorithm will construct a decision tree for every sample, then it will get prediction result from each decision tree.

🍃. Next, voting will be performed for every predicted result.

🍃. At last, select the most voted prediction as the final prediction result.

✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨
### ponits to be noted 
-  🌸 For a Random Forest Classifier :
 
 the final result will be the majority vote.
 
-  🌸 For a Random Forest Regressor :
 
 the final result will be mean of results of all the decision trees.

✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨✨

### Files 📁

| File | Contents |
|------|----------|
| `random_forest.py` | `Node`, `DecisionTree` and `RandomForest`, written from scratch with NumPy |
| `train_random_forest.py` | Trains the forest on the sklearn breast cancer dataset and prints test accuracy |

### Run it ▶️

```bash
pip install numpy scikit-learn
cd "Random forest from scratch"
python train_random_forest.py
```

```text
Accuracy: 0.9385964912280702
```

3 trees, `max_depth=10`, 80/20 split. Bootstrap sampling and feature selection are not
seeded, so accuracy moves around roughly 92-94% between runs.

