##
# Copyright 2016 Sagnik Ghosh, licensed under the Apache 2.0 License.
#
# GooPyCharts: an interface between Python and Google Charts API. Written to serve as a simple substitute
# for matplotlib. Syntax is similar to MATLAB figures.
##

# Python3 compatibility
import sys
python_version = sys.version_info[0]
if python_version >= 3:
    try:
        from past.builtins import xrange
    except ImportError:
        print("past module not installed. Run `pip install future` for GooPyCharts's Python3 compatibility.")
        sys.exit()

# Module's meat begins
from _templates import * #All the JavaScript graph templates
from os import path
import webbrowser
try:
    from IPython.core.display import display, HTML, display_html, display_javascript
except ImportError:
    pass

#helper function to determine template type
def templateType(xdata):
    #check if x axis is numeric, string, or datetime
    if type(xdata[1]) is str:
        #check if first 4 characters of xdata is a valid year
        if len(xdata[1]) == 19 and int(xdata[1][:4]) > 0 and int(xdata[1][:4]) < 3000:
            #the x-axis data looks like it's a datetime! use datetime template
            return graphPgTemplateStart+graphPgTemplate_dateTime+graphPgTemplateEnd
        else:
            #the x-axis data is a string; process as such
            return graphPgTemplateStart+graphPgTemplate_string+graphPgTemplateEnd
    else:
        #otherwise, data is simply numeric
        return graphPgTemplateStart+graphPgTemplate_numeric+graphPgTemplateEnd

#helper function to combine data
def combineData(xdata,ydata,xlabel):
    #if ydata is a simple vector, encapsulate it into a 2D list
    if type(ydata[1]) is not list:
        ydata = [[val] for val in ydata]

    #if xdata is time data, add HH:MM:SS if it is missing (just 00:00:00)
    if type(xdata[1]) is str:
        #check if first 4 characters of xdata is a valid year
        if len(xdata[1]) == 10 and int(xdata[1][:4]) > 0 and int(xdata[1][:4]) < 3000:
            xdata[1:] = [val+' 00:00:00' for val in xdata[1:]]

    #figure out independent variable headers
    # if there is a title row, use that title
    if type(ydata[0][0]) is str:
        data = [[xdata[0]] + ydata[0]]
        for i in xrange(1,len(xdata)):
            data.append([xdata[i]]+ydata[i])
    # otherwise, use a default labeling
    else:
        header = [xlabel]
        for i in xrange(len(ydata[0])):
            header.append('data'+str(i+1))

        data = [header]
        for i in xrange(len(xdata)):
            data.append([xdata[i]]+ydata[i])
    
    return data

##main class
class figure:
    '''GooPyCharts: a simple plotting tool for Python/Jupyter. See https://github.com/Dfenestrator/GooPyCharts for overview and examples.'''

    numFig = 1

    def __init__(self,title="Fig",xlabel='',ylabel='',height=600,width=1000):
        #set figure number, and increment for each instance
        self.figNum = figure.numFig
        figure.numFig = figure.numFig + 1

        #if title has not been changed, add figure number
        if title=="Fig":
            self.title = title+str(self.figNum)
        else:
            self.title = title

        self.fname = self.title+'.html'

        self.xlabel = xlabel
        self.ylabel = ylabel
        #for sizing plot
        self.height = height
        self.width = width

        #Set by the chart methods, can be printed out or exported to file.
        self.javascript = 'No chart created yet. Use a chart method'

    def __str__(self):
        return self.javascript

    #Write the JavaScript text out to file
    def write(self):
        with open(self.fname,'w') as f:
            f.write(self.javascript)

    #display HTML helper method. Trys nb() first, falls back on wb() if no notebook
    #the nb parameter has been deprecated and does nothing.
    def dispFile(self, nb=None):
        try:
            self.nb()
        except:
            self.wb()

    #Displays in a Jupyter notebook. Writes current data first.
    def nb(self):
        self.write()
        display(HTML(self.fname))

    #Displays in a web browser. Writes current data first.
    def wb(self):
        self.write()
        webbrowser.open_new(self.fname)

    #typical line chart plot
    def plot(self,xdata,ydata=[],logScale=False,nb=False):
        '''Graphs a line plot.
        
        xdata: list of independent variable data. Can optionally include a header, see testGraph.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of dependent variable data. Can be multidimensional. If xdata includes a header, include a header list on ydata as well.
        logScale: set to True to set the y axis to log scale.
        nb: for embedded plotting in notebooks. Recommended to use 'plot_nb' instead of setting this manually.
        '''
        
        #combine data into proper format
        #check if only 1 vector was sent, then plot against a count
        if ydata:
            data = combineData(xdata,ydata,self.xlabel)
        else:
            data = combineData(range(len(xdata)),xdata,self.xlabel)

        #determine log scale parameter
        if logScale:
            logScaleStr = 'true'
        else:
            logScaleStr = 'false'

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data': str(data),
                    'title': self.title,
                    'height': self.height,
                    'width': self.width,
                    'logScaleFlag': logScaleStr,
                    'ylabel': self.ylabel,
                    'trendLineStr': '',
                    'plotType': 'LineChart',
                    'numFig': self.numFig}

        self.javascript = (templateType(xdata) % argDict)
        
        if nb:
            self.dispFile()
        
    #scatter plot
    def scatter(self,xdata,ydata=[],trendline=False,nb=False):
        '''Graphs a scatter plot.
        
        xdata: list of independent variable data. Can optionally include a header, see testGraph.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of dependent variable data. Can be multidimensional. If xdata includes a header, include a header list on ydata as well.
        trendline: set to True to plot a linear regression trend line through the first dependend variable.
        nb: for embedded plotting in notebooks. Recommended to use 'scatter_nb' instead of setting this manually.
        '''

        #combine data into proper format
        #check if only 1 vector was sent, then plot against a count
        if ydata:
            data = combineData(xdata,ydata,self.xlabel)
        else:
            data = combineData(range(len(xdata)),xdata,self.xlabel)

        #insert trend line, if flag is set
        if trendline:
            trendLineStr = 'trendlines: { 0: {showR2: true, visibleInLegend: true} }'
        else:
            trendLineStr = ''

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'trendLineStr':trendLineStr,
                    'plotType':'ScatterChart',
                    'numFig':self.numFig}

        self.javascript = (templateType(xdata) % argDict)

        if nb:
            self.dispFile()
            
    #bar chart
    def bar(self,xdata,ydata,nb=False):
        '''Displays a bar graph.
        
        xdata: list of bar graph categories/bins. Can optionally include a header, see testGraph_barAndHist.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of values associated with categories in xdata. If xdata includes a header, include a header list on ydata as well.
        nb: for embedded plotting in notebooks. Recommended to use 'bar_nb' instead of setting this manually.
        '''
                
        #combine data into proper format
        data = combineData(xdata,ydata,self.xlabel)

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'trendLineStr':'',
                    'plotType':'BarChart',
                    'numFig':self.numFig}
        self.javascript = (templateType(xdata) % argDict)
        
        if nb:
            self.dispFile()
        
    #column chart
    def column(self,xdata,ydata,nb=False):
        '''Displays a column graph. A bar chart with vertical bars.
        
        xdata: list of column graph categories/bins. Can optionally include a header, see testGraph_barAndHist.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of values associated with categories in xdata. If xdata includes a header, include a header list on ydata as well.
        nb: for embedded plotting in notebooks. Recommended to use 'bar_nb' instead of setting this manually.
        '''
                
        #combine data into proper format
        data = combineData(xdata,ydata,self.xlabel)

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'trendLineStr':'',
                    'plotType':'ColumnChart',
                    'numFig':self.numFig}
        self.javascript = (templateType(xdata) % argDict)

        if nb:
            self.dispFile()
        
    #histogram
    def hist(self,xdata,nb=False):
        '''Graphs a histogram.
        
        xdata: List of values to bin. Can optionally include a header, see testGraph_barAndHist.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        nb: for embedded plotting in notebooks. Recommended to use 'hist_nb' instead of setting this manually.
        '''
                
        #combine data into proper format
        data = [self.xlabel]+xdata

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'trendLineStr':'',
                    'plotType':'Histogram',
                    'numFig':self.numFig}
        self.javascript = ((graphPgTemplateStart+graphPgTemplate_hist+graphPgTemplateEnd) % argDict)

        if nb:
            self.dispFile()
    
    #Jupyter plotting methods
    def plot_nb(self,xdata,ydata=[],logScale=False):
        '''Graphs a line plot and embeds it in a Jupyter notebook. See 'help(figure.plot)' for more info.'''
        self.plot(xdata,ydata,logScale,nb=True)
    
    def scatter_nb(self,xdata,ydata=[],trendline=False):
        '''Graphs a scatter plot and embeds it in a Jupyter notebook. See 'help(figure.scatter)' for more info.'''
        self.scatter(xdata,ydata,trendline,nb=True)
            
    def bar_nb(self,xdata,ydata):
        '''Displays a bar graph and embeds it in a Jupyter notebook. See 'help(figure.bar)' for more info.'''
        self.bar(xdata,ydata,nb=True)
            
    def hist_nb(self,xdata):
        '''Graphs a histogram and embeds it in a Jupyter notebook. See 'help(figure.hist)' for more info.'''
        self.hist(xdata,nb=True)        

