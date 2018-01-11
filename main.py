from multiprocessing.pool import Pool

from flask import Flask
from dateutil import parser
from genetic import optimization

import logging
logging.basicConfig(filename='lstm_sized.log', filemode='w', level=logging.DEBUG)


# create logger
logger = logging.getLogger("Main")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s", "%Y-%m-%d %H:%M:%S")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)



app = Flask(__name__)

best_result = None
finished = False
@app.route('/')
def index():
    return "Welcome: <a href='/start_computing'"

@app.route('/best')
def current_the_best():
    return str(best_result)

@app.route('/status')
def status():
    global finished

    if finished:
        return "Finished!"
    else:
        return "Not finished! Best: " + str(best_result)

@app.route('/start_computing')
def start_computing():
    global best_result
    best_result = optimization.BestIndividual()
    start_date = parser.parse("2007-01-01")
    end_date = parser.parse("2009-12-31")

    start_test_date = parser.parse("2012-01-01")
    end_test_date = parser.parse("2013-12-31")

    pool = Pool(processes=1)  # Start a worker processes.

    opt = optimization.Optimization("msft", start_date, end_date, start_test_date, end_test_date, best_result)
    result = pool.apply_async(opt.run, callback=callback)

    #pop, log = optimization.run()

    return 'Processamento Iniciado!'

def callback(pop, log):
    global finished
    logger.info(":Best of the best:")
    logger.info(str(optimization.best_individual))
    finished = True

@app.errorhandler(500)
def server_error(e):
    logger.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    logger.info("Starting...")
    try:
        app.run(host='127.0.0.1', port=8080, debug=True)
    except Exception as e:
        logger.error(e)
        logger.info("Finishing...")
# [END app]