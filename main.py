import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
from Classes import Current
import pandas as pd

# This function calculate all the parameters of a Langmuir probe analysis
# with ajustables fit to see the effect on every fits.


Data = pd.read_csv('3mt.csv')

x = np.array(Data['Tension'])
y = np.array(Data['Current'])

##
## Data initialisation
##
#instance of the ion current


Ion_current = Current(x,y,icursor = [0,10])
Ion_current.Fit()

# Electron current
I_e = y-Ion_current.fit

# instance of the Fit on the electron current
Fit_Te = Current(x,I_e,icursor = [round(len(x)/2),round(len(x)/2)+50])
Fit_Te.Fit(log=True)
#instance of the electron saturation current to find Vp and Ise
Fit_Ne = Current(x,y,icursor=[len(x)-20,len(x)-1])
Fit_Ne.Fit()

#set later, except Vf, its constant.
V_p = 0
I_se = 0
iV_f =  np.abs(y).argmin()
V_f = x[iV_f]


##
## initialization of the figure
##
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
ax.set_ylim(1e-6, 2*max(y)) # y axis limit.
plt.xlabel('Tension (V)')
plt.ylabel('Current (A)')


# Plot of the IV curve (data provided)
plt.semilogy(x, abs(y), lw=2, color='blue')
# Plot of the Ion_current (linear Fit)
plot_Ii, = plt.semilogy(Ion_current.x, abs(Ion_current.fit),'--', color='red')
# Plot of the cursor of the ion current linear fit.
plot_Ion_cursor, = plt.semilogy(Ion_current.posx,Ion_current.posy, 'o', color='red')
# Plot of the electron current (I_tot - I_i)
plot_Ie, = plt.semilogy(x, I_e)
# plot of the fit on the linear part (in log) of Ie to find Te
plot_Te, = plt.semilogy(Fit_Te.x, np.exp(Fit_Te.fit),'--',color='orange')
plot_Te_cursor, = plt.semilogy(Fit_Te.posx,Fit_Te.posy, 'o', color='orange')

#This is a lin fit on the electron saturation current to find Vp ans Ise
plot_Ne, = plt.semilogy(Fit_Ne.x, Fit_Ne.fit, '--', color='green')
plot_Ne_cursor, = plt.semilogy(Fit_Ne.posx,Fit_Ne.posy, 'o', color='green')


##
## creation of the slider to chose the limits of the fits
##
axcolor = 'lightgoldenrodyellow'
                #x pos, y pos, x size, y size
axpos1 = plt.axes([0.20, 0.12, 0.30, 0.03], facecolor=axcolor)
axpos2 = plt.axes([0.60, 0.12, 0.30, 0.03], facecolor=axcolor)
axpos3 = plt.axes([0.20, 0.07, 0.30, 0.03], facecolor=axcolor)
axpos4 = plt.axes([0.60, 0.07, 0.30, 0.03], facecolor=axcolor)
axpos5 = plt.axes([0.20, 0.02, 0.30, 0.03], facecolor=axcolor)
axpos6 = plt.axes([0.60, 0.02, 0.30, 0.03], facecolor=axcolor)

spos1 = Slider(axpos1, 'fit ion',valmin= 0, valmax=len(x), valinit=Ion_current.icursor[0])
spos2 = Slider(axpos2, '',valmin= 0, valmax=len(x)-1, valinit=Ion_current.icursor[1])
spos3 = Slider(axpos3, 'fit Te',valmin= 0, valmax=len(x), valinit=Fit_Te.icursor[0])
spos4 = Slider(axpos4, '',valmin= 0, valmax=len(x)-1, valinit=Fit_Te.icursor[1])
spos5 = Slider(axpos5, 'fit electron',valmin= 0, valmax=len(x), valinit=Fit_Ne.icursor[0])
spos6 = Slider(axpos6, '',valmin= 0, valmax=len(x)-1, valinit=Fit_Ne.icursor[1])

# the text box that give Te and Vp
axTe = plt.axes([0.3, 0.9, 0.1, 0.03], facecolor=axcolor)
Text_Te = TextBox(axTe, "Te", initial="{0:.2f}".format(round(Fit_Te.Te,2)), color='.95', hovercolor='1', label_pad=0.01)
axVp = plt.axes([0.44, 0.9, 0.1, 0.03], facecolor=axcolor)
Text_Vp = TextBox(axVp, "Vp", initial="{0:.2f}".format(round(V_p,2)), color='.95', hovercolor='1', label_pad=0.01)
axVf = plt.axes([0.58, 0.9, 0.1, 0.03], facecolor=axcolor)
Text_Vf = TextBox(axVf, "Vf", initial="{0:.2f}".format(round(V_f,2)), color='.95', hovercolor='1', label_pad=0.01)
axIse = plt.axes([0.72, 0.9, 0.12, 0.03], facecolor=axcolor)
Text_Ise = TextBox(axIse, "Ise", initial="{0:.2e}".format(round(I_se,2)), color='.95', hovercolor='1', label_pad=0.01)

#
# All action occurs here
#

def update(val):
    # Get the upper and lower x limit of the fit
    Ion_current.seticursor(int(spos1.val), int(spos2.val))
    Ion_current.Fit() # fit
    plot_Ii.set_ydata(abs(Ion_current.fit)) # plot
    plot_Ion_cursor.set_xdata(Ion_current.posx) # plot
    plot_Ion_cursor.set_ydata(Ion_current.posy) # plot
    #calculate the electron current (Itot-Ii)
    I_e = y-Ion_current.fit
    plot_Ie.set_ydata(I_e) # plot
    Fit_Te.set_y(I_e) #get the data in the object
    #Get the upper and lower x limit of the fit
    Fit_Te.seticursor(int(spos3.val), int(spos4.val))
    Fit_Te.Fit(log=True) #fit

    plot_Te.set_ydata(np.exp(Fit_Te.fit))# plot
    plot_Te_cursor.set_xdata(Fit_Te.posx)# plot
    plot_Te_cursor.set_ydata(Fit_Te.posy)# plot
    #Get the upper and lower x limit of the fit
    Fit_Ne.seticursor(int(spos5.val), int(spos6.val))
    Fit_Ne.Fit()  # fit
    plot_Ne.set_ydata(Fit_Ne.fit)# plot
    plot_Ne_cursor.set_xdata(Fit_Ne.posx)# plot
    plot_Ne_cursor.set_ydata(Fit_Ne.posy)# plot

    # Calculate Vp and Ise, its the intersection between the fit for te
    # and the fit on the electron saturation current.
    iV_p =  (np.abs(Fit_Ne.fit-np.exp(Fit_Te.fit))).argmin()
    V_p = x[iV_p] # plasma potential
    I_se = y[iV_p] #electron saturation current
    # change the value in the text boxes
    Text_Te.set_val("{0:.2f}".format(round(Fit_Te.Te,2)))
    Text_Vp.set_val("{0:.2f}".format(round(V_p,2)))
    Text_Ise.set_val("{0:.2e}".format((I_se)))

    fig.canvas.draw_idle()
spos1.on_changed(update)
spos2.on_changed(update)
spos3.on_changed(update)
spos4.on_changed(update)
spos5.on_changed(update)
spos6.on_changed(update)

plt.show()
