from routes import *

def check(location, destination, passenger, minimum):
    if (location == ''
                or destination == ''
                or not passenger.isnumeric()
                or not minimum.isnumeric()
                or int(passenger) < 1
                or int(minimum) < 1):
        return True
    else:
        return False
