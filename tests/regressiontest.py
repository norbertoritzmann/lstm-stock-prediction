from dateutil import parser
from genetic.individual import Individual
from util.indicatorutil import IndicatorEnum, IndicatorRepository
from util import targettransformer as tf

class Parameters(object):
    pass


chromosome = [9, 1, 5, 0, 11, 1, 10, 1, 10, 0, 10, 1, 12, 1]
start_date, end_date = parser.parse("2005-10-20"), parser.parse("2006-10-25")
start_test_date, end_test_date = parser.parse("2006-10-26"), parser.parse("2007-10-26")

repository = IndicatorRepository("msft", directory_base="/../database/sized/", target_transformer=tf.CLOSE)

parameters = Parameters()
parameters.start_date = start_date
parameters.end_date = end_date
parameters.start_test_date = start_test_date
parameters.end_test_date = end_test_date
individual = Individual(chromosome, repository, parameters)

train, test = individual.generate_dataset()

print(train.head(15))
print(test.head(15))

from model_handler import LSTMModelHandler
best_result = 1.0
lstm_model_handler = LSTMModelHandler.init_from_pandas_df(pandas_dataframe=train, pandas_dataframe_test=test, best_result=best_result, is_regression=True)

# Build an optimezed hyper parameter LSTM model with two hidden layers
lstm_model_handler.build_and_train_lstm_hyperparameter_opt_two_hidden()


lstm_model_handler.best_result