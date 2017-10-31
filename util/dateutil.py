def getFirstDay(funds,year,month):
    for date in funds.index:
        if((date.year==year) and (date.month==month)):
            return(date)
    return('ERROR')

def getLastDay(funds,year,month):
    return_date = 'ERROR'
    for date in funds.index:
        if((date.year==year) and (date.month==month)):
            return_date = date
    return(return_date)
