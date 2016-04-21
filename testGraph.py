import webbrowser
import urllib2

webPgNm = 'testGraph.html'

f = open(webPgNm,'w')

webPg = """
<html>
<head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var dataArr = [
        ['Year', 'Sales', 'Expenses'],
        [2004,  1000,      400],
        [2005,  1170,      460],
        [2006,  660,       1120],
        [2007,  1030,      540]
        ];

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

# f.write(message % str(vals))
vals = [
        ['Year', 'Sales', 'Expenses'],
        ['2004',  1000,      400],
        ['2005',  1170,      460],
        ['2006',  660,       1120],
        ['2007',  1030,      540]
        ]
# f.write(webPg % (vals,"hAxisTitle"))
# f.write(webPg % (vals,"My Graph", "My x", "My y"))
f.write(webPg % ("My Graph", "My x", "My y"))
f.close()

#Change path to reflect file location
filename = webPgNm
webbrowser.open_new(filename)


