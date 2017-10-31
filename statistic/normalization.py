

def standardization(df):

    return (df - df.mean()) / df.std()

def min_max(df):

    return (df - df.min()) / (df.max() - df.min())