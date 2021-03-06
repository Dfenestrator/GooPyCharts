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
from os import path
from warnings import warn
import webbrowser
import re
try:
    from IPython.core.display import display, HTML, display_html, display_javascript
except ImportError:
    pass

#The webpage templates. One each for numeric, datetime, and string as the independent variable.
#Compressed the start and end of the template into 1 string to shorten number of lines of code.
graphPgTemplateStart = """
<html>
<head>
    <script src="https://code.jquery.com/jquery-1.10.2.js"></script>
    <script type="text/javascript">
    $.getScript( "https://www.gstatic.com/charts/loader.js", function() {
      if ((typeof google === 'undefined') || (typeof google.visualization === 'undefined')) 
      {
         google.charts.load('current', {'packages':['corechart']});
      }

      google.charts.setOnLoadCallback(drawChart%(functionName)s);
    });
    
    function drawChart%(functionName)s() {
        var dataArr = %(data)s;
        var grTitle = '%(title)s';
        var height = %(height)d;
        var width = %(width)d;
        var logScaleFlag = %(logScaleFlag)s;
        var vAxisTitle = '%(ylabel)s';
        var vAxisOpt;
        if(logScaleFlag)
        {
            vAxisOpt = { title: vAxisTitle, logScale: true, format: 'scientific'};
        }
        else
        {
            vAxisOpt = { title: vAxisTitle };
        }
"""

graphPgTemplate_numeric = """
        var options = {
            width: width,
            height: height,
            explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: 0.01 },
            curveType: 'function',
            title: grTitle,
            titleTextStyle: { fontSize: 18, bold: true },
            hAxis: { title: dataArr[0][0] },
            vAxis: vAxisOpt,
            %(other)s
        };

        var data = new google.visualization.DataTable();
        var csvOut = "data:text/csv;charset=utf-8";
        // Add column headers
        for (var j = 0; j < dataArr[0].length; j++)
        {
            data.addColumn('number',dataArr[0][j]);
            csvOut += ',' + dataArr[0][j];
        }
        csvOut += '\\n';

        // Add columns
        for (var i = 1; i < dataArr.length; i++)
        {
            data.addRow(dataArr[i]);
            csvOut += dataArr[i].join(",") + '\\n';
        }
"""

graphPgTemplate_string = """
        var options = {
            width: width,
            height: height,
            explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: 0.01 },
            curveType: 'function',
            title: grTitle,
            titleTextStyle: { fontSize: 18, bold: true },
            hAxis: { title: dataArr[0][0] },
            vAxis: vAxisOpt,
            %(other)s
        };

        var data = new google.visualization.DataTable();
        var csvOut = "data:text/csv;charset=utf-8";
        // Add column headers
        data.addColumn('string',dataArr[0][0]);
        csvOut += ',' + dataArr[0][0];
        for (var j = 0; j < dataArr[0].length-1; j++)
        {
           data.addColumn('number',dataArr[0][j+1]);
           csvOut += ',' + dataArr[0][j+1];
        }
        csvOut += '\\n';

        // Add columns
        for (var i = 1; i < dataArr.length; i++)
        {
            data.addRow(dataArr[i]);
            csvOut += dataArr[i].join(",") + '\\n';
        }
"""

graphPgTemplate_dateTime = """
        var options = {
            width: width,
            height: height,
            explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: 0.01 },
            curveType: 'function',
            title: grTitle,
            titleTextStyle: { fontSize: 18, bold: true },
            hAxis: { title: dataArr[0][0],
               "gridlines": {
                  "count": -1,
                  "units": {
                  "minutes": { "format": [ "HH:mm", "mm" ] },
                  "hours": { "format": [ "MM/dd HH:mm", "HH" ] },
                  "days": { "format": [ "MM/dd" ] },
                  }
               },
               "minorGridlines": {
                  "count": -1,
                  "units": {
                  "minutes": { "format": [ "HH:mm", "mm" ] },
                  "hours": { "format": [ "MM/dd HH:mm", "HH" ] },
                  "days": { "format": [ "MM/dd" ] },
                  }
               },
            },
            vAxis: vAxisOpt,
            %(other)s
         };

         var data = new google.visualization.DataTable();
         var csvOut = "data:text/csv;charset=utf-8";
         // Add column headers
         data.addColumn('date',dataArr[0][0]);
         csvOut += ',' + dataArr[0][0];
         for (var j = 0; j < dataArr[0].length-1; j++)
         {
            data.addColumn('number',dataArr[0][j+1]);
            csvOut += ',' + dataArr[0][j+1];
         }
         csvOut += '\\n';

         var tmpArr;
         // Add columns
         for (var i = 0; i < dataArr.length-1; i++)
         {
            // Add time data
            tempStr = dataArr[i+1][0];
            year = parseInt(tempStr.substr(0,4));
            month = parseInt(tempStr.substr(5,2))-1;
            day = parseInt(tempStr.substr(8,2));
            hour = parseInt(tempStr.substr(11,2));
            minute = parseInt(tempStr.substr(14,2));
            second = parseInt(tempStr.substr(17,2));
            tmpArr = [new Date(year,month,day,hour,minute,second)];

            data.addRow(tmpArr.concat(dataArr[i+1].slice(1,dataArr[i+1].length)));
            csvOut += tempStr + ',' + dataArr[i+1].slice(1,dataArr[i+1].length).join(",") + '\\n';
        }
"""

graphPgTemplate_hist = """
        var options = {
            width: width,
            height: height,
            title: grTitle,
            titleTextStyle: { fontSize: 18, bold: true },
            hAxis: { title: dataArr[0]},
            vAxis: vAxisOpt,
            %(other)s
        };

        var data = new google.visualization.DataTable();
        var csvOut = "data:text/csv;charset=utf-8";
        // Add column header
        data.addColumn('number',dataArr[0]);
        csvOut += ',' + dataArr[0];
        csvOut += '\\n';

        // Add data
        for (var i = 1; i < dataArr.length; i++)
        {
            data.addRow([dataArr[i]]);
            csvOut += dataArr[i].toString()+'\\n';
        }
"""

graphPgTemplateEnd = """
        var chart = new google.visualization.%(plotType)s(document.getElementById('chart_div%(functionName)s'));

        chart.draw(data, options);
        document.getElementById('pic_div%(functionName)s').innerHTML = '<a href="' + chart.getImageURI() + '" download="'+grTitle+'.png">Download Figure</a>'
        document.getElementById('csvFileDl%(functionName)s').innerHTML = '<a href="' + encodeURI(csvOut) + '" download="'+grTitle+'.csv">Download CSV</a>'
    }
    </script>
</head>
<body>
    <div id="chart_div%(functionName)s"></div>
    <div id="pic_div%(functionName)s"></div>
    <div id="csvFileDl%(functionName)s"></div>
</body>
</html>
"""

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

#helper function, returns title as a valid JS identifier, prefixed by '_'.
def slugify(title):
    return '_' + re.sub('[^\w\d_]', '_', title) #Make valid JS identifier

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

    # Get the full HTML of the file.
    def __str__(self):
        return self.javascript

    # Returns the drawFigure function from the JavaScript in its entirety.
    def get_drawChart(self):
        tabwidth = 4

        start = self.javascript.find('function drawChart') - tabwidth
        end = self.javascript.find('</head>') - len('</script>') - 1
        raw_drawChart = self.javascript[start:end]

        #Unindent 4 spaces on all lines
        final_drawChart = ''
        for line in raw_drawChart.split('\n'):
            final_drawChart += line[tabwidth:] + '\n'

        final_drawChart = final_drawChart.rstrip()
        return final_drawChart

    #Write the JavaScript text out to file
    def write(self):
        with open(self.fname,'w') as f:
            f.write(self.javascript)

    #display HTML helper method. Trys nb() first, falls back on wb() if no notebook
    #the nb parameter has been deprecated and does nothing.
    def dispFile(self, nb=None):
        if nb is not None:
            warn('dispFile() nb paraneter is deprecated and does nothing.',
                    DeprecationWarning)
        try:
            self.nb()
        except NameError:
            self.wb()

    #Alias for dispFile()
    def show(self):
        self.dispFile()

    #Displays in a Jupyter notebook. Writes current data first.
    def nb(self):
        self.write()
        display(HTML(self.fname))

    #Displays in a web browser. Writes current data first.
    def wb(self):
        self.write()
        webbrowser.open_new(self.fname)

    #typical line chart plot
    def plot(self,xdata,ydata=[],logScale=False,disp=True,**kwargs):
        '''Graphs a line plot.
        
        xdata: list of independent variable data. Can optionally include a header, see testGraph.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of dependent variable data. Can be multidimensional. If xdata includes a header, include a header list on ydata as well.
        logScale: set to True to set the y axis to log scale.
        disp: for displaying plots immediately. Set to True by default. Set to False for other operations, then use show() to display the plot.
        **kwargs: Access to other Google Charts API options. The key is the option name, the value is the option's full JS code.
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

        #Include other options, supplied by **kwargs
        other = ''

        for option in kwargs:
            other += option + ': ' + kwargs[option] + ',\n'

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data': str(data),
                    'title':self.title,
                    'functionName':slugify(self.title),
                    'height': self.height,
                    'width': self.width,
                    'logScaleFlag': logScaleStr,
                    'ylabel': self.ylabel,
                    'plotType': 'LineChart',
                    'numFig': self.numFig,
                    'other': other}

        self.javascript = templateType(xdata) % argDict
        
        if disp:
            self.dispFile()
        
    #scatter plot
    def scatter(self,xdata,ydata=[],trendline=False,disp=True,**kwargs):
        '''Graphs a scatter plot.
        
        xdata: list of independent variable data. Can optionally include a header, see testGraph.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of dependent variable data. Can be multidimensional. If xdata includes a header, include a header list on ydata as well.
        trendline: set to True to plot a linear regression trend line through the first dependend variable.
        disp: for displaying plots immediately. Set to True by default. Set to False for other operations, then use show() to display the plot.
        **kwargs: Access to other Google Charts API options. The key is the option name, the value is the option's full JS code.
        '''

        #combine data into proper format
        #check if only 1 vector was sent, then plot against a count
        if ydata:
            data = combineData(xdata,ydata,self.xlabel)
        else:
            data = combineData(range(len(xdata)),xdata,self.xlabel)

        #Include other options, supplied by **kwargs
        other = ''

        #insert trend line, if flag is set
        if trendline:
            other = 'trendlines: { 0: {showR2: true, visibleInLegend: true} },\n'

        for option in kwargs:
            other += option + ': ' + kwargs[option] + ',\n'

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'functionName':slugify(self.title),
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'plotType':'ScatterChart',
                    'numFig':self.numFig,
                    'other':other}

        self.javascript = templateType(xdata) % argDict

        if disp:
            self.dispFile()
            
    #bar chart
    def bar(self,xdata,ydata,disp=True,**kwargs):
        '''Displays a bar graph.
        
        xdata: list of bar graph categories/bins. Can optionally include a header, see testGraph_barAndHist.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of values associated with categories in xdata. If xdata includes a header, include a header list on ydata as well.
        disp: for displaying plots immediately. Set to True by default. Set to False for other operations, then use show() to display the plot.
        **kwargs: Access to other Google Charts API options. The key is the option name, the value is the option's full JS code.
        '''
                
        #combine data into proper format
        data = combineData(xdata,ydata,self.xlabel)

        #Include other options, supplied by **kwargs
        other = ''

        for option in kwargs:
            other += option + ': ' + kwargs[option] + ',\n'

        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'functionName':slugify(self.title),
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'plotType':'BarChart',
                    'numFig':self.numFig,
                    'other':other}

        self.javascript = templateType(xdata) % argDict
        
        if disp:
            self.dispFile()
        
    #column chart
    def column(self,xdata,ydata,disp=True,**kwargs):
        '''Displays a column graph. A bar chart with vertical bars.
        
        xdata: list of column graph categories/bins. Can optionally include a header, see testGraph_barAndHist.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        ydata: list of values associated with categories in xdata. If xdata includes a header, include a header list on ydata as well.
        disp: for displaying plots immediately. Set to True by default. Set to False for other operations, then use show() to display the plot.
        **kwargs: Access to other Google Charts API options. The key is the option name, the value is the option's full JS code.
        '''
                
        #combine data into proper format
        data = combineData(xdata,ydata,self.xlabel)

        #Include other options, supplied by **kwargs
        other = ''

        for option in kwargs:
            other += option + ': ' + kwargs[option] + ',\n'
            
        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'functionName':slugify(self.title),
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'plotType':'ColumnChart',
                    'numFig':self.numFig,
                    'other':other}

        self.javascript = templateType(xdata) % argDict

        if disp:
            self.dispFile()
        
    #histogram
    def hist(self,xdata,disp=True,**kwargs):
        '''Graphs a histogram.
        
        xdata: List of values to bin. Can optionally include a header, see testGraph_barAndHist.py in https://github.com/Dfenestrator/GooPyCharts for an example.
        disp: for displaying plots immediately. Set to True by default. Set to False for other operations, then use show() to display the plot.
        **kwargs: Access to other Google Charts API options. The key is the option name, the value is the option's full JS code.
        '''
                
        #combine data into proper format
        data = [self.xlabel]+xdata

        #Include other options, supplied by **kwargs
        other = ''

        for option in kwargs:
            other += option + ': ' + kwargs[option] + ',\n'
            
        #input argument format to template is in dictionary format (see template for where variables are inserted)
        argDict = { 'data':str(data),
                    'title':self.title,
                    'functionName':slugify(self.title),
                    'height':self.height,
                    'width':self.width,
                    'logScaleFlag':'false',
                    'ylabel':self.ylabel,
                    'plotType':'Histogram',
                    'numFig':self.numFig,
                    'other':other}

        self.javascript = (graphPgTemplateStart+graphPgTemplate_hist+graphPgTemplateEnd) % argDict

        if disp:
            self.dispFile()
    
    #Jupyter plotting methods (depricated; keeping for now for backwards compatibility)
    def plot_nb(self,xdata,ydata=[],logScale=False):
        '''Graphs a line plot and embeds it in a Jupyter notebook. See 'help(figure.plot)' for more info.'''
        self.plot(xdata,ydata,logScale)
    
    def scatter_nb(self,xdata,ydata=[],trendline=False):
        '''Graphs a scatter plot and embeds it in a Jupyter notebook. See 'help(figure.scatter)' for more info.'''
        self.scatter(xdata,ydata,trendline)
            
    def bar_nb(self,xdata,ydata):
        '''Displays a bar graph and embeds it in a Jupyter notebook. See 'help(figure.bar)' for more info.'''
        self.bar(xdata,ydata)

    def column_nb(self,xdata,ydata):
        '''Displays a column graph and embeds it in a Jupyter notebook. See 'help(figure.bar)' for more info.'''
        self.column(xdata,ydata)
            
    def hist_nb(self,xdata):
        '''Graphs a histogram and embeds it in a Jupyter notebook. See 'help(figure.hist)' for more info.'''
        self.hist(xdata)        

