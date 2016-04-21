import webbrowser

graphPgTemplate = """
<html>
<head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var dataArr = %s;
        var grTitle = '%s';

        var options = {
            width: 1000,
            height: 600,
            explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: 0.01 },
            curveType: 'function',
            title: grTitle,
            titleTextStyle: { fontSize: 18, bold: true },
            hAxis: { title: dataArr[0][0] },
            vAxis: { title: '%s' },
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

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

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

class figure:
   numFigs = 1

   def __init__(self,title="Fig",xlabel='',ylabel=''):
      self.figNum = figure.numFigs
      figure.numFigs = figure.numFigs + 1

      if title=="Fig":
         self.title = title+str(self.figNum)
      else:
         self.title = title

      self.fname = self.title+'.html'

      self.xlabel = xlabel
      self.ylabel = ylabel

   def plot(self,xdata,ydata):
      f = open(self.fname,'w')

      #figure out independent variable headers
      # if there is a title row, use that title
      if type(ydata[0][0]) is str:
         data = [[xdata[0]] + ydata[0]]
         for i in xrange(1,len(xdata)):
            data.append([xdata[i]]+ydata[i])
      # otherwise, use a default labeling
      else:
         header = [self.xlabel]
         for i in xrange(len(ydata[0])):
            header.append('data'+str(i+1))

         data = [header]
         for i in xrange(len(xdata)):
            data.append([xdata[i]]+ydata[i])

      f.write(graphPgTemplate % (str(data),self.title,self.ylabel))
      f.close()

      webbrowser.open_new(self.fname)

