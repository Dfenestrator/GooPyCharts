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
            hAxis: { title: '%s' },
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

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

        chart.draw(data, options);
    }
    </script>
</head>
<body>
    <div id="curve_chart"></div>
</body>
</html>
"""

class gpchart:
   numFigs = 1

   def __init__(self,title="Fig",xlabel='',ylabel=''):
      self.figNum = gpchart.numFigs
      gpchart.numFigs = gpchart.numFigs + 1

      if title=="Fig":
         self.title = title+str(self.figNum)
      else:
         self.title = title

      self.webPgName = self.title+'.html'

      self.xlabel = xlabel
      self.ylabel = ylabel

   def plot(self,data):
      f = open(self.webPgName,'w')
      f.write(graphPgTemplate % (str(data),self.title,self.xlabel,self.ylabel))
      f.close()

      webbrowser.open_new(self.webPgName)

