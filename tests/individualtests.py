import unittest
from genetic.individual import Individual
from util.indicatorutil import IndicatorEnum, IndicatorRepository
from dateutil import parser

chromosome = [9, 1, 5, 0, 11, 1, 10, 1, 10, 0, 10, 1, 12, 1]
start_date, end_date = parser.parse("2005-10-20"), parser.parse("2005-10-25")
start_test_date, end_test_date = parser.parse("2005-10-20"), parser.parse("2005-10-25")
class MyTestCase(unittest.TestCase):

    def test_dataset_generation(self):
        repository = IndicatorRepository("msft", directory_base="/../database/sized/")

        self.start_date = start_date
        self.end_date = end_date
        self.start_test_date = start_test_date
        self.end_test_date = end_test_date
        ind = Individual(chromosome, repository, self)
        train, test = ind.get_indicator_datasets(ind.indicators_wsize[IndicatorEnum.ADX], IndicatorEnum.ADX)
        self.assertEqual(True, train is not None)
        self.assertEqual(True, test is not None)
        self.assertEqual(True, train["willRise"] is not None)
        self.assertEqual(True, train["wsize_9"] is not None)
        train, test = ind.generate_dataset()
        self.assertEqual(True, "ADX" in train.columns)
        self.assertEqual(True, "willRise" in train.columns)

if __name__ == '__main__':
    unittest.main()
