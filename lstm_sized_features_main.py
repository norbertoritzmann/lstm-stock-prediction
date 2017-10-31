from dateutil import parser
from genetic import optimization
import logging
'''
[X] 1. Criar um tranformador para gerar a coluna target_columns='willRise'
[X] 2. Filtrar os resultados por data para cada conjunto (teste e treino)
[X] 3. Criar um loop de treinamento do AG para capturar as colunas do repositório, gerando um novo df
'''
logging.basicConfig(filename='lstm_sized.log', filemode='w', level=logging.DEBUG)

# [ ] 1. willRise Transformer
#feat_forward_rise_days_class

# [ ] 2. Filtro
start_date = parser.parse("2005-01-01")
end_date = parser.parse("2009-12-31")

start_test_date = parser.parse("2010-01-01")
end_test_date = parser.parse("2013-12-31")

# [ ] 3. GA
optimization = optimization.Optimization("msft", start_date, end_date, start_test_date, end_test_date)

pop, log = optimization.run()

logging.info(":Best of the best:")
logging.info(str(optimization.best_individual))

#dfFordX, dfFordY, dfFordFull = Validation.load_holdout("ford.csv")
#fordX = timeseries.reshape(dfFordX.values)
#fordY = timeseries.reshape_y(dfFordY.values)#fordFull

#dfJpmX, dfJpmY, dfJpmFull = Validation.load_holdout("jpm.csv")
#jpmX = timeseries.reshape(dfJpmX.values)
#jpmY = timeseries.reshape_y(dfJpmY.values)

#dfTescoX, dfTescoY, dfTescoFull = Validation.load_holdout("TESCO.csv")
#tescoX = timeseries.reshape(dfTescoX.values)
#tescoY = timeseries.reshape_y(dfTescoY.values)


#val = Validation(lstm_model_handler.model)


#predicted = val.predict_point_by_point(lstm_model_handler.testX)
#predictedFord = val.predict_point_by_point(fordX)
#predictedJpm = val.predict_point_by_point(jpmX)
#predictedTesco = val.predict_point_by_point(tescoX)

#print("MSFT: ", val.mesure_accuracy(predicted, lstm_model_handler.testY))
#print("Ford: ", val.mesure_accuracy(predictedFord, fordY))
#print("JPM: ", val.mesure_accuracy(predictedJpm, jpmY))
#print("TESCO: ", val.mesure_accuracy(predictedTesco, tescoY))