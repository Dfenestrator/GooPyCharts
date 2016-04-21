import webbrowser
from gpcharts import figure

vals = [
        ['Year', 'Sales', 'Expenses'],
        [2004,  1000,      400],
        [2005,  1170,      460],
        [2006,  660,       1120],
        [2007,  1030,      540]
        ]

fig1 = figure()
fig1.title = "My Graph!"
fig1.plot([val[0] for val in vals],[val[1:] for val in vals])

fig2 = figure()
fig2.scatter([vals[i][0] for i in xrange(1,len(vals))],[vals[i][1:] for i in xrange(1,len(vals))],trendline=True)
