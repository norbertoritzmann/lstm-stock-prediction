import logging
from multiprocessing.pool import Pool

from flask import Flask
from dateutil import parser
from genetic import optimization

import logging
logging.basicConfig(filename='lstm_sized.log', filemode='w', level=logging.DEBUG)

app = Flask(__name__)

opt = None
finished = False

@app.route('/best')
def current_the_best():
    return str(opt.best_individual)

@app.route('/status')
def status():
    global finished
    if finished:
        return "Finished!"
    else:
        return "Not finished!"

@app.route('/start_computing')
def start_computing():
    global opt
    start_date = parser.parse("2005-01-01")
    end_date = parser.parse("2009-12-31")

    start_test_date = parser.parse("2010-01-01")
    end_test_date = parser.parse("2013-12-31")

    pool = Pool(processes=1)  # Start a worker processes.
    opt = optimization.Optimization("msft", start_date, end_date, start_test_date, end_test_date)
    result = pool.apply_async(opt.run, callback)

    #pop, log = optimization.run()

    return 'Processamento Iniciado!'

def callback(pop, log):
    global finished
    logging.info(":Best of the best:")
    logging.info(str(optimization.best_individual))
    finished = True

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]