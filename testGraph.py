import webbrowser
from gpcharts import gpchart

vals = [
        ['Year', 'Sales', 'Expenses'],
        [2004,  1000,      400],
        [2005,  1170,      460],
        [2006,  660,       1120],
        [2007,  1030,      540]
        ]

fig1 = gpchart("My Graph","my X","my Y")
fig1.plot(vals)

fig2 = gpchart()
fig2.plot(vals)
