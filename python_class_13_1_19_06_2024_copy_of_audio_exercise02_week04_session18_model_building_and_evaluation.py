# -*- coding: utf-8 -*-
"""Python Class 13.1 - 19/06/2024 Copy of Audio_Exercise02_Week04_session18_Model_Building_and Evaluation.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19ctUlogY-ag-9SVhp2z_q1W3yRoS2pjy
"""

from google.colab import drive
drive.mount('/content/drive')

"""### Load the CSV files

- Please uploadn the created the train and test CSV files to the colab environment.
"""

# define the paths
TRAIN_CSV = "/content/drive/MyDrive/AIClub_AP_Pentela_Lakshmi_Rishi/Datasets/music_instrument_features_train.csv"
TEST_CSV = "/content/drive/MyDrive/AIClub_AP_Pentela_Lakshmi_Rishi/Datasets/music_instrument_features_test.csv"

import pandas as pd

# load the train csv
data_train = pd.read_csv(TRAIN_CSV)
data_train.head()

"""### Encoding Labels"""

# labels are there as string otherwise words
# need to convert the labels into numbers
print(data_train["LABEL"].value_counts())
LABELS = list(data_train["LABEL"].unique())
# sort the labels
LABELS.sort()
print(LABELS)

"""### Encoding Structure
- We are encoding the labels in alphabetical order.
- electric_guitar gets 0 while piano gets 1.
"""

# convert into numbers
data_train["LABEL"] = pd.factorize(data_train["LABEL"], sort = True)[0]
data_train["LABEL"].value_counts()

"""### Seperate features and labels
- Label is at the last index which we can reference by -1
"""

# get all features without the labels
# all the rows
# all the columns without the last column
X = data_train.iloc[:, :-1].values
# all rows
# only the lastb column, which is the label
Y = data_train.iloc[:, -1].values

"""### Train the Model using Cross Validation"""

from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score
import numpy as np

def cross_validation(model, data = (X, Y), splits = 11):
    kf = KFold(n_splits=splits, shuffle=True, random_state=42)

    # Perform k-fold cross-validation
    accuracy = []
    precision = []
    recall = []

    for train_index, valid_index in kf.split(data[0]):
        X_train, X_valid = data[0][train_index], data[0][valid_index]
        y_train, y_valid = data[1][train_index], data[1][valid_index]

        # Fit the defined model
        model.fit(X_train, y_train)

        # Make predictions on the test data
        y_pred = model.predict(X_valid)

        # Calculate accuracy, precision and recall
        accuracy.append(accuracy_score(y_pred, y_valid))
        precision.append(precision_score(y_pred, y_valid))
        recall.append(recall_score(y_pred, y_valid))


    # get arrays
    accuracy_set = np.array(accuracy)
    precision_set = np.array(precision)
    recall_set = np.array(recall)

    print("Mean Accuracy: {}".format(accuracy_set.mean()))
    print("Mean Precision: {}".format(precision_set.mean()))
    print("Mean Recall: {}".format(recall_set.mean()))

"""### Logistic Regression"""

from sklearn.linear_model import LogisticRegression

# fit the logistic regression
lr = LogisticRegression()

cross_validation(lr)

"""### KNN"""

from sklearn.neighbors import KNeighborsClassifier

# Use 5-fold cross validation for hyper-parameter tuning
# Try out different values and choose the best hyper-parameters
knn = KNeighborsClassifier(n_neighbors=10)

cross_validation(knn)

"""### Random Forest"""

from sklearn.ensemble import RandomForestClassifier

# Use 5-fold cross validation for hyper-parameter tuning
# Try out different values and choose the best hyper-parameters
rf = RandomForestClassifier()

cross_validation(rf)

"""### Fit the best model

- Select the best model having the highest cross validation accuracy
"""

# Model with the lowest RMSE or highest r2
best_model = RandomForestClassifier()

# Fit the model on the full training dataset
best_model.fit(X, Y)

"""### Load the test data"""

# load the test data
data_test = pd.read_csv(TEST_CSV)
data_test.head()

"""### Encode the test data as well"""

# encode the labels
data_test["LABEL"] = pd.factorize(data_test["LABEL"], sort = True)[0]
data_test["LABEL"].value_counts()

"""### Seperate features and labels"""

# all the rows
# all the columns without the last column
x_test = data_test.iloc[:, : -1]
# all rows
# only the lastb column, which is the label
y_test = data_test.iloc[:, -1]

"""### Use the best model to make predictions"""

# make predictions
predictions = best_model.predict(x_test)
print(predictions)

"""### Evaluate the test data"""

#evaluation function

def model_evaluations(y_true, y_pred, labels):
  import matplotlib.pyplot as plt
  import seaborn as sns
  from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

  acc_score = accuracy_score(y_true, y_pred)
  print("Accuracy score: {}\n".format(acc_score))

  print("Classification Report: {}".format(classification_report(y_true, y_pred)))

  plt.figure(figsize = (5, 5))
  sns.heatmap(confusion_matrix(y_true, y_pred),  annot = True, fmt="g", cmap = "Blues", xticklabels = labels, yticklabels = labels)
  plt.title("Consfuion Matrix")
  plt.show()

# run the evaluation functions
model_evaluations(y_test, predictions, LABELS)

"""### Save the best model

- Make sure to donwload the model when you are planning to use the model later.
"""

import pickle

fh = open("/content/drive/MyDrive/AIClub_AP_Pentela_Lakshmi_Rishi/Datasets/music_instruments_best_model", "wb")
pickle.dump(best_model, fh)
fh.close()