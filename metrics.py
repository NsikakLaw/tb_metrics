# This is a sample Python script.
import requests
import pandas as pd

pd.options.mode.chained_assignment = None


def weekly_series(date, start_date):
    # Find the week in which a particular date is in specified by the start date
    # For example in this script, the start date is a friday rather than the generic Monday

    start_date = pd.to_datetime(start_date)

    if date < start_date:
        return None
    else:

        while date >= start_date:
            delta = date - start_date

            if delta.days < 7:

                return start_date
            else:
                start_date = start_date + pd.to_timedelta(7, unit='d')


def create_date_df(start, end):
    # create a date dataframe specified by the start and end date of the period.

    df = pd.DataFrame(pd.date_range(start=start, end=end), columns=['date'])

    return df


class HelperFunctions:
    """
    Helper functions to faciliate data download from url

    :param base_url: url of the api service
    :param query_params: query parameters for the url

    """

    def __init__(self, base_url, query_params=None):
        self.base_url = base_url
        self.query_params = query_params
        self.query_url = None

    def create_url(self):

        # creates the url to download the data from the api service

        query_string = "&".join([f"{i}={j}" for i, j in self.query_params.items()])
        query_url = f"{self.base_url}?{query_string}"

        self.query_url = query_url

    def download_csv(self):
        # download the data from url and stores it in data directory
        query_url = self.query_url

        try:
            url_content = requests.get(query_url).content

        except Exception as e:
            print(e)
            return None

        with open('data/covid_data.csv', 'wb') as csv_file:
            csv_file.write(url_content)

        covid_df = pd.read_csv("data/covid_data.csv")
        return covid_df


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    df_date = create_date_df("2020-03-20", "2021-01-01")

    params = {'stat': 'cases', 'geo': 'pt', 'loc': 'ON', 'after': '2020-03-20', 'before': '2021-01-01',
              'fmt': 'csv'}

    url = "https://api.opencovid.ca/timeseries"
    help_f = HelperFunctions(url, params)
    help_f.create_url()

    df_covid = help_f.download_csv()

    if df_covid is None:
        print("CSV Download is Unsuccesful!")
        exit(1)

    df_covid['date'] = pd.to_datetime(df_covid['date'])

    df_restaurant = pd.read_excel("data/data.xlsx", engine='openpyxl', sheet_name='Sample Restaurant Revenue')
    df_ontario = df_restaurant.loc[df_restaurant['Province'] == 'ON']
    df_ontario['Date'] = pd.to_datetime(df_ontario['Date'])

    # merge dataframe to the date_df to get daily cases/revenue per day
    df_covid_date = pd.merge(df_date, df_covid, how='left', left_on='date', right_on='date')
    df_restaurant_date = pd.merge(df_date, df_ontario, how='left', left_on='date', right_on='Date')

    # merge covid data and restaurant data
    df_merged = pd.merge(df_covid_date, df_restaurant_date, how='inner', left_on='date', right_on='date')
    df_merged['First Day of Week'] = df_merged.apply(lambda x: weekly_series(x['date'], '2020-03-20'), axis=1)
    df_merged['Last Day of Week'] = df_merged['First Day of Week'] + pd.to_timedelta(6, unit='d')

    final_df = df_merged.groupby(['First Day of Week', 'Last Day of Week']).agg(
        {'value_daily': ['mean', 'max', 'var', 'min'],
         'Revenue': ['mean', 'max', 'var', 'min']
         })

    rename_cols = {'mean': 'Average', 'min': 'Minimum',
                   'max': 'Maximum', 'var': 'Variance', 'value_daily': 'Covid Cases',
                   'Revenue': 'Restaurant Revenue'}

    # rename columns to give a better look

    final_df.rename(columns=rename_cols, level=1, inplace=True)
    final_df.rename(columns=rename_cols, level=0, inplace=True)

    print(final_df)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
