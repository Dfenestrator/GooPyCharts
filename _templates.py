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

      google.charts.setOnLoadCallback(drawChart);
    });
    
    function drawChart_%(title)() {
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
            %(trendLineStr)s
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
            %(trendLineStr)s
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
            %(trendLineStr)s
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
            %(trendLineStr)s
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
        var chart = new
        google.visualization.%(plotType)s(document.getElementById('chart_div_%(title)s'));

        chart.draw(data, options);
        document.getElementById('pic_div_%(title)s').innerHTML = '<a href="' + chart.getImageURI() + '" download="'+grTitle+'.png">Download Figure</a>'
        document.getElementById('csvFileDl_%(title)s').innerHTML = '<a href="' + encodeURI(csvOut) + '" download="'+grTitle+'.csv">Download CSV</a>'
    }
    </script>
</head>
<body>
    <div id="chart_div_%(title)s"></div>
    <div id="pic_div_%(title)s"></div>
    <div id="csvFileDl_%(title)s"></div>
</body>
</html>
"""

