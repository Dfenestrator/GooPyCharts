# GooPyCharts
A Google Charts API for Python 2 and 3, meant to be used as an alternative to matplotlib. Syntax is similar to MATLAB. The goal of this project is to make an easy to use graphing utility for the most common graphical use cases.

## Python (Web Browser) Screenshot

![Alt text](assets/testGraphOutput.JPG?raw=true "Python example")

## Jupyter Screenshot

![Alt text](assets/Sample\ Jupyter\ graph.png?raw=true "Jupyter example")

You can find a Jupyter notebook with examples [here](examples/gpcharts%20test.ipynb). A Python script with examples can be found [here](examples/testGraph.py).

## Installation and use
GooPyCharts can be installed with pip using the following command:

```
pip install gpcharts
```

Alternately, you can put gpcharts.py in your working directory or library path. Then, import gpcharts to your Python code:

```
from gpcharts import figure
```

That's it. To get started, you can plot and display a simple graph with the following code:

```
fig1 = figure()
fig1.plot([8,7,6,5,4])
```

This will open the chart in a Jupyter notebook if you're using one. If you aren't, it will open a webpage in your default browser with the plot.

For more examples, see [testGraph.py](examples/testGraph.py). Examples include scatter plots, adding titles/plot labels, and datetime graphs. For simple bar and histogram examples, see [testGraph_barAndHist.py](examples/testGraph_barAndHist.py). For a jupyter notebook example, see [gpcharts test.ipynb](examples/gpcharts%20test.ipynb). The example does not display properly in Github, but the file should work if you download it and then do "Cell->Run All."

For timeseries, use as your x-axis the following format (as a string): 'yyyy-mm-dd HH:MM:SS'. The 'HH:MM:SS' is optional, but be consistent throughout your input. GooPyCharts will take care of the rest.

Each kind of chart has a number of possible configuration options provided by the Google Chart API and GooPyCharts allows you to use any combination of them via keywork arguments. For example, to show a line chart without a legend and with straight lines between each of the po, you can write:

```
f1 = figure()
f1.plot([1,2], legend="'none'", curveType="'straight'")
```

You can determine the name of the keyword arguments by consulting the [Google Charts API documentation](https://developers.google.com/chart/interactive/docs/customizing_charts) for each chart, such as the [Line Chart](https://developers.google.com/chart/interactive/docs/gallery/linechart#configuration-options). You'll notice that the example strings above are surrounded by single quotes. You are injecting a literal JavaScript option into the chart, so the final drawChart method will have single quotes around the option. This can be somewhat inconvenient, but it is necessary because certain options require dictionaries.

You can use these customization features to overwrite the default options within GooPyCharts. The default GooPyCharts curveType is `'function'`, which produces curved lines, but the example above replaces that with the Google Charts API default, which is not curved.

## Features
- line, scatter, bar, column, and histogram plots
- plot multiple columns in one call
- tooltips
- easy access to best fit line for scatter plots
- full access to the charts' configuration options
- save figure as HTML or PNG
- save data to CSV
- zooming (click and drag to zoom, right-click to reset zoom)
- log scale for y-axis
- automatic datetime/string/numeric detection on x-axis input (a huge pain point in both MATLAB and matplotlib)
- Easy webpage integration (just copy and paste the HTML/Javascript from the output HTML file)
    - To get the HTML in code, cast a `figure` object to `str`. The
      `figure.get_drawChart` method returns just the JavaScript function that
      draws the chart.
- Jupyter notebook integration

## Some Rules
- Headers are column titles. The dependent variable header will be the title of the x axis, and the other headers will appear in the legend.
- If you have headers on your dependent variables, make sure to also have a header on the independent variable.
- The header on the x axis will overwrite the x label. The y label is independent and is not assigned any header.
- If you want to do some fancy math using NumPy and then plot a NumPy array, use the tolist() function to convert the array to a Python list.

## Comparisons to Matplotlib and MATLAB
See the README's [compareToMatplotlib.md](assets/compareToMatplotlib.md) and [compareToMATLAB.md](assets/compareToMATLAB.md).

Please report bugs to me and I'll do my best to fix them in short order.
