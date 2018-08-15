# Langmuir_probe_interactive

This code is for real-time analysis and visualization of Langmuir probe curves.

The function shows 

- Raw data (Total current vs tension) in absolute value for a semiLog display (blue)

- Linear fit on the ion saturation current (red)

- Electron current (Total current - Ion current) (light blue)

- Fit on the linear part of the electron current which have a slope of 1/Te (yellow)

- A fit on the electron saturation current. The interception between this fit and the one for Te give the plasma potention (Vp) and the electron saturation current (Ise) (green)


<img width="627" alt="screen shot 2018-08-14 at 11 23 07 pm" src="https://user-images.githubusercontent.com/33142211/44129941-0df893e0-a019-11e8-8a93-f3b18349ce88.png">



The main idea behind this program is to change the upper and lower bound of all the Fits (with thoses sliders) and see the direct effect on the extracted parameters such as Te.
