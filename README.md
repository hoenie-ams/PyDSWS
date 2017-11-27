# PyDSWS
Python: Datastream WebServices API (DSWS)

Connect to the Thomson Reuters Datastream database via Datastream Web Services (DSWS). You need to have a Datastream subscription and a username/password to use this package. Please note that this package is under development. For the time being it is only possible to retrieve timeseries of a single instrument with a single data field per request.

### Installation
```
pip install PyDSWS
```

### Usage

Quick Start: 

An example how to retrieve closing prices for Vodafone. 
1) import the 'PyDSWS' package
2) authenticate with your username and password
3) use the 'get_data' function

```
import PyDSWS

ds = PyDSWS.Datastream(username='XXXXXXX', password='XXXXXXX')

data = ds.get_data('VOD')

print(data)
```

You can set parameters like this:
```
get_data(tickers='VOD', fields='P', date_from='-10D', date_to='-0D', freq='D')
```
Please check http://datastream.thomsonreuters.com/DswsClient/Docs/Default.aspx for further documentation.


### Resources
You can use the Datastream Navigator to look up codes and data types: http://product.datastream.com/navigator/

### Development
If you discover any issues with regards to this project, please feel free to create an Issue.
If you have coding suggestions that you would like to provide for review, please create a Pull Request.

### Acknowledgements
Thanks to Vladimir Filimonov for his work on https://github.com/vfilimonov/pydatastream, and Charles Cara for https://github.com/CharlesCara/DatastreamDSWS2R
