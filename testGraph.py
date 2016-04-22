from gpcharts import figure

#simple line graph, as described in the readme.
fig1 = figure()
fig1.plot([1,2,3,4,5],[8,7,6,5,4])

#another line graph, but with two data types. Also adding title
fig2 = figure(title='Two lines',xlabel='Days',ylabel='Count')
xVals = ['Mon','Tues','Wed','Thurs','Fri']
yVals = [[5,4],[8,7],[4,8],[10,10],[3,12]]
fig2.plot(xVals,yVals)

#a graph with dates and times. Title is assigned afterwards, and data is given headers
fig3 = figure()
fig3.title = 'Weather over Days'
fig3.ylabel = 'Temperature'

# X data can take either of the following formats: "yyyy-mm-dd HH:MM:SS" or "yyyy-mm-dd" (but be consistent)
#xVals = ['Dates','2016-03-20 00:00:00','2016-03-21 00:00:00','2016-03-25 00:00:00','2016-04-01 00:00:00']
xVals = ['Dates','2016-03-20','2016-03-21','2016-03-25','2016-04-01']
yVals = [['Shakuras','Korhal','Aiur'],[10,30,40],[12,28,41],[15,34,38],[8,33,47]]
fig3.plot(xVals,yVals)

#a simple scatter plot. Putting in trend line, only supported for first y variable for now.
fig4 = figure('Strong Correlation')
fig4.scatter([1,2,3,4,5],[[1,5],[2,4],[3,3],[4,2],[5,1]],trendline=True)
