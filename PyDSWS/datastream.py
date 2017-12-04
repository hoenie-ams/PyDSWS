import requests
import json
import urllib.parse
import datetime
import pandas as pd


class Datastream:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.get_token(username, password)

    @staticmethod
    def get_token(username, password):
        # To get token, first set URL (HTTP Method: GET)
        url_token = 'http://datastream.thomsonreuters.com/DswsClient/V1/DSService.svc/rest/Token?' \
                    'username={0}&password={1}'.format(username, password)

        # Retrieve token
        t = requests.get(url_token)

        # Token to JSON format
        token_raw = json.loads(t.text)

        # Extract token
        token = token_raw["TokenValue"]

        return token

    def get_data(self, tickers, fields, date=None, start='-1D', end='-0D', freq='D', static=False):
        # Address of the API
        base = 'http://datastream.thomsonreuters.com/DswsClient/V1/DSService.svc/rest/Data?'

        # Time series or static request
        if static:
            datekind = 'Snapshot'
            if date:
                start = date
        else:
            datekind = 'TimeSeries'

        # Put all the fields in a request and encode them for requests.get
        f = {'token': self.token, 'instrument': tickers, 'datatypes': fields, 'datekind': datekind,
             'start': start, 'end': end, 'freq': freq}
        f = urllib.parse.urlencode(f)

        url = base + f

        # Retrieve data
        response = requests.get(url)

        # Data in JSON
        response_json = json.loads(response.text)

        df = self.from_json_to_df(response_json)

        return df

    @staticmethod
    def from_json_to_df(response_json):
        dates = response_json['Dates']

        # If dates is not available, the request is not constructed correctly
        if dates:
            dates_converted = []
            for d in dates:
                d = d[6:16]
                d = float(d)
                d = datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d')
                dates_converted.append(d)
        else:
            return 'Error - please check instruments and parameters (time series or static?)'

        # Set up the DataFrame
        df = pd.DataFrame(index=dates_converted)

        df.index.name = 'Date'

        # Loop through the values in the response
        for item in response_json['DataTypeValues']:
            field = item['DataType']
            for i in item['SymbolValues']:
                instrument = i['Symbol']
                values = i['Value']
                col = (instrument, field)
                df[col] = None

                # Time series return a list, Snapshots only a value
                try:
                    if values == list:
                        df[col] = pd.DataFrame(values).values
                    else:
                        df[col] = values
                except ValueError:
                    df[col] = 'ERROR'
                    print('ValueError for field: ' + field + ' (instrument: ' + instrument + ')')

        # Use Pandas MultiIndex to get from tuples to two header rows
        df.columns = pd.MultiIndex.from_tuples(df.columns, names=['Instrument', 'Field'])

        return df


