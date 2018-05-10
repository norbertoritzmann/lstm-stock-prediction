import numpy
import pandas as pd


def extract_and_append_next_day_close(df):
    next_days = extract_next_day_close(df)
    willRiseSeries = pd.Series(next_days, index=df.index)
    #temp = df[['Close']]
    #temp['willRise'] = willRiseSeries
    df['willRise'] = willRiseSeries
    return df
    #df['willRise'] = pd.DataFrame({'Date': df["Date"], 'Close': df["Close"], 'willRise': willRiseSeries})


def extract_next_day_close(df):
    closings = df["Close"]
    #df['willRise'] = 1
    next_days = []
    next_day_index = 1
    #next_days.append(0)

    for today_close in closings:
        if next_day_index == len(closings):
            next_days.append(today_close)
            break

        next_days.append(closings[next_day_index])

        next_day_index += 1

    return next_days


def extract_and_append_next_day_will_rise(df):
    next_days = extract_next_day_will_rise(df)
    willRiseSeries = pd.Series(next_days, index=df.index)
    #temp = df[['Close']]
    #temp['willRise'] = willRiseSeries
    df['willRise'] = willRiseSeries
    return df
    #df['willRise'] = pd.DataFrame({'Date': df["Date"], 'Close': df["Close"], 'willRise': willRiseSeries})


def extract_next_day_will_rise(df):
    closings = df["Close"]
    #df['willRise'] = 1
    next_days = []
    next_day_index = 1
    #next_days.append(0)

    for today_close in closings:
        if next_day_index == len(closings):
            next_days.append(0)
            break
        if today_close > closings[next_day_index]:
            next_days.append(0)
        else:
            next_days.append(1)
        next_day_index += 1
        #next_days.append(0)

    return next_days

def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window_data[0])) - 1) for p in window]
        normalised_data.append(normalised_window)
    return normalised_data


'''Transforms a pandas dataframe into a keras model readable data
   Returns data and target in separate
'''
def extract_keras_format_data(pandas_dataframe, train_columns, target_columns):
    if target_columns not in pandas_dataframe.columns:
        print("Target None")
    y = pandas_dataframe.pop(target_columns).as_matrix()
    #y = pandas_dataframe[target_columns].as_matrix()
    if train_columns is not None:
        x = pandas_dataframe[train_columns].values
    else:
        x = pandas_dataframe.values

    x = reshape(x)
    if len(y.shape) == 1:
        y = reshape_y_2D(y)

    return x, y


def reshape(x):
    x = numpy.reshape(x, (x.shape[0], 1, x.shape[1]))
    return x


def reshape_y(y):
    y = numpy.reshape(y, (y.shape[0], 1, 1))
    return y

def reshape_y_2D(y):
    y = numpy.reshape(y, (y.shape[0], 1))
    return y