import pendulum

def gap_years(x: int) -> list[pendulum.DateTime]:
    """ Gets the last x years of data 
    
    Parameters
    ----------
    x: int
        number of years to get of data
    """
    dates = []
    date_now = pendulum.now()
    for i in range(1,x+1):
        sub_year = date_now.subtract(years=i)
        dates.append(sub_year.format("YYYY"))
    return dates

if __name__ == '__main__':
    dates = gap_years(3)
    print(dates)
