import math
from tabulate import tabulate
import itertools

class TSPData(object):
    """ The data object that stores all the input data of the TSP Problem -
        1. The no of cities - citiesCount
        2. The names/Ids of the cities - citiesNames
        3. The x,y coordinates of the cities - citiesCoordinates
    """   
    
    def __init__(self, inputFileName):
        """ Loads the data from the input file. Assumes the format:
            no of cities (first line),
            cityId, x, y (on each subsequent line)
        """ 
        f = open(inputFileName, 'r') 
        lines = f.readlines()
        f.close()
        
        self.citiesCount=int(lines[0])
        self.citiesNames = []
        self.citiesCoordinates = {}

        for line in lines[1:]:
            cityId, cityX, cityY = line.split(' ')
            self.citiesNames.append(cityId)
            self.citiesCoordinates[cityId] = (int(cityX), int(cityY))

        return


    def getDistance(self, city1, city2):
        """ Returns the Euclidean distance between city1 and city2"""
        x1, y1 = self.citiesCoordinates[city1]
        x2, y2 = self.citiesCoordinates[city2]
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def getDistancesFromCity(self, fromCity, otherCities):
        distances = []

        for otherCity in otherCities:
            distances.append((otherCity, self.getDistance(fromCity, otherCity)))

        return sorted(distances, key=lambda tup: tup[1])

    def getAllCities(self):
        return self.citiesNames
        
    def summary(self, file=None):
        print(15*'=' + "Data Summary" + 15*'=', file=file)
        print('No of cities = %d' % self.citiesCount, file=file)
        headers = ['City', 'X-coordinate', 'Y-coordinate']
        data = sorted([(k,v[0],v[1]) for k,v in self.citiesCoordinates.items()])
        print(tabulate(data, headers=headers), file=file)
        print(42*'=', file=file)

    def getMinimumSpanningTreeCost(self, citiesList, startCity):
        """Calculate the cost of all the edges of the Minimum Spanning Tree
           formed from the graph represented by cities list
        """
        #TODO: move this to TSPHelper class
        if len(citiesList) == 0:
            return 0
        
        if startCity not in citiesList:
            print('StartCity should be in the cities list')

        #find the distances of all of city-pairs and sort by the distance
        paths = [(path[0], path[1], self.getDistance(path[0], path[1])) for path in itertools.combinations(citiesList, 2)]
        paths.sort(key=lambda tup: tup[2])

        #Progressively build the MST
        mstSoFar = [startCity]
        mstPathCost = 0 
        del citiesList[citiesList.index(startCity)]

        while citiesList:
            #From all possible city pairs take only those that connect a city from mstSoFar to a city not in mstSoFar
            filteredPaths = []
            for path in paths:
                if (path[0] in mstSoFar and path[1] not in mstSoFar) or (path[1] in mstSoFar and path[0] not in mstSoFar):
                    filteredPaths.append(path)                   
            filteredPaths = sorted(filteredPaths, key=lambda tup: tup[2])
            
            nextPath = filteredPaths.pop(0) #of the paths that connect mstSoFar to the rest of the graph, take the lowest cost edge

            #Get the next city to be added into the MST
            if (nextPath[0] in mstSoFar) and (nextPath[1] not in mstSoFar):
                nextCity = nextPath[1]
            elif (nextPath[1] in mstSoFar) and (nextPath[0] not in mstSoFar):
                nextCity = nextPath[0]
            mstPathCost += nextPath[2]
            mstSoFar.append(nextCity)
            del citiesList[citiesList.index(nextCity)]
            paths = [path for path in paths if path != nextPath]
        return mstPathCost
                    
if __name__ == '__main__':
    #Load the data from the input file
    testData = TSPData('C:/Users/nkadiyar/Documents/git-repos/simulated-annealing/simulated-annealing-tsp/input-data/8/instance_5.txt')

    #Print the data summary
    testData.summary()

    #Print all the city names
    citiesList = testData.getAllCities()
    print('List of Cities =', end=' ')
    print(citiesList)

    #Print the distance between any two cities
    print('Distance from %s to %s = %d' % (citiesList[0], citiesList[1], testData.getDistance(citiesList[0], citiesList[1])))

    #Print the distances from one city to all other cities
    print('Distances from %s to other cities:' % citiesList[0])
    print(testData.getDistancesFromCity(citiesList[0], citiesList))

    #Print the minimum Spanning Tree Cost of the entire tree
    print('Minimum Spanning Tree Cost = %f' % testData.getMinimumSpanningTreeCost(citiesList, citiesList[0]))

