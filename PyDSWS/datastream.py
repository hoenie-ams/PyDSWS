import requests
import json
import datetime
import pandas as pd


class Datastream:
    def __init__(self, username, password):
        print('TEST - __init__')
        self.username = username
        self.password = password
        self.token = self.get_token(username, password)

    def get_token(self, username, password):
        print('TEST - get_token')

        # To get token, first set URL (HTTP Method: GET)
        URL_token = 'http://datastream.thomsonreuters.com/DswsClient/V1/DSService.svc/rest/Token?' \
                    'username={0}&password={1}'.format(username, password)

        # Retrieve token
        t = requests.get(URL_token)

        # Token to JSON format
        token_raw = json.loads(t.text)

        # Extract token
        token = token_raw["TokenValue"]

        # Format token for URL
        token = token.replace("+", "%2B")

        return token

    def get_data(self, tickers='VOD', fields='P', date=None, date_from='-10D', date_to='-0D', freq='D'):
        URL_data = 'http://datastream.thomsonreuters.com/DswsClient/V1/DSService.svc/rest/Data?token={0}' \
                   '&instrument={1}&datatypes={2}&datekind=TimeSeries&start={3}&end={4}&freq={5}'\
            .format(self.token, tickers, fields, date_from, date_to, freq)

        # Retrieve data
        r = requests.get(URL_data)

        # Data in JSON
        text = json.loads(r.text)

        # Define dates and format for make it human readable
        dates = pd.DataFrame(text['Dates'])
        dates = dates[0].str.slice(start=6, stop=16)
        dates = dates.astype(float)
        dates = dates.apply(lambda x: datetime.datetime.fromtimestamp(x).strftime('%Y-%m-%d'))

        # Extract close prices
        close_price = text['DataTypeValues'][0]['SymbolValues'][0]['Value']

        # Close prices in Pandas DataFrame
        closes = pd.DataFrame(close_price)

        # Concatenate dates and close prices into DataFrame
        data = pd.concat([dates, closes], axis=1)

        # Rename the column
        data.columns = ['Date', tickers]

        return data


