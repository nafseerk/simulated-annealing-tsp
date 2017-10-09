from tsp_data import TSPData
from tsp_helper import TSPHelper
from tsp_state import TSPState
from schedule import ExponentialSchedule, LogarithmicSchedule, QuadraticSchedule
import random, math
import time as tm
import matplotlib.pyplot as plt

class Problem(object):

    def __init__(self, initialState, stoppingTemperature=1):
        self.initialState = initialState
        self.Tstop = stoppingTemperature
        self.time = -1
        self.T = -1
        self.finalState = None
        self.x_axis = []
        self.y_axis = []

    def getStoppingTemperature(self):
        return self.Tstop

    def getInitialState(self):
        return self.initialState

    def setTime(self, time):
        self.time = time

    def getTime(self):
        return self.time

    def setTemperature(self, temperature):
        self.T = temperature

    def getTemperature(self):
        return self.T

    def setFinalState(self, state):
        self.finalState = state

    def getFinalState(self):
        return self.finalState

    def setResults(self, state, time, temperature, xValues, yValues):
        self.setFinalState(state)
        self.setTime(time)
        self.setTemperature(temperature)
        self.x_axis = xValues
        self.y_axis = yValues
        

    
def simulated_annealing(problem, schedule):
    currentState = problem.getInitialState()
    startTime = tm.time()
    time = 1
    x_time = [0]
    y_cost = [currentState.getValue()]
    while True:
        #print('At time %d' % time)
        currentTemperature = schedule.getTemperature(time)
        #print('Current temprature = %f' % currentTemperature)

        #TODO: When to stop
        #Stop when the system is at equilibrium
        if currentTemperature <= problem.getStoppingTemperature():
            problem.setResults(currentState, time, currentTemperature, x_time, y_cost)
            return

        #print('Current state: %s' % currentState.getPath())
        #print('Current state cost = %f' % currentState.getValue())
        nextState = currentState.getSuccessor()
        #print('Next state: %s' % nextState.getPath())
        #print('Next state cost = %f' % nextState.getValue())
        deltaValue = nextState.getValue() - currentState.getValue()
        #print('deltaValue = %d' % deltaValue)

        if deltaValue < 0: #If improvement, then accept the solution  TODO: what to do if deltaValue = 0
            currentState = nextState
            #print('Better Solution...Accepting')
        elif acceptWithProbabilty(deltaValue, currentTemperature): #If bad solution, then accept with probability
            currentState = nextState
            #print('Bad Solution...Accepting')
        else:
            pass
            #print('Bad Solution...Not Accepting')
        #input('Enter to continue...')
        x_time.append(time)
        y_cost.append(currentState.getValue())
        time += 1
        #Stop after 5 minute    
        currentTime = tm.time()
        if (currentTime - startTime)/60 > 5:
            print('Terminating after 5 minutes...')
            break
    problem.setResults(currentState, time, currentTemperature, x_time, y_cost)
    return


def acceptWithProbabilty(valueChange, temperature):
    probability = math.exp(-valueChange/temperature)
    #print('P=%.2f' % probability)
    return random.random() < probability


if __name__ == '__main__':
    tspData = TSPData('C:/Users/nkadiyar/Documents/git-repos/simulated-annealing/simulated-annealing-tsp/input-data/problem36');
    tspData.summary()
    tspHelper = TSPHelper(tspData, startCity='A')

    #Create initial state 
    startState = TSPState(tspHelper, tspHelper.getGreedyTour()[0])
    print('The start state: %s' % startState.getPath())
    print('The start cost: %.2f' % startState.getValue())

    #TODO: how to set the initial temperature
    #Create schedule
    #schedule = ExponentialSchedule()
    #schedule = LogarithmicSchedule(T0=10000)
    schedule = QuadraticSchedule()
    
    
    #Perform simulated annealing
    problem = Problem(startState)
    simulated_annealing(problem, schedule)
    finalState = problem.getFinalState()

    print('The final state: %s' % finalState.getPath())
    print('The final cost: %.2f' % finalState.getValue())
    print('Solution found after %d steps and %.2f temperature' % (problem.getTime(), problem.getTemperature()))
    plt.scatter(problem.x_axis, problem.y_axis)
    plt.show()
