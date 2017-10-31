import numpy

import pandas as pd


class Validation(object):

    def __init__(self, model):
        self.model = model

    def predict_point_by_point(self, data):
        # Predict each timestep given the last sequence of true data, in effect only predicting 1 step ahead each time
        predicted = self.model.predict(data)
        predicted = numpy.reshape(predicted, (predicted.size,))
        return predicted

    def mesure_accuracy(self, predicted, testY):
        correct = 0
        for p, y in zip(predicted, testY):
            if p >= 0.5 and y == 1:
                correct = correct + 1
            elif p < 0.5 and y == 0:
                correct = correct + 1

        accuracy = correct / len(testY)

        return accuracy

    # evaluate loaded model on test data
    def validation(self, X, Y):
        #self.model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        score = self.model.evaluate(X, Y, verbose=0)
        print("%s: %.2f%%" % (self.model.metrics_names[1], score[1] * 100))

    def save_holdout_prediction(self, df_testX, df_testY, stock_name, train_colums):
        # reshape input to be [samples, time steps, features] or (batch_size, sequence_length, input_dimension)
        testX = numpy.reshape(df_testX[train_colums].values, (df_testX[train_colums].values.shape[0], 1, df_testX[train_colums].values.shape[1]))
        testY = numpy.reshape(df_testY.values, (df_testY.values.shape[0], 1, df_testY.values.shape[1]))

        predicted = self.predict_point_by_point(testX)
        accuracy = self.mesure_accuracy(predicted, testY)
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

