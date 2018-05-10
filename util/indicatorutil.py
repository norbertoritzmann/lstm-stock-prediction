from indicators_reader import IndicatorExtractor
from enum import Enum
import pandas as pd
from dateutil import parser

import util.targettransformer as tf


class IndicatorEnum(Enum):
    ADX = "ADX"
    CCI = "CCI"
    MINUS_DI = "MINUS_DI"
    PLUS_DI = "PLUS_DI"
    STOCH_K = "STOCH_K"
    WMA = "WMA"
    PSY = "PSY"

class IndicatorRepository(object):

    def __init__(self, stock_name, directory_base="/database/sized/", target_transformer=tf.WILL_RISE):
        extractor = IndicatorExtractor()
        self.database = extractor.extract_indicators(stock_name, directory_base, target_transformer)
        
        #for df in self.database:
         #   pd.to_datetime(self.database[df]['Date'])

    def getvalue(self, date, size, indicator=IndicatorEnum.ADX):
        df = self.database[indicator.value]
        return df[df['Date'] == date]['wsize_' + str(size)]

    def getbyrange(self, start_date, end_date, size=None, indicator=IndicatorEnum.ADX):
        return self.getbyrange_column(start_date, end_date, size, indicator.value)

    def getbyrange_column(self, start_date, end_date, size=None, column='willRise'):
        df = self.database[column]

        return df[start_date:end_date]