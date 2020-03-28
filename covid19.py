import os
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
             'Australia',
             'Germany']

vis = 32 # Plot last 'vis' days (default=40)
dpi = 100 # PNG image saving dpi

today = date.today()
datet = today.strftime("%Y-%m-%d")
print('Building plots for %s'%(datet))

print('Data downloaded from the European Centre for Disease Prevention and Control')
# Updated link since 2020-03-27 by the ECDPC
url = 'https://opendata.ecdc.europa.eu/covid19/casedistribution/csv'

if not path.exists('data/'+datet+'.csv'):
    wget.download(url, out='data/')
    os.rename('data/csv', 'data/'+datet+'.csv')
    print('')

data = {}
for country in countries:
    dates = []
    cases = []
    deaths = []
    data[country] = {}
    with open('data/'+datet+'.csv', "rt", encoding="iso-8859-2") as csv_file:
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

