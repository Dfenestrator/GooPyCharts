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

This will open a webpage in your default browser with the plot. For more examples, see testGraph.py. Examples include scatter plots, adding titles/plot labels, and datetime graphs. For simple bar and histogram examples, see testGraph_barAndHist.py.

For timeseries, use as your x-axis the following format (as a string): 'yyyy-mm-dd HH:MM:SS'. The 'HH:MM:SS' is optional, but be consistent throughout your input. GooPyCharts will take care of the rest.

## Features
- line, scatter, bar, and histogram plots
- plot multiple columns in one call
- tooltips
- best fit line for scatter plots
- save figure as HTML or PNG
- save data to CSV
- zooming (click and drag to zoom, right-click to reset zoom)
- log scale for y-axis
- automatic datetime/string/numeric detection on x-axis input (a huge pain point in both MATLAB and matplotlib)
- Easy webpage integration (just copy and paste the HTML/Javascript from the output HTML file)

## Some Rules
- Headers are column titles. The dependent variable header will be the title of the x axis, and the other headers will appear in the legend.
- If you have headers on your dependent variables, make sure to also have a header on the independent variable.
- The header on the x axis will supercede the x label. This is not true for the y label.

## Comparisons to Matplotlib and MATLAB
See the readme's compareToMatplotlib.md and compareToMatlab.md.

Please report bugs to me and I'll do my best to fix them in short order.
