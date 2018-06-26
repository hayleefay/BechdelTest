from bs4 import BeautifulSoup
from urllib.request import urlopen
import csv

url = 'https://www.the-numbers.com/box-office-records/domestic/all-movies/cumulative/released-in-2017'
html = urlopen(url)

soup = BeautifulSoup(html, 'lxml')
tables = soup.findChildren('table')
table = tables[1]
top50 = []

rows = table.findChildren(['th', 'tr'])
i = 0
for row in rows:
    if i > 49:
        break
    cells = row.findChildren(['td'])
    for cell in cells:
        titles = cell.findChildren(['b'])
        for title in titles:
            # print(cell)
            value = title.string
            if 'â\x80\x99s' in value:
                index = value.find('â\x80\x99s')
                value = value[:index] + "'s" + value[index+len('â\x80\x99s'):]
            top50.append(value)
            i += 1

filename = 'top50.csv'
with open(filename, "w") as output:
    writer = csv.writer(output, lineterminator='\n')
    for title in top50:
        writer.writerow([title])
