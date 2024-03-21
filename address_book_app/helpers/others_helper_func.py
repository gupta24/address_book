import json
from urllib.request import urlopen
from fastapi import status, HTTPException
from geopy import distance



def fiter_by_loc_distace(all_avail_records, curr_cor, dest_cor):
    try:
        main_distace = get_distance(curr_cor, dest_cor)
        all_find_address = []
        for row in all_avail_records:
            existing_loc_cor = (row.x_coordinates, row.y_coordinates)
            exist_distance = get_distance(curr_cor, existing_loc_cor)

            if exist_distance < main_distace:
                all_find_address.append(row)
        
        return all_find_address
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST,
                            content={"message": "occurs something...!"})


def get_distance(curr_place: tuple, dest_place: tuple):
    loc_distance = str(distance.distance(curr_place, dest_place)).split(" ")[0]
    loc_distance = round(float(loc_distance), 3)
    return loc_distance