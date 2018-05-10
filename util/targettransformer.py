import abc
import util.timeseries as tm


class TargetTransformer(object):
    __metaclass__ = abc.ABCMeta


    @abc.abstractmethod
    def transform(self, input):
        return


class CloseTargetTransformer(TargetTransformer):

    def transform(self, input):
        return tm.extract_and_append_next_day_close(input)


class DiscreteWillRiseTargetTransformer(TargetTransformer):

    def transform(self, input):
        return tm.extract_and_append_next_day_will_rise(input)


CLOSE = CloseTargetTransformer()
WILL_RISE = DiscreteWillRiseTargetTransformer()
