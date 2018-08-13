
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

import pandas as pd
Data = pd.read_csv('12p6.csv')


all_x = Data['Tension'][:130]
all_y = abs(Data['Ampere'][:130])
pos1 = 50
x = all_x[:pos1]

fit = np.polyfit(x,all_y[:pos1],1)
y = fit[0]*all_x + fit[1]

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)


a0=1
f0=1
delta=1
# plot de la courbe IV
plt.semilogy(all_x, all_y, lw=2, color='blue')
#plot du fit
l, = plt.semilogy(all_x, y, lw=2, color='red')
#plt.axis([0, 1, -10, 10])

axcolor = 'lightgoldenrodyellow'
axpos1 = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axpos2 = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

spos1 = Slider(axpos1, 'pos1', 0, 130, valinit=0, valstep=delta)
spos2 = Slider(axpos2, 'pos2', 0, 130, valinit=10,valstep=delta)


def update(val):
    pos1 = int(spos1.val)
    pos2 = int(spos2.val)
    fit = np.polyfit(all_x[pos1:pos2], all_y[pos1:pos2],1)
    l.set_ydata(fit[0]*all_x + fit[1])
    fig.canvas.draw_idle()
spos1.on_changed(update)
spos2.on_changed(update)

resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')


def reset(event):
    spos1.reset()
    spos2.reset()
button.on_clicked(reset)

rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)


def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()
radio.on_clicked(colorfunc)

plt.show()
