import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox

import pandas as pd
Data = pd.read_csv('3mt.csv')

x = np.array(Data['Tension'])
y = np.array(Data['Current'])

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
        if log==True:
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


Ion_current = Current(x,y,icursor = [0,10])
Ion_current.Fit()

# initialization of the figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_ylim(1e-6, 2*max(y))
# plot de la courbe IV
plt.semilogy(x, abs(y), lw=2, color='blue')
#plot du fit
plot1, = plt.semilogy(Ion_current.x, abs(Ion_current.fit), lw=2, color='red')


# plot des points du fit
plot2, = plt.semilogy(Ion_current.posx,Ion_current.posy, 'o', color='red')
#plot du courant électrique
I_e = y-Ion_current.fit
plot3, = plt.semilogy(x, I_e)
#plt.axis([all_x[0], all_x[-1],min(I_e), max(I_e)])
Fit_Te = Current(x,I_e,icursor = [len(x)-50,len(x)-1])
Fit_Te.Fit(log=True)


plot4, = plt.semilogy(Fit_Te.x, np.exp(Fit_Te.fit))
plot5, = plt.semilogy(Fit_Te.posx,Fit_Te.posy, 'o', color='orange')


axcolor = 'lightgoldenrodyellow'
axpos1 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axpos2 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axpos3 = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
axpos4 = plt.axes([0.25, 0.005, 0.65, 0.03], facecolor=axcolor)

spos1 = Slider(axpos1, 'pos1',valmin= 0, valmax=len(x), valinit=Ion_current.icursor[0])
spos2 = Slider(axpos2, 'pos2',valmin= 0, valmax=len(x), valinit=Ion_current.icursor[1])
spos3 = Slider(axpos3, 'pos3',valmin= 0, valmax=len(x), valinit=Fit_Te.icursor[0])
spos4 = Slider(axpos4, 'pos4',valmin= 0, valmax=len(x), valinit=Fit_Te.icursor[1])

axTe = plt.axes([0.3, 0.8, 0.2, 0.03], facecolor=axcolor)
Text_Te = TextBox(axTe, "Te", initial="{0:.2f}".format(round(Fit_Te.Te,2)), color='.95', hovercolor='1', label_pad=0.01)

def update(val):
    Ion_current.seticursor(int(spos1.val), int(spos2.val))
    Ion_current.Fit()
    plot1.set_ydata(abs(Ion_current.fit))
    plot2.set_xdata(Ion_current.posx)
    plot2.set_ydata(Ion_current.posy)
    I_e = y-Ion_current.fit
    plot3.set_ydata(I_e)
    Fit_Te.set_y(I_e)
    Fit_Te.seticursor(int(spos3.val), int(spos4.val))
    Fit_Te.Fit(log=True)

    plot4.set_ydata(np.exp(Fit_Te.fit))
    plot5.set_xdata(Fit_Te.posx)
    plot5.set_ydata(Fit_Te.posy)

    Text_Te.set_val("{0:.2f}".format(round(Fit_Te.Te,2)))

    #plt.axis([all_x[0], all_x[-1],min(I_e), max(I_e)])
    fig.canvas.draw_idle()
spos1.on_changed(update)
spos2.on_changed(update)
spos3.on_changed(update)
spos4.on_changed(update)






plt.show()
