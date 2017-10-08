from tsp_data import TSPData

class TSPHelper(object):
    """Helper class for carrying out book keeping tasks related to TSP problem.
       Also contains utility functions. Has attributes
       1. tspData - tspData instance of the specific TSP problem
       2. startCity - starting city of the tour which is also the last city of the tour
    """

    def __init__(self, tspData, startCity=None):
        self.tspData = tspData
        
        if not startCity:
            self.startCity = tspData.getAllCities()[0]
        else:
            self.startCity = startCity


    def getStartCity(self):
        return self.startCity
    
    def getGreedyTour(self):
        """
           A tour starting at startCity and going to the next closest city
        """
        tour = [self.startCity]
        tourCost = 0
        remainingCities = self.tspData.getAllCities()
        remainingCities.remove(self.startCity)

        while remainingCities:
            currentCity = tour[-1]
            distancesFromCurrentCity = self.tspData.getDistancesFromCity(currentCity, remainingCities)
            nextCity = distancesFromCurrentCity[0][0]
            tour.append(nextCity)
            tourCost += distancesFromCurrentCity[0][1]
            remainingCities.remove(nextCity)

        tourCost += self.tspData.getDistance(tour[-1], self.startCity)
        tour.append(self.startCity)
        return tour, tourCost
        

if __name__ == '__main__':
    tspData = TSPData('C:/Users/nkadiyar/Documents/git-repos/simulated-annealing/simulated-annealing-tsp/input-data/8/instance_5.txt');
    tspData.summary()
    print('List of cities', end=' ')
    print(tspData.getAllCities())

    tspHelper = TSPHelper(tspData)
    print('start city = ' + tspHelper.getStartCity())

    #Test greedy tour
    initialTour, initialTourCost = tspHelper.getGreedyTour()
    print('Greedy tour:', end=' ')
    print('->'.join(initialTour))
    print('Tour Cost = %.2f' % initialTourCost)


