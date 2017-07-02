import json
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
import numpy as np


# Class to store the collected multi-label sklearn classifier and interact with it more
# easily. Primary features:
# X load data from JSON files (X,y\n format)
# X fit the classifier from outside the class
# X predict with classifier externally
# - combine load, fit, and predict into one method

# Wrapper class for sklearn's multilabel classifier... includes pipeline integration
class mlc:

    # Constructor
    def __init__(self):
        # load from pickle if it exists
        self.mlb = MultiLabelBinarizer()                # need this for transformations throughout class
        self.cv = CountVectorizer()                     # part of pipeline (1)
        self.tfidf = TfidfTransformer()                 # part of pipeline (2)
        self.clf = OneVsRestClassifier(LinearSVC())     # part of pipeline (3)
        self.classifier = None                          # Finished classifier (initial None for testing purposes)
        self.labels = []                                # all labels, transformed, over time appended (y's)

    # Load from CSV file (at specified filepath). CSV Format: "X","y[,y1,y2,...]"\n
    # Returns list of pairs to be fit elsewhere. Output Format: [ "X" , "y" ]
    # Deprecated: use the JSON method instead.
    @staticmethod
    def load_from_csv(filepath):
        training_pairs = []
        with open(filepath) as f:
            for line in f.read().splitlines():
                spline = line.split(",")
                X = spline[0]
                y = spline[1]
                training_pairs.append([X, y])
        return training_pairs

    # Load from JSON file.
    # Example:
    # {
    #   "Example with labels": ["Music","Activism"],
    #   "Example without labels": []
    # }
    # Returns dictionary of X:y to be (partial) fit elsewhere. Output Format: dictionary
    @staticmethod
    def load_from_json(filepath):
        return json.loads(open(filepath).read())

    # Partial-fit from dictionary object argument. Uses code from SO since I don't know Pipelines very well yet.
    # Returns usable classifier object.
    def fit(self, dict):
        # Since we want to simulate a partial fit and Pipeline doesn't support it,
        # we'll separate out the steps and recreate this ourselves. It's a bit un-sleek,
        # but it still gets the job done.

        # First, grab the key-value pairs and separate into X and y
        x = [key for key in dict.keys()]
        y = [val for val in dict.values()]

        # Next, we need to create the pipeline for the x values and prepare y values
        self.classifier = Pipeline([
            ('vectorizer', self.cv),
            ('tfidf', self.tfidf),
            ('clf', self.clf)])
        y = self.mlb.fit_transform(y)

        # Train the model
        self.classifier.fit(x, y)

    # Predict with existing model using internally stored y's and given x test values.
    # Returns a list of y values (inverse-transformed) predicted from x_test values passed in.
    def predict(self, x_test):
        # First, predict values
        predicted = self.clf.predict(x_test)

        # Then inverse the labels
        all_labels = self.mlb.inverse_transform(predicted)

        # Then return these readable label guesses:
        return all_labels

    # Combines functionality of loading from JSON, fitting, and predicting for the model.
    # Takes in a JSON filepath to load from and a list of x test values.
    def load_fit_predict(self, json_filepath, x_test):
        self.fit(self.load_from_json(json_filepath))
        return self.classifier.predict(x_test)
