import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.optimizers import gradient_descent_v2
from keras.layers import Dense, BatchNormalization, Activation, Dropout
from keras.callbacks import EarlyStopping, Callback
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from keras.models import load_model
from IPython.display import clear_output

user_object = dict()

user_object["fake"] = pd.read_csv("Dataset/fake_twitter_accounts.csv")
user_object["legit"] = pd.read_csv("Dataset/real_twitter_accounts.csv")

user_object["legit"] = user_object["legit"].drop(
    ["id", "name", "screen_name", "created_at", "lang", "location", "default_profile", "default_profile_image",
     "geo_enabled", "profile_image_url", "profile_banner_url", "profile_use_background_image",
     "profile_background_image_url_https", "profile_text_color", "profile_image_url_https",
     "profile_sidebar_border_color", "profile_background_tile", "profile_sidebar_fill_color",
     "profile_background_image_url", "profile_background_color", "profile_link_color", "utc_offset", "protected",
     "verified", "dataset", "updated", "description","url","time_zone"], axis=1)

user_object["fake"] = user_object["fake"].drop(
    ["id", "name", "screen_name", "created_at", "lang", "location", "default_profile", "default_profile_image",
     "geo_enabled", "profile_image_url", "profile_banner_url", "profile_use_background_image",
     "profile_background_image_url_https", "profile_text_color", "profile_image_url_https",
     "profile_sidebar_border_color", "profile_background_tile", "profile_sidebar_fill_color",
     "profile_background_image_url", "profile_background_color", "profile_link_color", "utc_offset", "protected",
     "verified", "dataset", "updated", "description","url","time_zone"], axis=1)

user_object["legit"] = user_object["legit"].values
user_object["fake"] = user_object["fake"].values

for index in range(len(user_object["legit"])):
    if type(user_object["legit"][index][5]) == str:
        user_object["legit"][index][5] = 1

    if type(user_object["legit"][index][6]) == str:
        user_object["legit"][index][6] = 1

for index in range(len(user_object["fake"])):
    if type(user_object["fake"][index][5]) == str:
        user_object["fake"][index][5] = 1

    if type(user_object["fake"][index][6]) == str:
        user_object["fake"][index][6] = 1

user_object["legit"] = user_object["legit"].astype(np.float64)
user_object["fake"] = user_object["fake"].astype(np.float64)

where_nans = np.isnan(user_object["legit"])
user_object["legit"][where_nans] = 0

where_nans = np.isnan(user_object["fake"])
user_object["fake"][where_nans] = 0

X = np.zeros((len(user_object["fake"]) + len(user_object["legit"]), 7))
Y = np.zeros(len(user_object["fake"]) + len(user_object["legit"]))

for index in range(len(user_object["legit"])):
    X[index] = user_object["legit"][index] / max(user_object["legit"][index])
    Y[index] = -1

for index in range(len(user_object["fake"])):
    bound = max(user_object["fake"][index])
    if bound == 0:
        bound = 1

    X[len(user_object["legit"]) + index] = user_object["fake"][index] / bound  # Normalizing Data [0 <--> 1]
    Y[len(user_object["legit"]) + index] = 1

X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(X, Y,
                                                                        test_size=0.24, random_state=42)

early_stopping = EarlyStopping(monitor='val_loss', patience=2)


class PlotLearning(Callback):
    def on_train_begin(self, logs={}):
        self.i = 0
        self.x = []
        self.losses = []
        self.val_losses = []
        self.acc = []
        self.val_acc = []
        self.fig = plt.figure()

        self.logs = []

    def on_epoch_end(self, epoch, logs={}):
        self.logs.append(logs)
        self.x.append(self.i)
        self.losses.append(logs.get('loss'))
        self.val_losses.append(logs.get('val_loss'))
        self.acc.append(logs.get('acc'))
        self.val_acc.append(logs.get('val_acc'))
        self.i += 1
        f, (ax1, ax2) = plt.subplots(1, 2, sharex=True)

        clear_output(wait=True)

        ax1.set_yscale('Log')
        ax1.plot(self.x, self.losses, label="loss")
        ax1.plot(self.x, self.val_losses, label="val_loss")
        ax1.legend()

        ax2.plot(self.x, self.acc, label="accuracy")
        ax2.plot(self.x, self.val_acc, label="validation accuracy")
        ax2.legend()

        plt.show();


plot = PlotLearning()

model = Sequential([
    BatchNormalization(),

    Dense(16, activation="relu", kernel_regularizer="l2"),
    BatchNormalization(),
    Dense(8, activation="relu", kernel_regularizer="l2"),
    BatchNormalization(),
    Dense(1, activation="tanh"),
])

model.build((None, X.shape[1]))
model.summary()
model.compile(
    optimizer="adadelta",
    loss="binary_crossentropy",
    metrics=["acc"]
)

model.fit(X_train_data, y_train_data, epochs=2000, validation_data=(X_test_data, y_test_data), shuffle=True,
          batch_size=100,
          callbacks=[early_stopping, plot])

prediction = model.predict(X_test_data).T[0]

for index in range(len(prediction)):
    prediction[index] = -1 if prediction[index] < 0 else 1


def plot_confusion_matrix(cm, title='CONFUSION MATRIX', cmap=plt.cm.Reds):
    target_names = ['Fake', 'Real']
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


mat = confusion_matrix(y_test_data, prediction)
print(mat)

plot_confusion_matrix(mat)

_, train_accuracy = model.evaluate(X_train_data, y_train_data)
_, validation_accuracy = model.evaluate(X_test_data, y_test_data)
print("Train Accuracy:", train_accuracy)
print("Validation Accuracy:", validation_accuracy)

model.save('keras_model/model_twitter.hdf5')
frozen_model = load_model("keras_model/model_twitter.hdf5")
