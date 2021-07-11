import os
import csv

inputpath = os.path.join('', 'Resources', 'budget_data.csv')
nettotal = 0
totalmonth = 0
difference = 0
difflist = []
monthlist = []

with open(inputpath) as budgetinfo:

    csv_header = next(budgetinfo)
    budget = csv.reader(budgetinfo, delimiter=',')
    previous_month = 0
    nettotal = 0
    # Read each row of data after the header
    for row in budget:
        nettotal = nettotal + int(row[1])
        if previous_month != 0:
            difflist.append(int(row[1])-int(previous_month))
            monthlist.append(row[0])
        previous_month = row[1]
        totalmonth = totalmonth + 1


decrease = min(difflist)
decreasemonth = monthlist[(difflist.index(decrease))]
increase = max(difflist)
increasemonth = monthlist[(difflist.index(increase))]
average = sum(difflist)/len(difflist)
average = format(average, '.2f')

analysisdata = [f'Total Months: {totalmonth}', f'Total: ${nettotal}', f'Average Change: ${average}',
                f'Greatest Increase in profits: {increasemonth} (${increase})',
                f'Greatest Decrease in profits: {decreasemonth} (${decrease})']

outputpath = os.path.join('', 'Analysis', 'analysis.txt')

with open(outputpath, 'w', newline='\n') as analysisfile:

    for stat in analysisdata:
        print(stat)
        analysisfile.write(stat + '\n')

analysisfile.close()
