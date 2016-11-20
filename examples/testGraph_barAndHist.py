from gpcharts import figure

#bar graph
fig1 = figure('Percent Alcohol Consumption')
fig1.bar(['Percentage','Beer','Wine','Liquor'],['Type',40,50,10])

#histogram
fig2 = figure('Distribution',xlabel='value')
fig2.hist([1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,3,3,3,3,4,4,5,6,7,8,8,8,8,8,9,9,9,10,11,12,13,13,13,13,14])
