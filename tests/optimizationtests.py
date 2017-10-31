import unittest
from genetic.optimization import Optimization
from dateutil import parser
from util.indicatorutil import IndicatorRepository

chromosome_all_inactive = [9, 0, 5, 0, 11, 0, 10, 0, 10, 0, 10, 0]
start_date, end_date = parser.parse("2005-10-20"), parser.parse("2005-10-25")
start_test_date, end_test_date = parser.parse("2005-10-20"), parser.parse("2005-10-25")

class MyTestCase(unittest.TestCase):
    def test_fitness_when_all_incative(self):
        repository = IndicatorRepository('msft', directory_base='/../database/sized/')
        opt = Optimization('msft', start_date, end_date, start_test_date, end_test_date, repository)
        value = opt.fitness(chromosome_all_inactive)
        self.assertEqual(value[0], 0.0)


if __name__ == '__main__':
    unittest.main()
