import json
import numpy

from model_io import ModelIO

numpy.random.seed(640)
import array
import random
import logging
import time
from keras import backend as K
from keras.models import Sequential

from genetic.individual import Individual
from model_handler import LSTMModelHandler
from util.indicatorutil import IndicatorRepository
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from util import timeseries as ts, targettransformer as tf

logging.basicConfig(filename='lstm_sized.log', filemode='w', level=logging.DEBUG)

# create logger
log = logging.getLogger("Optimization")
log.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
log.addHandler(ch)




class BestIndividual(object):
    def __init__(self):
        self.result = 0.0
        self.chromosome = []
        self.architecture = {}

    def __str__(self):
        return "Result: " + str(self.result) + "\nChromosome: " + str(self.chromosome) + "\nArchitecture: " + str(self.architecture)

class Optimization(object):
    # Attributes ranges
    MIN_MAX = [
        (5, 10),
        (0, 1),
        (6, 10),
        (0, 1),
        (5, 10),
        (0, 1),
        (5, 10),
        (0, 1),
        (8, 13),
        (0, 1),
        (6, 11),
        (0, 1),
        (8, 15),
        (0, 1)
    ]
    ADX_MIN_MAX = (5, 10)
    CCI_MIN_MAX = (6, 10)
    MDI_MIN_MAX = (5, 10)
    PDI_MIN_MAX = (5, 10)
    STK_MIN_MAX = (8, 13)
    WMA_MIN_MAX = (6, 11)
    PSY_MIN_MAX = (7, 14)

    def __init__(self, stock_name, start_date, end_date, start_test_date, end_test_date,
                 best_individual, target_extractor=tf.WILL_RISE, repository=None):
        if repository == None:
            self.repository = IndicatorRepository(stock_name=stock_name, target_transformer=target_extractor)
        else:
            self.repository = repository
        self.start_date = start_date
        self.end_date = end_date
        self.start_test_date = start_test_date
        self.end_test_date = end_test_date
        self.cache = {}
        self.best_individual = best_individual
        self.best_model = Sequential()
        self.cycles = 0
        self.modelio = ModelIO()

    def fitness(self, chromosome):
        K.clear_session()
        time.sleep(20)
        try:
            individual = Individual(chromosome, repository=self.repository, parameters=self)

        except TypeError as e:
            print("%%%%%%%%%%")
            print(e)
            print("%%%%%%%%%%")
            log.error(e)
            return (0.5,)
        log.info("--------- EVALUATING ---------")
        log.info(individual)
        print(individual)
        if str(individual) in self.cache:
            log.info("Using from cache(" + str(individual) + "): " + str(self.cache[individual.__str__()]))
            return (self.cache[individual.__str__()],)

        lstm_model_handler = self.calculate_accuracy(individual)

        self.cache[individual.__str__()] = lstm_model_handler.result.result

        if lstm_model_handler.result.result > self.best_individual.result:
            log.info("NEW GLOBAL BEST RESULT")
            log.info(lstm_model_handler.result.result)
            self.best_individual.result = lstm_model_handler.result.result
            self.best_individual.architecture = lstm_model_handler.result.architecture
            self.best_individual.chromosome = chromosome
            self.best_model = lstm_model_handler.best_model
            self.modelio.save(self.best_model)

        print("---- Accuracy ----")
        log.info("---- Accuracy ----")
        print(lstm_model_handler.result.result)
        log.info(lstm_model_handler.result.result)
        self.cycles += 1
        time.sleep(50)
        return (lstm_model_handler.result.result,)

    def check_bounds(self, first, second):

        def decorator(func):
            def wrapper(*args, **kargs):
                try:
                    offspring = func(*args, **kargs)
                    for child in offspring:
                        for i in range(len(child)):
                            min_value = Optimization.MIN_MAX[i][0]
                            max_value = Optimization.MIN_MAX[i][1]
                            if child[i] > max_value:
                                child[i] = max_value
                            elif child[i] < min_value:
                                child[i] = min_value
                except Exception as e:
                    log.error(e)
                    raise e

                return offspring

            return wrapper

        return decorator

    def setup(self, toolbox):
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

        toolbox.register("adx_window", random.randint, Optimization.ADX_MIN_MAX[0], Optimization.ADX_MIN_MAX[1])
        toolbox.register("cci_window", random.randint, Optimization.CCI_MIN_MAX[0], Optimization.CCI_MIN_MAX[1])
        toolbox.register("mdi_window", random.randint, Optimization.MDI_MIN_MAX[0], Optimization.MDI_MIN_MAX[1])
        toolbox.register("pdi_window", random.randint, Optimization.PDI_MIN_MAX[0], Optimization.PDI_MIN_MAX[1])
        toolbox.register("stk_window", random.randint, Optimization.STK_MIN_MAX[0], Optimization.STK_MIN_MAX[1])
        toolbox.register("wma_window", random.randint, Optimization.WMA_MIN_MAX[0], Optimization.WMA_MIN_MAX[1])
        toolbox.register("psy_window", random.randint, Optimization.PSY_MIN_MAX[0], Optimization.PSY_MIN_MAX[1])

        toolbox.register("adx_active", random.randint, 0, 1)
        toolbox.register("cci_active", random.randint, 0, 1)
        toolbox.register("mdi_active", random.randint, 0, 1)
        toolbox.register("pdi_active", random.randint, 0, 1)
        toolbox.register("stk_active", random.randint, 0, 1)
        toolbox.register("wma_active", random.randint, 0, 1)
        toolbox.register("psy_active", random.randint, 0, 1)

        # Structure initializers
        toolbox.register("individual_guess", self.init_individual, creator.Individual)

        toolbox.register("individual", tools.initCycle, creator.Individual,
                       (toolbox.adx_window, toolbox.adx_active,
                        toolbox.cci_window, toolbox.cci_active,
                        toolbox.mdi_window, toolbox.mdi_active,
                        toolbox.pdi_window, toolbox.pdi_active,
                        toolbox.stk_window, toolbox.stk_active,
                        toolbox.wma_window, toolbox.wma_active,
                        toolbox.psy_window, toolbox.psy_active), 1)

        toolbox.register("population_guess", self.init_population, list, toolbox.individual_guess, "initial_guess.json")

        toolbox.register("evaluate", self.fitness)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.1)
        toolbox.register("select", tools.selTournament, tournsize=3)

        toolbox.decorate("mate", self.check_bounds(1, 2))
        toolbox.decorate("mutate", self.check_bounds(1, 2))

        return toolbox

    def run(self):
        random.seed(64)

        toolbox = base.Toolbox()

        toolbox = self.setup(toolbox)

        # Process Pool of 4 workers
        #pool = multiprocessing.Pool(processes=4)
        #toolbox.register("map", pool.map)

        pop = toolbox.population_guess()
        hof = tools.HallOfFame(1) # Elitism: preserve the 1 most fit individuals unmutated in each generation
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, logger = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=500, stats=stats, halloffame=hof, verbose=False)#ngen=500
        #pool.close()

        log.debug("Population:")
        log.debug(pop)
        log.info("The Best Result:")
        log.info(hof[0])
        print("The best result: ")
        print(hof[0])

        return pop, logger

    def calculate_accuracy(self, individual):
        train, test = individual.generate_dataset()
        log.info("Train Data:")
        log.info(train.head(5))
        log.info("Test Data:")
        log.info(test.head(5))
        lstm_model_handler = LSTMModelHandler.init_from_pandas_df(pandas_dataframe=train, pandas_dataframe_test=test,
                                                                  best_result=self.best_individual)

        # Build an optimezed hyper parameter LSTM model with two hidden layers
        #lstm_model_handler.build_lstm_two_hidden()
        try:

            lstm_model_handler.build_and_train_lstm_hyperparameter_opt_two_hidden()
        except Exception as e:
            log.error("NÃO FOI POSSÍVEL FINALIZAR")
            log.error(e)

            raise e


        return lstm_model_handler

    def init_individual(self, icls, content):
        return icls(content)

    def init_population(self, pcls, ind_init, filename):
        with open(filename, "r") as pop_file:
            contents = json.load(pop_file)
        return pcls(ind_init(c) for c in contents)