import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox

import pandas as pd
Data = pd.read_csv('12p6.csv')


all_x = np.array(Data['Tension'][:130])
all_y = np.array(abs(Data['Ampere'][:130]))

pos = [0,10]
x = all_x[:pos[1]]

fit = np.polyfit(x,all_y[:pos[1]],1)
y = fit[0]*all_x + fit[1]

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)

# plot de la courbe IV
plt.semilogy(all_x, all_y, lw=2, color='blue')
#plot du fit
l, = plt.semilogy(all_x, y, lw=2, color='red')

x1 = all_x[pos]
y1 =all_y[pos]
# plot des points du fit
p, = plt.semilogy(x1,y1, 'o', color='red')
#plot du courant électrique
I_e = all_y-y
g, = plt.semilogy(all_x, all_y-y)
#plt.axis([all_x[0], all_x[-1],min(I_e), max(I_e)])

posTe = [100, 120]
fit2 = np.polyfit(all_x[posTe[0]:posTe[1]],np.log(I_e[posTe[0]:posTe[1]]) ,1)
y2 = fit2[0]*all_x + fit2[1]
Te = 1/fit2[0]
h, = plt.semilogy(all_x, np.exp(y2))
x2 = all_x[posTe]
y2 = I_e[posTe]
p2, = plt.semilogy(x2,y2, 'o', color='orange')


axcolor = 'lightgoldenrodyellow'
axpos1 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axpos2 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axpos3 = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
axpos4 = plt.axes([0.25, 0.005, 0.65, 0.03], facecolor=axcolor)

spos1 = Slider(axpos1, 'pos1',valmin= 0, valmax=130, valinit=pos[0])
spos2 = Slider(axpos2, 'pos2',valmin= 0, valmax=130, valinit=pos[1])
spos3 = Slider(axpos3, 'pos3',valmin= 0, valmax=130, valinit=posTe[0])
spos4 = Slider(axpos4, 'pos4',valmin= 0, valmax=130, valinit=posTe[1])

axTe = plt.axes([0.3, 0.8, 0.2, 0.03], facecolor=axcolor)
Text_Te = TextBox(axTe, "Te", initial="{0:.2f}".format(round(Te,2)), color='.95', hovercolor='1', label_pad=0.01)

def update(val):
    pos = [int(spos1.val),int(spos2.val)]
    fit = np.polyfit(all_x[pos[0]:pos[1]], all_y[pos[0]:pos[1]],1)
    val_fit = fit[0]*all_x + fit[1]
    l.set_ydata(val_fit)
    p.set_ydata(all_y[pos])
    p.set_xdata(all_x[pos])
    I_e = all_y-val_fit
    g.set_ydata(I_e)
    posTe = [int(spos3.val),int(spos4.val)]
    print(posTe)
    #posTe = [int(spos1.val),int(spos2.val)]
    fit2 = np.polyfit(all_x[posTe[0]:posTe[1]], np.log(I_e[posTe[0]:posTe[1]]),1)
    val_fit2 = fit2[0]*all_x + fit2[1]
    h.set_ydata(np.exp(val_fit2))
    p2.set_ydata(I_e[posTe])
    p2.set_xdata(all_x[posTe])

    Te = 1/fit2[0]
    Text_Te.set_val("{0:.2f}".format(round(Te,2)))

    #plt.axis([all_x[0], all_x[-1],min(I_e), max(I_e)])
    fig.canvas.draw_idle()
spos1.on_changed(update)
spos2.on_changed(update)
spos3.on_changed(update)
spos4.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    spos1.reset()
    spos2.reset()
button.on_clicked(reset)




plt.show()
