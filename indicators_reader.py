import os
from os import listdir
from os.path import isfile, join

import pandas

from statistic import normalization
from util import timeseries as ts


class IndicatorExtractor(object):

    def extract_indicators(self, stock, directory_base = "/database/sized/"):
        """
        :type stock: stock code name (example: msft)
        :type directory_base: path to root stocks data
        """
        print("Extracting on: " + os.getcwd() + directory_base + stock)
        train_file_path = os.getcwd() + directory_base + stock

        onlyfiles = [f for f in listdir(train_file_path) if isfile(join(train_file_path, f))]

        database = {}
        indexes = None
        willRise = None
        closes = None
        for f in onlyfiles:
            print(f.replace(".csv", ""))
            pandas_dataframe = pandas.read_csv(join(train_file_path, f), engine='python', parse_dates=['Date'])

            # Remove as primeiras 15 linhas
            pandas_dataframe = pandas_dataframe.iloc[15:]

            # Remove a coluna Date e deixa como indexação
            dates = pandas_dataframe.pop('Date')
            pandas_dataframe.index = dates

            # 50% balanced sampling
            if indexes is None:
                pandas_dataframe = ts.extract_and_append_next_day_will_rise(pandas_dataframe)
                pandas_dataframe = pandas_dataframe.sample(frac=0.25, replace=False)
                pandas_dataframe.sort_index(inplace=True)
                indexes = pandas_dataframe.index
                closes = pandas_dataframe['Close']
            else:
                pandas_dataframe = pandas_dataframe.loc[indexes]

            mean_values = pandas_dataframe.median(axis=0)
            pandas_dataframe = pandas_dataframe.fillna(method='ffill')
            pandas_dataframe = pandas_dataframe.fillna(mean_values)
            # Remove Close para realizar a normalização dos atributos
            pandas_dataframe.pop('Close')

            pd_normalized = normalization.standardization(pandas_dataframe)

            database[f.replace(".csv", "")] = pd_normalized

        pandas_dataframe = pandas.read_csv(join(train_file_path, onlyfiles[0]), engine='python', parse_dates=['Date'])

        database['willRise'] = ts.extract_and_append_next_day_will_rise(pandas_dataframe)
        database['willRise'].index = database['willRise'].pop('Date')
        database['Close'] = closes

        return database
