from tsp_data import TSPData
from tsp_helper import TSPHelper
import random

class TSPState(object):
    """class representing a state of the TSP problem. Contains attributes:
       1. tspHelper - all TSPState objects share the same instance of tspHelper object
       2. path - This is the how a state is represented - an ordered list of cities that represents a tour
                 Note that a TSPState is represented by a tour rather than a single city. The current city of the tour is
                 the last city of the path
       3. value - represents cost of the tour represented by the TSPState
    """

    def __init__(self, tspHelper, path):
        """ Create  a TSPState. Takes 1. the tspHelper instance of the problem and
            2. a string representing path in the format A->B->C->D
        """
        self.tspHelper = tspHelper
        self.path = path
        self.value = -1

    def getPath(self):
        return '->'.join(self.path)
    
    def isGoalState(self):
        """Checks if starts and ends at the same city and has visited all the other cities exactly once"""
        return self.path[0] == self.tspHelper.startCity and \
               self.path[0] == self.path[-1] and \
               sorted(self.path[0:-1]) == sorted(self.tspHelper.tspData.getAllCities())

    def moveToNextState(self, nextState):
        """Takes the necessary step to move from current state to the nextState"""
        pass

    def getSuccessor(self):
        """Returns a random next state using the following method:
           Take 2 rndom cities on the current tour (other than start and ending city)
           reverse the path between those 2 cities
        """
        currentTour = self.path[:]
        #special handling for # of cities < 3. No successors for such case
        if len(currentTour) < 4: return None
        
        position1 = -1
        position2 = -1
        while position1 == position2:
            #choosing 2 random positions other than start and end
            position1 = random.randint(1, len(currentTour)-2)
            position2 = random.randint(1, len(currentTour)-2)
            if position1 > position2:
                position1, position2 = position2, position1


        newTour = currentTour[:position1] + list(reversed(currentTour[position1: position2 +1])) + currentTour[position2 +1:]
        successor = TSPState(self.tspHelper, newTour)
        return successor
        


    def getValue(self):
        if self.value == -1:
            pathCost = 0
            for i in range(len(self.path) - 1):
                pathCost += self.tspHelper.tspData.getDistance(self.path[i], self.path[i+1])
            self.value = pathCost
        return self.value

    def summary(self):
        print(15*'=' + "State Summary" + 15*'=')
        print("Tour = %s" % '->'.join(self.path))
        print('Cost = %.2f' % self.getValue())
        print(42*'=')

if __name__ == '__main__':
    tspData = TSPData('C:/Users/nkadiyar/Documents/git-repos/simulated-annealing/simulated-annealing-tsp/input-data/6/instance_5.txt');
    tspData.summary()
    tspHelper = TSPHelper(tspData, startCity='A')

    #Test TSPState creation 
    startState = TSPState(tspHelper, tspHelper.getGreedyTour()[0])
    print('\nThis is the initial state')
    startState.summary()

    #Find the successor of the state
    successor = startState.getSuccessor()
    if successor:
        print('The state %s has successor: %s' % (startState.getPath(), successor.getPath()))
        successor.summary()
    else:
        print('No successor for state %s' % startState.getPath())


    
