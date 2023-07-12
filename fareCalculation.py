
from routes import starting_place_1


class Computation:
    def __init__(self):
        pass

    def calculate(status, starting_place, destination, passenger, minimum_fare):

        # Status and Discount
        if status == "Regular Commuter":
            getStatus = "Regular Commuter"
            getDiscount = "None"
        else:
            getStatus = "Discount Beneficiary"
            getDiscount = "20%"

        getTransit = starting_place+" to "+destination

        # Total

        # Getting the distance of starting place and destination in km
        distance1 = int(starting_place_1.index(starting_place))
        distance2 = int(starting_place_1.index(destination))

        # Subtracting the distance of the two to get the final distance
        total_distance1 = abs(distance1 - distance2)

        getDistance = total_distance1

        # Number of passenger
        number_of_passenger = int(passenger)

        # Minimum Fare
        min_fare = int(minimum_fare)

        # When the total distance is less than 4 then the tentative cost = 9 (Minimum Fare)
        if total_distance1 <= 4:
            tentative_cost = min_fare * number_of_passenger
        # Else, the total distance is the result of the formula below.
        else:
            tentative_cost = (((total_distance1 - 4) * 1.50) +
                              min_fare) * number_of_passenger

        # If status is student/ elderly/ disabled, discount is 20%
        if status == "Regular":
            fare_cost = tentative_cost
        else:
            discount_ = round((tentative_cost * 0.20), 2)
            fare_cost = tentative_cost - discount_

        getTotal = fare_cost

        return getStatus, getDiscount, getTransit, getDistance, getTotal,
