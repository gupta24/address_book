from fastapi import APIRouter, Body, status, HTTPException, Response, Depends
from fastapi.responses import JSONResponse
from typing import Optional, List
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session

from configuration import API_KEY
from address_book_app.core.logger import logger
from address_book_app.schema.api_request_schema import AddressDetails, OutAddressDetails
from address_book_app.helpers import crud_helper_func, others_helper_func
from address_book_app.core.sqlite_db_connection import get_db


routes = APIRouter(tags=["Geolocation"], prefix="/geolocation")


@routes.post('/create_address')
async def create_address(location_address: AddressDetails = Body(...), db : Session = Depends(get_db)):
    """
    Use to add the address with co-ordinates in address book for the given address.

    Request Args:
        location_address (Address) : take the address as argument.

    Reposnse:
        output (message): return created address message based on address and saved in address book.
    """

    location_address = dict(location_address)
    try:
        geolocation = Nominatim(user_agent = "MyApp")
        location = geolocation.geocode(location_address["address"])
        # get the distance of provide address with current location and distance will found in KM.
        loc_distance = others_helper_func.get_distance(location.latitude, location.longitude)
        if location:
            await crud_helper_func.create(location.address, location.latitude, location.longitude, loc_distance, db)
            return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "address created successfully!"})
        else:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "location addres is not valid!"})
    except Exception as err:
        logger.info("occurs error caused by address duplictes or address not correct!.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)



@routes.put('/update_address/{address_id}', response_model=OutAddressDetails)
async def update_address(address_id: int, location_address: AddressDetails = Body(...), db : Session = Depends(get_db)):
    """
    Use to update the address with co-ordinates in address book for the given address id.

    Request Args:
        location_address (Address) : take the address and address_id as argument.

    Reposnse:
        output (message): return the update address and coordinate message based on address_id and saved in address book 
    """
    data = await crud_helper_func.get_by_id(address_id=address_id, db=db)
    if data == None:
        raise HTTPException(detail=f"error : address id is not valid!", status_code=status.HTTP_400_BAD_REQUEST)
    
    location_address = dict(location_address)
    try:
        geolocation = Nominatim(user_agent = "MyApp")
        location = geolocation.geocode(location_address["address"])
        # get the distance of provide address with current location and distance will found in KM.
        loc_distance = others_helper_func.get_distance(location.latitude, location.longitude)
        if location:
            res_data = await crud_helper_func.update(address_id, location.address, location.latitude, location.longitude, loc_distance, db)
            return res_data
        else:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "location addres is not valid!"})
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)



@routes.get('/get_address', response_model=List[OutAddressDetails])
async def get_address(skip: int = 0, limit: int = 10, db : Session = Depends(get_db)):
    """
    Use to get the address with co-ordinates from address book.

    Request Args:
        location_address (Address) : take the address as argument.

    Reposnse:
        output (message): return all address that come within coordinates from address book.
    """
    try:
        res_data = await crud_helper_func.get(skip, limit, db)
        return res_data
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)


@routes.get('/get_address_by_distance_coordinates')
async def get_address(lattitude: float = 0.0, longitude: float = 0.0, distance: float = 0.0,  db : Session = Depends(get_db)):
    """
    Use to get the address within co-ordinates and distnace from address book.

    Request Args:
        location_address (Address) : take the latitude , longitude and distance as arguments.

    Reposnse:
        output (message): return all address that come within range of coordinates and distance of address book.
    """
    try:
        res_data = await crud_helper_func.get_by_obj_keys(lattitude, longitude, distance, db)
        return res_data
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)
        
    
@routes.delete('/delete_address/{address_id}')
async def delete_address(address_id: int, db : Session = Depends(get_db)):
    """
    Use to delete the address information from address book for the given address id.

    Request Args:
        location_address (Address) : take the address_id as argument.

    Reposnse:
        output (message): return delete address info message on address_id.
    """
    data = await crud_helper_func.get_by_id(address_id=address_id, db=db)
    if data == None:
        raise HTTPException(detail=f"error : address id is not valid!", status_code=status.HTTP_400_BAD_REQUEST)

    try:
        res_data = await crud_helper_func.delete(address_id, db)
        if not res_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "data deleted successfully!"})
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)