import pandas as pd

url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_cases = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

def get_data(url, sheet):
    # Get raw data from John Hopkins Github
    raw = pd.read_csv(url)
    raw.rename({'Country/Region': 'Country', 'Province/State': 'Province'}, axis=1, inplace=True)  # Better names

    # Create dataframe compressing country regions i.e. to produce one number per country
    cumul_unsort = raw.iloc[:, 4:].groupby(raw.Country).sum()  # cumulative, unsorted
    cumul_unsort.loc['World', :] = cumul_unsort.sum(axis=0)  # cumulative + world total
    cumul = cumul_unsort.sort_values(by=cumul_unsort.columns[-1], ascending=False)  # cumulative, sorted
    daily = cumul.diff(axis=1)  # daily, sorted
    daily['1/22/20'] = cumul['1/22/20'].values  # daily + first day (removed during diff)

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(sheet, engine='xlsxwriter')

    # Write each dataframe to a different worksheet.
    raw.to_excel(writer, sheet_name='raw')
    cumul.to_excel(writer, sheet_name='cumulative')
    daily.to_excel(writer, sheet_name='daily')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

get_data(url_cases, 'cases.xlsx')
get_data(url_deaths, 'deaths.xlsx')