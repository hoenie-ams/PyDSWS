"""
PyDSWS

@author: Joris Hoendervangers

"""

import datetime
import json

import pandas as pd
import requests


class Datastream:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.get_token(username, password)

    @staticmethod
    def get_token(username, password):
        # To get token, first set URL (HTTP Method: GET)
        token_url = 'https://product.datastream.com/DSWSClient/V1/DSService.svc/rest/Token?' \
                    'username={0}&password={1}'.format(username, password)

        # Retrieve token
        token_raw = requests.get(token_url)

        # Token to JSON format
        token_json = json.loads(token_raw.text)

        # Extract token
        token = token_json["TokenValue"]

        return token

    @staticmethod
    def from_json_to_df(response_json):
        if not response_json['Dates']:
            return 'Error - please check instruments and parameters (time series or static)'

        dates = response_json['Dates']
        dates_converted = []
        for d in dates:
            d = d[6:-10]
            d = float(d)
            d = datetime.datetime.fromtimestamp(d).strftime('%Y-%m-%d')
            dates_converted.append(d)
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
                    if values == list:  # Time series
                        df[col] = pd.DataFrame(values).values
                    else:
                        if (
                            'Type' in i.keys()
                            and i['Type'] == 4
                            and values[:6] == '/Date('
                        ):
                            values = datetime.datetime.fromtimestamp(float(values[6:-10])).strftime('%Y-%m-%d')

                        df[col] = values  # Snapshot

                except ValueError:  # In case of ValueError, fill the column with 'ERROR'
                    df[col] = 'ERROR'
                    print('ValueError for field: ' + field + ' (instrument: ' + instrument + ')')

        # Use Pandas MultiIndex to get from tuples to two header rows
        df.columns = pd.MultiIndex.from_tuples(df.columns, names=['Instrument', 'Field'])

        return df

    def get_data(self, tickers, fields='', date='', start='', end='', freq=''):
        # Only 'tickers' is required. The others default to '' instead of None, otherwise the API calls won't work.
        # Address of the API
        url = 'https://product.datastream.com/DswsClient/V1/DSService.svc/rest/Data?'

        # Decide if the request is a time series or static request
        if not start:
            datekind = 'Snapshot'
            start = date  # For static requests, the value of 'date' needs to be put in to 'start'
            # 'date' is not used in the actual request to the API, it is designed to make PyDSWS more intuitive.
        else:
            datekind = 'TimeSeries'

        # Put all the fields in a request and encode them for requests.get
        fields = {'token': self.token, 'instrument': tickers, 'datatypes': fields, 'datekind': datekind,
                  'start': start, 'end': end, 'freq': freq}

        # Retrieve data and use the json native decoder
        response = requests.get(url, params=fields).json()

        # Run 'from_json_to_df()' to convert the JSON response to a Pandas DataFrame
        df = self.from_json_to_df(response)

        return df

    def get_usage(self):
        # Returns usage statistics.
        # Address of the API
        url = 'https://product.datastream.com/DswsClient/V1/DSService.svc/rest/Data?'

        # Put all the fields in a request and encode them for requests.get
        fields = {'token': self.token, 'instrument': 'STATS', 'datatypes': 'DS.USERSTATS', 'datekind': 'Snapshot',
                  'start': '', 'end': '', 'freq': ''}

        # Retrieve data and use the json native decoder
        response = requests.get(url, params=fields).json()

        # Run 'from_json_to_df()' to convert the JSON response to a Pandas DataFrame
        df = self.from_json_to_df(response)

        return df
