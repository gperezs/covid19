import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from matplotlib.dates import datestr2num


def div0(n, d):
    return n / d if d else 0

def build_plot(data, countries, data_type='Not specified', vis=40, dpi=100):
    if data_type == 'Cases':
        threshold = 10000
    elif data_type == 'Deaths':
        threshold = 500
    elif data_type == 'Mortality':
        threshold = 0.025
    countries = countries[::-1]
    myFmt = mdates.DateFormatter('%d-%m-%Y')
    fig, ax = plt.subplots()
    if data_type == 'Mortality':
        for country in countries:
            res = []
            for i, j in zip(data[country]['CUM_DEATHS'], data[country]['CUM_CASES']):
                if j < 100: # To have a representative (?) sample
                    res.append(0)
                else:
                    res.append(div0(i,j))
            ax.plot(mdates.num2date(datestr2num(data[country]['DATE'][-vis:])),res[-vis:],'.-')
    elif data_type == 'Cases':    
        for country in countries:
            ax.plot(mdates.num2date(datestr2num(data[country]['DATE'][-vis:])), 
                    data[country]['CUM_CASES'][-vis:],'.-')
    elif data_type == 'Deaths':
        for country in countries:
            ax.plot(mdates.num2date(datestr2num(data[country]['DATE'][-vis:])), 
                    data[country]['CUM_DEATHS'][-vis:],'.-')
    ax.legend(countries, loc='upper left', shadow=True)
    ax.set_ylabel(data_type)
    ax.set_xticks(mdates.num2date(datestr2num(data['Italy']['DATE'][0::1])))
    ax.grid(True, linestyle='--')
    ax.xaxis.set_major_formatter(myFmt)
    ax.set_facecolor('#ECECEC')
    ax.fill_between(mdates.num2date(datestr2num(data['Italy']['DATE'][-vis:])), 0, 0.025, facecolor='#CCCCCC')
    plt.xticks(rotation=45)
    plt.hlines(y=threshold, xmin=min(mdates.num2date(datestr2num(data['Italy']['DATE'][-vis:]))),
            xmax=max(mdates.num2date(datestr2num(data['Italy']['DATE']))), linestyles='dotted', color='w')
    figure = plt.gcf() # get current figure
    figure.set_size_inches(16, 10)
    filename = 'plots/covid19_' + data_type + '.png'
    plt.savefig(filename, dpi=dpi)
    plt.close()
    print("%s plot saved to file '%s'"%(data_type, filename))

