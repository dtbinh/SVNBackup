from LinearRegressionCalculator import *
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    lr = LinearRegressionCalculator(7)
    lr.load('auto_mpg-norm.csv')
    #lr.calc()
    lr.runCnt = 10000
    #lr.calcByGA(1000, [-1.0, 1.0])
    lr.calcByPSO(1000, [-1.0, 1.0])
    print lr.betas
    print lr.mle
    
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(np.arange(lr.runCnt), lr.fitnessVal)
    plt.show()
    
    print lr.fitnessVal[lr.runCnt-1]
    