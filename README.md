# GooPyCharts
A Google Charts API for Python, meant to be used as an alternative to matplotlib. Syntax is similar to MATLAB. The goal of this project is to make an easy to use graphing utility for the most common graphical use cases.

## Installation and use
Put gpcharts.py in your working directory or library path and import gpcharts to your Python code:

```
from gpcharts import figure
```

That's it. To get started, you can plot a simple graph with the following code:

```
fig1 = figure()
fig1.plot([1,2,3,4,5],[8,7,6,5,4])
```

This will open a webpage in your default browser with the plot. For more examples, see testGraph.py. Examples include scatter plots, adding titles/plot labels, and datetime graphs.

For timeseries, use as your x-axis the following format (as a string): 'yyyy-mm-dd HH:MM:SS'. GooPyCharts will take care of the rest.

## Features
- line and scatter plots
- plot multiple columns in one call
- tooltips
- best fit line for scatter plots
- save figure as HTML or PNG
- save data to CSV
- zooming (click and drag to zoom, right-click to reset zoom)
- automatic datetime/string/numeric detection on x-axis input (a huge pain point in both MATLAB and matplotlib)

## Comparisons to matplotlib and MATLAB
See the readme's compareToMatplotlib.md and compareToMatlab.md.

Please report bugs to me and I'll do my best to fix them in short order.
