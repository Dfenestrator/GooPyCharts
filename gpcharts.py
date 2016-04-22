##
# Copyright 2016 Sagnik Ghosh, licensed under the Apache 2.0 License.
#
# GooPyCharts: an interface between Python and Google Charts API. Written to serve as a simple substitute
# for matplotlib. Syntax is similar to MATLAB figures.
##

import webbrowser

#The webpage templates. One each for numeric, datetime, and string as the independent variable.
#Compressed the start and end of the template into 1 string to shorten number of lines of code.
graphPgTemplateStart = """
<html>
<head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var dataArr = %s;
        var grTitle = '%s';
        var width = %d;
        var height = %d;
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
            vAxis: { title: '%s' },
            %s
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
            vAxis: { title: '%s' },
            %s
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
            vAxis: { title: '%s' },
            %s
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
            vAxis: { title: '%s' },
            %s
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
        var chart = new google.visualization.%s(document.getElementById('chart_div'));

        chart.draw(data, options);
        document.getElementById('pic_div').innerHTML = '<a href="' + chart.getImageURI() + '" download="'+grTitle+'.png">Download Figure</a>'
        document.getElementById('csvFileDl').innerHTML = '<a href="' + encodeURI(csvOut) + '" download="'+grTitle+'.csv">Download CSV</a>'
    }
    </script>
</head>
<body>
    <div id="chart_div"></div>
    <div id="pic_div"></div>
    <div id="csvFileDl"></div>
</body>
</html>
"""

#helper function to determine template type
def templateType(xdata):
    #check if x axis is numeric, string, or datetime
    if type(xdata[1]) is str:
        #check if first 4 characters of xdata is a valid year
        if len(xdata[1]) == 19 and int(xdata[1][0:3]) > 0 and int(xdata[1][0:3]) < 3000:
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
    if type(ydata[1]) is int:
        ydata = [[val] for val in ydata]

    #if xdata is time data, add HH:MM:SS if it is missing (just 00:00:00)
    if type(xdata[1]) is str:
        #check if first 4 characters of xdata is a valid year
        if len(xdata[1]) == 10 and int(xdata[1][0:3]) > 0 and int(xdata[1][0:3]) < 3000:
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
   numFigs = 1

   def __init__(self,title="Fig",xlabel='',ylabel='',height=1000,width=600):
      #set figure number, and increment for each instance
      self.figNum = figure.numFigs
      figure.numFigs = figure.numFigs + 1

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

   #typical line chart plot
   def plot(self,xdata,ydata):
      f = open(self.fname,'w')
    
      #combine data into proper format
      data = combineData(xdata,ydata,self.xlabel)

      #input argument format to template is: data, title, y label, trendline/additional options, chart type
      f.write(templateType(xdata) % 
              (str(data),self.title,self.height,self.width,self.ylabel,'','LineChart'))
      f.close()

      webbrowser.open_new(self.fname)

   #scatter plot
   def scatter(self,xdata,ydata,trendline=False):
      f = open(self.fname,'w')

      #combine data into proper format
      data = combineData(xdata,ydata,self.xlabel)

      #insert trend line, if flag is set
      if trendline:
         trendLineStr = 'trendlines: { 0: {} }'
      else:
         trendLineStr = ''

      #input argument format to template is: data, title, y label, trendline/additional options, chart type
      f.write(templateType(xdata) % 
              (str(data),self.title,self.height,self.width,self.ylabel,trendLineStr,'ScatterChart'))
      f.close()

      webbrowser.open_new(self.fname)
   
   #bar chart
   def bar(self,xdata,ydata):
      f = open(self.fname,'w')
    
      #combine data into proper format
      data = combineData(xdata,ydata,self.xlabel)

      #input argument format to template is: data, title, y label, trendline/additional options, chart type
      f.write(templateType(xdata) % 
              (str(data),self.title,self.height,self.width,self.ylabel,'','BarChart'))
      f.close()

      webbrowser.open_new(self.fname)

   #histogram
   def hist(self,xdata):
      f = open(self.fname,'w')
    
      #combine data into proper format
      data = [self.xlabel]+xdata

      #input argument format to template is: data, title, y label, trendline/additional options, chart type
      f.write((graphPgTemplateStart+graphPgTemplate_hist+graphPgTemplateEnd) % 
              (str(data),self.title,self.height,self.width,self.ylabel,'','Histogram'))
      f.close()

      webbrowser.open_new(self.fname)

