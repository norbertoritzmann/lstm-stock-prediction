from util.indicatorutil import IndicatorEnum
import logging as log
from pandas import DataFrame as df
from util.targettransformer import TargetTransformer

class Individual(object):

    def __init__(self, chromosome, repository, parameters):
        self.repository = repository
        self.parameters = parameters
        self.chromosome = chromosome
        self.indicators_active = {IndicatorEnum.ADX: chromosome[1] == 1,
                                  IndicatorEnum.CCI: chromosome[3] == 1,
                                  IndicatorEnum.MINUS_DI: chromosome[5] == 1,
                                  IndicatorEnum.PLUS_DI: chromosome[7] == 1,
                                  IndicatorEnum.STOCH_K: chromosome[9] == 1,
                                  IndicatorEnum.WMA: chromosome[11] == 1,
                                  IndicatorEnum.PSY: chromosome[13] == 1}

        if all(active == 0 for active in self.indicators_active.values()):
            raise TypeError("all args are")

        self.indicators_wsize = {IndicatorEnum.ADX: chromosome[0],
                                 IndicatorEnum.CCI: chromosome[2],
                                 IndicatorEnum.MINUS_DI: chromosome[4],
                                 IndicatorEnum.PLUS_DI: chromosome[6],
                                 IndicatorEnum.STOCH_K: chromosome[8],
                                 IndicatorEnum.WMA: chromosome[10],
                                 IndicatorEnum.PSY: chromosome[12]}

    def get_indicator_datasets(self, indicator_time_length, indicator):
        trainDataset = self.repository.getbyrange(start_date=self.parameters.start_date, end_date=self.parameters.end_date, size=indicator_time_length, indicator=indicator)
        testDataset = self.repository.getbyrange(start_date=self.parameters.start_test_date, end_date=self.parameters.end_test_date, size=indicator_time_length, indicator=indicator)

        will_rise_train = self.repository.getbyrange_column(start_date=self.parameters.start_date, end_date=self.parameters.end_date, column='willRise')
        will_rise_test = self.repository.getbyrange_column(start_date=self.parameters.start_test_date, end_date=self.parameters.end_test_date, column='willRise')

        trainDataset['willRise'] = will_rise_train.loc[:,'willRise']
        testDataset['willRise'] = will_rise_test.loc[:,'willRise']

        return trainDataset, testDataset

    def generate_dataset(self):
        train = df()
        test = df()

        for indicator in IndicatorEnum:
            if self.indicators_active[indicator]:
                train_indicator, test_indicator = self.get_indicator_datasets(self.indicators_wsize[indicator], indicator)
                if 'willRise' not in train.columns:
                    train['willRise'] = train_indicator['willRise']
                    test['willRise'] = test_indicator['willRise']
                train[indicator.value] = train_indicator['wsize_' + str(self.indicators_wsize[indicator])]
                test[indicator.value] = test_indicator['wsize_' + str(self.indicators_wsize[indicator])]

        return train, test

    def __str__(self):
        str_result = ""

        for indicator in IndicatorEnum:
            if self.indicators_active[indicator]:
                str_result = str_result + ", " + indicator.value + ':: ' + str(self.indicators_wsize[indicator])

        return str_result