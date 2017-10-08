import math

class ExponentialSchedule(object):
    """Uses exponential schedule. Reference: http://iopscience.iop.org/article/10.1088/0305-4470/31/41/011/pdf 
        T(t) = T0 X αt(α raised to the power t) 
    """

    def __init__(self, alpha=0.995, T0=10000):
        self.alpha = alpha
        self.T0 = T0
        self.T = T0
        
        
    def getTemperature(self, stepCount):
        self.T = self.T0 * (self.alpha**stepCount)

        #Round to 2 decimal places
        self.T = math.ceil(self.T*100)/100 
        return self.T
    
    

if __name__ == '__main__':
    schedule = ExponentialSchedule()
    for stepCount in range(1, 1001):
        print(schedule.getTemperature(stepCount))
