import geocoder
from internet_connection import isConnectedToInternet
import errors as err

# returns current latitude and longitude
def lat_long_gps():
    if isConnectedToInternet(False):
        geo_coder = geocoder.ip('me')
        return 0, (str(round(geo_coder.lat, 2)), str(round(geo_coder.lng, 2)))
    else:
        return err.error_no_internet, "You must be connected to the internet to provide me with your localization data."
