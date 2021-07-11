import csv
import os

inputpath = os.path.join('', 'Resources', 'election_data.csv')
totalvotes = 0
khantotal = 0
correytotal = 0
litotal = 0
otooleytotal = 0
candidates = []
candidatevotes = []
placeholder = 0

with open(inputpath) as electiondata:
    csv_header = next(electiondata)
    voter = csv.reader(electiondata, delimiter=',')
    for row in voter:
        totalvotes += 1
        if row[2] not in candidates:
            candidates.append(row[2])
            candidatevotes.append(0)
    electiondata.seek(0)

    for row in voter:
        if row[2] in candidates:
            placeholder = (candidates.index(row[2]))
            candidatevotes[placeholder] = candidatevotes[placeholder] + 1

electiondata.close()
winner = {"name": 'None', "winningvotes": 0 }
x = 0

while x < len(candidates):
    if winner["winningvotes"] < candidatevotes[x]:
        winner["name"] = candidates[x]
        winner["winningvotes"] = candidatevotes[x]
    x += 1

message = ['Election Results', '-----------------------------', f'Total Votes: {totalvotes}',
           '-----------------------------']

x = 0
while x < len(candidates):
    message.append(f'{candidates[x]}: {format(candidatevotes[x]/totalvotes*100,".3f")}% ({candidatevotes[x]})')
    x += 1
message.append('-----------------------------')
message.append(f'Winner {winner["name"]}')

outputpath = os.path.join('', 'Analysis', 'analysis.txt')


with open(outputpath, 'w', newline='\n') as analysisfile:

    for stat in message:
        print(stat)
        analysisfile.write(stat + '\n')

analysisfile.close()
