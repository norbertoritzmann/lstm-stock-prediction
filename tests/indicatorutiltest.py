from util.indicatorutil import IndicatorRepository, IndicatorEnum
from dateutil import parser
import unittest


class IndicatorUtilTest(unittest.TestCase):

    def get_value(self):
        repository = IndicatorRepository("msft", directory_base = "/../database/sized/")
        print(repository.getvalue(parser.parse("2005-10-24"), 9, indicator=IndicatorEnum.WMA))

    def get_by_range(self, size=None):
        repository = IndicatorRepository("msft", directory_base = "/../database/sized/")
        range = repository.getbyrange(parser.parse("2005-10-20"), parser.parse("2005-10-25"), size,
                              indicator=IndicatorEnum.WMA)
        print(range)

    def test_all(self):
        self.get_value()
        self.get_by_range()
        self.get_by_range(9)

if __name__ == '__main__':
    unittest.main()
