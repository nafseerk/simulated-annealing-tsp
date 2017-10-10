import math
import matplotlib.pyplot as plt

class ExponentialSchedule(object):
    """Uses exponential schedule. Reference: http://iopscience.iop.org/article/10.1088/0305-4470/31/41/011/pdf 
        T(t) = T0 X αt(α raised to the power t) 
    """

    def __init__(self, alpha=0.999995, T0=200000):
        self.alpha = alpha
        self.T0 = T0
        self.T = T0
        
        
    def getTemperature(self, stepCount):
        self.T = self.T0 * (self.alpha**stepCount)

        #Round to 2 decimal places
        self.T = math.ceil(self.T*100)/100 
        return self.T
    

class LogarithmicSchedule(object):
    """Uses logaritmic multiplicative schedule. Reference: Aarts, E.H.L. & Korst, J., 1989 
        T(t) = T0 / (1 + αLog(1 + t))
    """

    def __init__(self, alpha=1000, T0=10000):
        self.alpha = alpha
        self.T0 = T0
        self.T = T0
        
        
    def getTemperature(self, stepCount):
        self.T = self.T0 / (1 + self.alpha * math.log(1 + stepCount))

        #Round to 2 decimal places
        self.T = (self.T*100)/100 
        return self.T

class QuadraticSchedule(object):
    """Uses linear schedule. Reference: http://iopscience.iop.org/article/10.1088/0305-4470/31/41/011/pdf
        T(t) = T0 * ((maxSteps - stepCount)/maxSteps)^4 
    """
    def __init__(self, alpha=1, T0=2000000, maxSteps = 2000000):
        self.alpha = alpha
        self.T0 = T0
        self.T = T0
        self.maxSteps = maxSteps
        
        
    def getTemperature(self, stepCount):
            
        self.T = self.T0 * ((self.maxSteps - stepCount)/self.maxSteps)**4

        #Round to 1 decimal places
        self.T = (self.T*10)/10 
        return self.T    

    
if __name__ == '__main__':
    #Test Exponential schedule
    schedule = ExponentialSchedule()
    x = []
    y = []
    for stepCount in range(1, 1500001):
        x.append(stepCount)
        y.append(schedule.getTemperature(stepCount))
    plt.scatter(x,y)
    plt.show()

    #Test Linear schedule
    schedule = LogarithmicSchedule()
    x = []
    y = []  
    for stepCount in range(1, 50001):
        x.append(stepCount)
        y.append(schedule.getTemperature(stepCount))

    plt.scatter(x,y)
    plt.show()

    #Test Quadratic schedule
    x = []
    y = []
    schedule = QuadraticSchedule()
    for stepCount in range(1, 2000001):
        x.append(stepCount)
        y.append(schedule.getTemperature(stepCount))  
    plt.scatter(x,y)
    plt.show()

    
