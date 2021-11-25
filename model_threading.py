from concurrent.futures import ThreadPoolExecutor
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import learning_curve
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error
import tensorflow as tf

class Model:
    def __init__(self, model=None):
        self.model = model

    def model_train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        print("Model Cross Val:", np.mean(cross_val_score(self.model,X_train,y_train, scoring = 'neg_mean_absolute_error', cv= 3)))
    
    def model_predict(self, X_test, y_test):
        model_predict = self.model.predict(X_test)
        print("Prediction MAE", mean_absolute_error(y_test, model_predict))
    
    def plot_loss_curve(self, X_train, y_train, train_sizes=[500, 1500, 3000], cv=3):
        train_sizes, train_scores, validation_scores = learning_curve(self.model, X_train, y_train, train_sizes = train_sizes,
                                                                    cv = cv, scoring = 'neg_mean_squared_error')
        train_scores_mean = train_scores.mean(axis=1)
        validation_scores_mean = validation_scores.mean(axis=1)
        
        plt.plot(train_sizes, train_scores_mean ,'g', label='Training Score')
        plt.plot(train_sizes, validation_scores_mean , 'b', label='Validation Score')
        plt.title('Training and Validation Score')
        plt.xlabel('Training Size')
        plt.ylabel('Score')
        plt.legend()
        plt.show()


