import logging as log

import numpy

numpy.random.seed(640)
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from keras import backend as K
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import time
import pandas
from model_validation import Validation
from util import timeseries


class LSTMModelHandler:
    def __init__(self, trainX, trainY, testX, testY, pipeline_transform=None):
        self.trainX, self.trainY = trainX, trainY
        self.testX, self.testY = testX, testY
        self.model = Sequential()
        self.input_layer_size = self.trainX.shape[2]
        self.output_layer_size = self.trainY.shape[1]
        self.validation = Validation(self.model)
        self.best_result = {'result': 0.0, 'architecture': {}}

        if pipeline_transform is not None:
            pipeline_transform.fit_transform(self.trainX)
            pipeline_transform.fit_transform(self.testX)

    @classmethod
    def init_from_pandas_df(cls, pandas_dataframe, pandas_dataframe_test, train_columns=None, target_columns='willRise',
                            pipeline_transform=None):
        trainX, trainY = timeseries.extract_keras_format_data(pandas_dataframe, train_columns, target_columns)
        testX, testY = timeseries.extract_keras_format_data(pandas_dataframe_test, train_columns, target_columns)
        return cls(trainX, trainY, testX, testY)

    @classmethod
    def init_from_file(cls, train_file_path, test_file_path, train_columns, target_columns, usecols=(2, 3, 4, 5, 6, 7)):
        pandas_dataframe = pandas.read_csv(train_file_path, usecols=usecols, engine='python')
        pandas_dataframe_test = pandas.read_csv(test_file_path, usecols=usecols, engine='python')
        return cls.init_from_pandas_df(pandas_dataframe, pandas_dataframe_test, train_columns, target_columns)

    def build_optimized_hyper_lstm_two_hidden(self, hiden_layers=(200, 100), activation='sigmoid', dropout_rate_1=0.25,
                                              dropout_rate_2=0.45, optimizer='RMSprop', loss='mse',
                                              metrics=['accuracy']):
        try:
            self.model.add(LSTM(
                input_dim=self.input_layer_size,
                units=hiden_layers[0],
                return_sequences=True))
            self.model.add(Dropout(dropout_rate_1))

            self.model.add(LSTM(
                units=hiden_layers[1],
                return_sequences=False))
            self.model.add(Dropout(dropout_rate_2))

            self.model.add(Dense(units=self.output_layer_size))
            self.model.add(Activation(activation))  # sigmoid

            start = time.time()
            self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)  # binary_crossentropy

        except TypeError as e:
            raise e

        return self.model

    def build_lstm_two_hidden(self, hiden_layers=(100, 150), activation='sigmoid', dropout_rate_1=0.25,
                              dropout_rate_2=0.45, optimizer='RMSprop', loss='mse', metrics=['accuracy']):
        try:
            self.model.add(LSTM(
                input_dim=self.input_layer_size,
                units=hiden_layers[0],
                return_sequences=True))
            self.model.add(Dropout(dropout_rate_1))

            self.model.add(LSTM(
                units=hiden_layers[1],
                return_sequences=False))
            self.model.add(Dropout(dropout_rate_2))

            self.model.add(Dense(units=self.output_layer_size))
            self.model.add(Activation(activation))  # sigmoid

            start = time.time()
            self.model.compile(loss=loss, optimizer=optimizer, metrics=metrics)  # binary_crossentropy

        except TypeError as e:
            print(e)
            raise e

        return self.model

    def build_and_train_lstm_hyperparameter_opt_two_hidden(self):
        start = time.time()

        try:
            num_units_lstm = [80, 100, 150, 200, 300, 400, 500]
            dropout_rate = [0.25, 0.45, 0.55]
            activations = ['sigmoid', 'relu']
            optimizations = ['adam', 'rmsprop']
            epoch_sizes = [80, 90, 100, 110]

            space = {
                    'choice': hp.choice('num_layers',
                                         [{'layers': 'two', },
                                          {'layers': 'three',
                                           'units3': hp.choice('units3', num_units_lstm),
                                           'dropout3': hp.choice('dropout3', dropout_rate)}
                                          ]),

                     'units1': hp.choice('units1', num_units_lstm),
                     'units2': hp.choice('units2', num_units_lstm),
                     'dropout1': hp.choice('dropout1', dropout_rate),
                     'dropout2': hp.choice('dropout2', dropout_rate),
                     'nb_epochs': hp.choice('nb_epochs', epoch_sizes),
                     'optimizer': hp.choice('optimizer', optimizations),
                     'activation': hp.choice('activation', activations)
                     }

            trials = Trials()
            best = fmin(self.hyper_optimization, space, algo=tpe.suggest, max_evals=50, trials=trials)
            print("Best")
            print(best)
            log.info(":BEST:")
            log.info(best)


            print("Compilation Time %n ", ((time.time() - start) * 6))

        except TypeError as e:
            print(e)
            raise e

        return self.model

    def train(self, epoch=100, validation_split=0.3, validation_data=None):
        self.model.fit(
            self.trainX,
            self.trainY,
            batch_size=self.trainX.shape[0],
            validation_data=validation_data,
            nb_epoch=epoch
            #    , callbacks=[tensorCallback]
        )

    def test_measurements(self):
        predicted = self.validation.predict_point_by_point(self.testX)

        return self.validation.mesure_accuracy(predicted, self.testY)

    def hyper_optimization(self, params):
        K.clear_session()
        loss = 'mse'
        metrics = ['accuracy']

        print(str((self.trainX.shape[1], self.trainX.shape[2])))
        self.model = Sequential()
        self.validation = Validation(self.model)

        self.model.add(LSTM(
            input_shape=(self.trainX.shape[1], self.trainX.shape[2]),
            units=params['units1'],
            return_sequences=True))
        self.model.add(Dropout(params['dropout1']))

        self.model.add(LSTM(
            units=params['units2'],
            return_sequences=params['choice']['layers'] == 'three'))
        self.model.add(Dropout(params['dropout2']))

        if params['choice']['layers'] == 'three':
            print("Three layers!")
            self.model.add(LSTM(
                units=params['choice']['units3'],
                return_sequences=False))
            self.model.add(Dropout(params['choice']['dropout3']))

        self.model.add(Dense(units=self.output_layer_size))
        self.model.add(Activation(params['activation']))

        self.model.compile(loss=loss, optimizer=params['optimizer'], metrics=metrics)  # binary_crossentropy

        self.train(validation_data=(self.testX, self.testY), epoch=params['nb_epochs'])
        acc = self.test_measurements()

        if acc > self.best_result['result']:
            print("There is a new best result for: " + str(params))
            print(str(acc))
            self.best_result = {'result': acc, 'architecture': params}


        loss = 1.0 - acc
        return {'loss': loss, 'status': STATUS_OK}