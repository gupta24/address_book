import json
from urllib.request import urlopen
from fastapi import status, HTTPException
from geopy import distance

from configuration import CURRENT_LOC_URL



def curren_loc_coordinates():
    try:
        response = urlopen(CURRENT_LOC_URL)
        data = json.load(response)
        if data and data.get("loc", None):
            curr_lat_lon = data["loc"].split(",")
            current_place = (float(curr_lat_lon[0]), float(curr_lat_lon[1]))
            return current_place
        return {"message": "current address location coordinates not found!"}
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_204_NO_CONTENT, content={"message": "current location not found!"})


def get_distance(address_lat: float, address_lon: float):
    des_place = (address_lat, address_lon)
    curr_place = curren_loc_coordinates()
    loc_distance = str(distance.distance(curr_place, des_place)).split(" ")[0]
    loc_distance = round(float(loc_distance), 3)
    return loc_distance