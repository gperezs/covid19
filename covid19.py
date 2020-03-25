import sys
import csv
import wget
import numpy as np
from os import path
from datetime import datetime, date
from utils import div0, build_plot

# Countries to plot
countries = ['Colombia',
             'Spain',
             'Italy',
             'France',
             'United_States_of_America',
             'United_Kingdom',
             'China']

vis = 32 # Plot last 'vis' days (default=40)
dpi = 100 # PNG image saving dpi

today = date.today()
date = today.strftime("%Y-%m-%d")
print('Building plots for %s'%(date))

print('Data downloaded from the European Centre for Disease Prevention and Control')
url = 'https://www.ecdc.europa.eu/sites/default/files/documents/COVID-19-geographic-disbtribution-worldwide-' + date + '.csv'

if not path.exists('data/'+url.split('/')[-1]):
    wget.download(url, out='data/')
    print('')

data = {}
for country in countries:
    dates = []
    cases = []
    deaths = []
    data[country] = {}
    with open('data/'+url.split('/')[-1]) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if country == row[6]:
                date = datetime.strptime(row[0],'%d/%m/%Y')
                dates.append(date.strftime('%m/%d/%Y'))
                cases.append(row[4])
                deaths.append(row[5])
        data[country]['DATE'] = dates[::-1]
        data[country]['CUM_CASES'] = np.cumsum([int(ns) for ns in cases[::-1]])
        data[country]['CUM_DEATHS'] = np.cumsum([int(ns) for ns in deaths[::-1]])

build_plot(data, countries, 'Cases', vis, dpi)
build_plot(data, countries, 'Deaths', vis, dpi)
build_plot(data, countries, 'Mortality', vis, dpi)
print('Done!')

