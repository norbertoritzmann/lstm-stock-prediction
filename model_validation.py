import numpy

import pandas as pd
from keras import losses
import abc


class Validation(object):

    def __init__(self, model):
        self.model = model

    __metaclass__ = abc.ABCMeta

    def predict_point_by_point(self, data):
        # Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
        predicted = self.model.predict(data)
        predicted = numpy.reshape(predicted, (predicted.size,))
        return predicted

    @abc.abstractmethod
    def evaluate(self, predicted_y, true_y):
        return

    @abc.abstractmethod
    def is_result_better_than(self, result_y, older_best_y):
        return

    @staticmethod
    def get_instance(model, is_regression=False):
        if is_regression:
            return RegressionValidation(model)
        else:
            return ClassificationValidation(model)

    # evaluate loaded model on test data
    #def validation(self, X, Y):
        #self.model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        #score = self.model.evaluate(X, Y, verbose=0)
        #print("%s: %.2f%%" % (self.model.metrics_names[1], score[1] * 100))

    def save_holdout_prediction(self, df_testX, df_testY, stock_name, train_colums):
        # reshape input to be [samples, time steps, features] or (batch_size, sequence_length, input_dimension)
        testX = numpy.reshape(df_testX[train_colums].values, (df_testX[train_colums].values.shape[0], 1, df_testX[train_colums].values.shape[1]))
        testY = numpy.reshape(df_testY.values, (df_testY.values.shape[0], 1, df_testY.values.shape[1]))

        predicted = self.predict_point_by_point(testX)
        accuracy = self.evaluate(predicted, testY)
        print("Accuracy for " + stock_name + " is %f", accuracy)

        df_will_rise_prediction = pd.DataFrame({'willRisePred': predicted})
        X = df_testX[["Date", "Close"]]

        result = pd.concat([X, df_will_rise_prediction], axis=1)
        result.to_csv(stock_name + "_predctions.csv", sep=',', index=False)

    def load_holdout(stock_file_name, train_columns, target_columns='willRise'):
        dataframe = pd.read_csv(stock_file_name, engine='python')

        Y = dataframe[target_columns]
        X = dataframe[train_columns]
        full = dataframe

        return X, Y, full

class ClassificationValidation(Validation):

    def evaluate(self, predicted_y, true_y):
        return self.measure_accuracy(predicted_y, true_y)

    def is_result_better_than(self, result_y, older_best_y):
        return result_y > older_best_y

    def measure_accuracy(self, predicted, testY):
        correct = 0
        for p, y in zip(predicted, testY):
            if p >= 0.5 and y == 1:
                correct = correct + 1
            elif p < 0.5 and y == 0:
                correct = correct + 1

        accuracy = correct / len(testY)

        return accuracy


class RegressionValidation(Validation):

    def evaluate(self, predicted_y, true_y):
        return self.measure_mse(predicted_y, true_y)

    def is_result_better_than(self, result_y, older_best_y):
        return result_y < older_best_y

    def measure_mse(self, predicted, testY):
        mse = losses.mean_squared_error(testY, predicted)

        return mse

    def measure_mape(self, predicted, testY):
        mape = losses.mean_absolute_percentage_error(testY, predicted)

        return mape

    def measure_mae(self, predicted, testY):
        mae = losses.mean_absolute_error(testY, predicted)

        return mae
