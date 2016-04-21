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

        var options = {
            width: 1000,
            height: 600,
            explorer: { actions: ['dragToZoom', 'rightClickToReset'], maxZoomIn: 0.01 },
            curveType: 'function',
            title: '%s',
            titleTextStyle: { fontSize: 18, bold: true },
            hAxis: { title: dataArr[0][0] },
            vAxis: { title: '%s' },
        };

        var data = new google.visualization.DataTable();
        // Add column headers
        for (var j = 0; j < dataArr[0].length; j++)
        {
            data.addColumn('number',dataArr[0][j]);
        }

        // Add columns
        for (var i = 1; i < dataArr.length; i++)
        {
            data.addRow(dataArr[i]);
        }

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));

        chart.draw(data, options);
    }
    </script>
</head>
<body>
    <div id="chart_div"></div>
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

