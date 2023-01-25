# PyDSWS
Python wrapper for the Datastream Web Services API (DSWS)

Connect to the Refinitiv Datastream database via Datastream Web Services. You need to have a Datastream subscription and a username/password to use this package.
Please note that this is an unofficial/unsupported package and it is still under development. The package has basic functionality and most of the error handling still needs to be done.

### Installation
PyDSWS is written in Python 3.
Dependencies:
```
pandas
requests
```

Installation:
```shell
pip install PyDSWS
```

### Usage

Quick Start:

An example how to retrieve closing prices for Vodafone.
1) import the 'PyDSWS' package
2) authenticate with your username and password
3) use the 'get_data' function

```python
import PyDSWS

ds = PyDSWS.Datastream(username='XXXXXXX', password='XXXXXXX')

df = ds.get_data('VOD')

print(df)
```

Please find below examples on how to set parameters for the requests.

For static data:
```python
ds.get_data(tickers='VOD', fields='P', date='2017-01-01')
```

For time series:
```python
ds.get_data(tickers='VOD', fields='P,MV,VO', start='-10D', end='-0D', freq='D')
```
*for multiple tickers/fields, just use a comma. In this example: fields='P,MV,VO'


The output is a Pandas DataFrame:
```
Instrument     VOD
Field            P        MV       VO
Date
2017-11-21  229.75  61283.06  55100.4
2017-11-22  228.75  61016.34  79602.5
2017-11-23  225.40  60122.75  35724.1
2017-11-24  225.50  60149.44  42918.0
2017-11-27  224.60  59909.38  50355.3
2017-11-28  226.45  60402.83  49027.0
2017-11-29  225.25  60082.74  61618.1
2017-11-30  224.30  59829.99  95423.4
2017-12-01  224.00  59749.96  54855.4
2017-12-04  225.55  60163.41  47524.1
2017-12-05  225.25  60083.38  43846.7
```

In order to get usage statistics call:
```python
ds.get_usage()
```

The output is a Pandas DataFrame:
```
Instrument    STATS                                                           
Field          User Hits Requests Datatypes Datapoints  Start Date    End Date
Date                                                                          
2019-06-26  ZMTXXXX  564      362      1319    1283696  2019-06-01  2019-07-01
```

Please check http://datastream.refinitiv.com/DswsClient/Docs/Default.aspx for further documentation.


### Resources
You can use the Datastream Navigator to look up codes and data types: http://product.datastream.com/navigator/

### Development
If you discover any issues with regards to this project, please feel free to create an Issue.
If you have coding suggestions that you would like to provide for review, please create a Pull Request.

### Acknowledgements
Thanks to Vladimir Filimonov for his work on https://github.com/vfilimonov/pydatastream, and Charles Cara for https://github.com/CharlesCara/DatastreamDSWS2R


