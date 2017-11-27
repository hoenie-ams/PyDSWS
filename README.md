# PyDSWS
Python: Datastream WebService (DSWS) API

Connect to the Thomson Reuters Datastream database via the DSWS server. You need to have a Datastream subscription and a username/password to use this package.

An example how to retrieve closing prices for Vodafone.
```
import PyDSWS

ds = PyDSWS.Datastream(username='XXXXXXX', password='XXXXXXX')

data = ds.get_data('VOD')

print(data)
```

Please check http://datastream.thomsonreuters.com/DswsClient/Docs/Default.aspx for all documentation.


### Resources
You can use the Datastream Navigator to look up codes and data types: http://product.datastream.com/navigator/

### Development
If you discover any issues with regards to this project, please feel free to create an Issue.
If you have coding suggestions that you would like to provide for review, please create a Pull Request.
