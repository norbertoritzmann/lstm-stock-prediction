from dateutil import parser

import unittest

import logging as log

from genetic.individual import Individual
from model_handler import LSTMModelHandler
from util.indicatorutil import IndicatorRepository

chromosome = [9, 1, 5, 0, 11, 1, 10, 1, 10, 0, 10, 1]
start_date, end_date = parser.parse("2005-10-20"), parser.parse("2005-10-25")
start_test_date, end_test_date = parser.parse("2005-10-20"), parser.parse("2005-10-25")
class MyTestCase(unittest.TestCase):

    def generate_individual(self):
        self.start_date = start_date
        self.end_date = end_date
        self.start_test_date = start_test_date
        self.end_test_date = end_test_date

        repository = IndicatorRepository("msft", directory_base="/../database/sized/")
        return Individual(chromosome, repository, self)

    def test_something(self):
        individual = self.generate_individual()
        train, test = individual.generate_dataset()
        log.info("Train Data:")
        log.info(train.head(5))
        lstm_model_handler1 = LSTMModelHandler.init_from_pandas_df(pandas_dataframe=train, pandas_dataframe_test=test)
        lstm_model_handler1.build_lstm_two_hidden()
        result1 = lstm_model_handler1.test_measurements()

        lstm_model_handler2 = LSTMModelHandler.init_from_pandas_df(pandas_dataframe=train, pandas_dataframe_test=test)
        lstm_model_handler2.build_lstm_two_hidden()
        result2 = lstm_model_handler2.test_measurements()

        lstm_model_handler3 = LSTMModelHandler.init_from_pandas_df(pandas_dataframe=train, pandas_dataframe_test=test)
        lstm_model_handler3.build_lstm_two_hidden()
        result3 = lstm_model_handler3.test_measurements()

        lstm_model_handler4 = LSTMModelHandler.init_from_pandas_df(pandas_dataframe=train, pandas_dataframe_test=test)
        result4 = lstm_model_handler4.test_measurements()

        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertEqual(result3, result4)
        self.assertEqual(result4, result1)


if __name__ == '__main__':
    unittest.main()
