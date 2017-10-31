import indicators_reader as reader
import unittest


class MyTestCase(unittest.TestCase):

    def test_extraction(self):
        extractor = reader.IndicatorExtractor()
        database = extractor.extract_indicators("aapl", "/../database/sized/")
        assert database is not None

if __name__ == '__main__':
    unittest.main()