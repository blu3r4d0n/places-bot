import geopandas as gpd
import us

import rasterio
import rasterio.mask
from xyzservices import TileProvider
from requests.exceptions import HTTPError
#df=gpd.read_file("")
df = gpd.read_file("US_place_2020.shp")  #this file can be obtained from IPUHMS NHGIS
df=df.to_crs(epsg=3857)

import contextily as ctx


west, south, east, north = bbox = df.iloc[0].geometry.bounds
shapes=[df.geometry.iloc[0]]
try:
	img, ext = ctx.bounds2raster(west,south,east,north,"output.tif",zoom='auto',source=TileProvider.from_qms("Google Satellite")) #try with auto zoom level
except HTTPError:
        img, ext = ctx.bounds2raster(west,south,east,north,"output.tif",zoom=15,source=TileProvider.from_qms("Google Satellite")) #if that doesn't work try with 15, if this fails the program will crash
with rasterio.open("output.tif") as src:
	out_image, out_transform = rasterio.mask.mask(src,shapes,crop=True)  #mask the input iamge to polygon bounds 
	out_meta=src.meta


out_meta.update({"driver": "GTiff","height": out_image.shape[1],"width": out_image.shape[2],"transform": out_transform}) #update the metadata
     
with rasterio.open("masked.tif", "w", **out_meta) as dest:
	dest.write(out_image)

#get info for place
name=df.iloc[0].NAME
geoid=df.iloc[0].GEOID
statefp = df.iloc[0].STATEFP
state=us.states.lookup(statefp).name

#save the image as a JPG to make it postable to twitter
from PIL import Image
im = Image.open("masked.tif")
bg=Image.new("RGB",tuple([int(round(.05*x+x)) for x in im.size]),(255,255,255)) 
img_w, img_h = im.size
bg_w, bg_h = bg.size
bg_w, bg_h = bg.size
offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)

bg.paste(im,offset,im)
size=1980,1080
bg.thumbnail(size,Image.LANCZOS)
bg.save("image.jpg")

filename="image.jpg"

#post to twitter
import tweepy
from secrets import *
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

res = api.media_upload(filename)

media_id = res.media_id

api.create_media_metadata(media_id,f"An aerial image of {name}, {state} surrounded by white.")
api.update_status(status=f'GEOID {geoid} {name}, {state}',media_ids=[media_id])


#delete this row and save to shapefile
df=gpd.read_file("US_place_2020.shp")
df = df.iloc[1:]
df.to_file("US_place_2020.shp")

