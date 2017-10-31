import unittest

import pandas

from util import timeseries


class MyTestCase(unittest.TestCase):

    def extract_next_day_will_rise(self):
        df = pandas.read_csv("ADX.csv", engine='python', parse_dates=['Date'])
        df = timeseries.extract_and_append_next_day_will_rise(df)

        print(df['willRise'])
        #self.assertEqual(df['willRise'][0], 0)


if __name__ == '__main__':
    unittest.main()
