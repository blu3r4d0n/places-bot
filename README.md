# Every Place Bot

[@everyusplace](@everyusplace) is a twitter bot that tweets out masked aerial images of geographies
![alt text](https://pbs.twimg.com/media/FHWGap2X0AI2GAP?format=jpg&name=900x900)
## Description

This bot tweets out masked aerial imagery of US Census places using shapes from [IPUMS NHGIS](https://www.nhgis.org/). 

## Getting Started
This bot looks for a shapefile named US_place_2020.shp which can be obtained from NHGIS. You can also swap out this file for another file but some things might break depending on the names of the attributes of the file.

You will also need to create a secrets.py and populate it with [twitter developer credentials](https://developer.twitter.com/en/products/twitter-api). Like this:
```
consumer_key = "YOUR API KEY HERE"
consumer_secret="YOUR API SECRET HERE"
access_token="YOUR ACCESS TOKEN HERE"
access_token_secret="YOUR ACCESS TOKEN SECRET HERE"
```
### Dependencies

* python 3.9
* geopandas
* rasterio
* us
* rasterio
* xyzservices
* requests
* tweepy

### Executing program

```
python bot.py
```

## Authors


Philip Nelson
ex. [@blu3r4d0n](https://twitter.com/blu3r4d0n)


## Acknowledgments

The inspiration for this bot was [@everytract](https://twitter.com/everytract) by [@fitnr](https://twitter.com/fitnr).
