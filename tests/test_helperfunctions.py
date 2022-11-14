from metrics import HelperFunctions, create_date_df, weekly_series
import pytest
import pandas as pd


@pytest.mark.parametrize(
    "url,params,output",
    [
        ("google.com", {'a': 'b', 'c': 'd', 'e': 'f'}, 'google.com?a=b&c=d&e=f'),
        ("facebook.com", {'user': 'james', 'region': 'America'}, 'facebook.com&user=james&region=America')
    ]
)
def test_create_url(url, params, output):
    func = HelperFunctions(url, params)
    func.create_url()

    assert func.query_url == output


@pytest.mark.parametrize(
    "url,output",
    [
        ("https://api.opencovid.ca/timeseries?stat=cases&geo=pt&loc=ON&after=2020-03-20&before=2020-04-21&fmt=csv",
         "<class 'pandas.core.frame.DataFrame'>"),
        ("https://api23.ovid.ca/timeserides?stat=caes&geo=pt&loc=ON&after=2020-03-20&before=2020-04-21&fmt=csv",
         "<class 'NoneType'>")
    ]
)
def test_download_csv(url, output):
    func = HelperFunctions(url)
    func.query_url = url

    assert str(type(func.download_csv())) == output


def test_create_date_df():
    date_df = create_date_df("2020-03-20", "2020-03-27")

    assert len(date_df) == 8


def test_weekly_series():
    current_date = pd.to_datetime("2022-11-14")
    start_date = pd.to_datetime("2022-11-04")

    week_date = weekly_series(current_date, start_date)

    assert week_date == pd.to_datetime("2022-11-11")
