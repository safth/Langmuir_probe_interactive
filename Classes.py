import numpy as np
import matplotlib.pyplot as plt

class Current():

    def __init__(self,x,y,icursor):
        self.icursor = icursor
        self.posx = x[self.icursor]
        self.posy = abs(y[self.icursor])
        self.x = x
        self.y = y
        self.fit = []
        self.Te = 0
    def Fit(self,log=False):
        fit=[]
        if log==True: # for Te, we want a lin fit on the log! (fit an exponetial)
            fit = np.polyfit(self.x[self.icursor[0]:self.icursor[1]],
                        np.log(self.y[self.icursor[0]:self.icursor[1]]),1)
        else:
            fit = np.polyfit(self.x[self.icursor[0]:self.icursor[1]],
                        self.y[self.icursor[0]:self.icursor[1]],1)

        self.fit = fit[0]*self.x + fit[1]
        self.Te = 1/fit[0]

    def seticursor(self,a,b):
        self.icursor = [a,b]
        self.posx = self.x[self.icursor]
        self.posy = abs(self.y[self.icursor])

    def set_y(self,new_y):
        self.y = new_y
