from fastapi import APIRouter, Body, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import List
from geopy.geocoders import Nominatim
from sqlalchemy.orm import Session

from address_book_app.core.logger import logger
from address_book_app.schema.api_request_schema import (AddressDetails,
                                                        OutAllAddressDetails,
                                                        SetAddress,
                                                        OutSetAddressDetails) 
from address_book_app.helpers import crud_helper_func
from address_book_app.core.sqlite_db_connection import get_db


routes = APIRouter(tags=["Geolocation"], prefix="/geolocation")


@routes.post('/create_address')
async def create_address(location_address: SetAddress = Body(...),
                         db : Session = Depends(get_db)):
    """
    Use to add the address with co-ordinates in address book for the given address.

    Request Args:
        location_address (Address) : take the address as argument.

    Reposnse:
        output (message): return created address message based on address and saved
                        in address book.
    """

    location_address = dict(location_address)
    try:
        geolocation = Nominatim(user_agent = "MyApp")
        loc = geolocation.geocode(location_address["dest_address"])

        if loc:
            await crud_helper_func.create(loc.address, loc.latitude, loc.longitude, db)
            return JSONResponse(status_code=status.HTTP_201_CREATED,
                                content={"message": "address created successfully!"})
        else:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                                content={"message": "location addres is not valid!"})
        
    except Exception as err:
        logger.info("occurs error caused by address duplictes or address not correct!.")
        raise HTTPException(detail=f"error : {err}",
                            status_code=status.HTTP_400_BAD_REQUEST)



@routes.put('/update_address/{address_id}', response_model=OutSetAddressDetails)
async def update_address(address_id: int, location_address: SetAddress = Body(...),
                         db : Session = Depends(get_db)):
    """
    Use to update the address with co-ordinates in address book for the given address id.

    Request Args:
        location_address (Address) : take the address and address_id as argument.

    Reposnse:
        output (message): return the update address and coordinate message based on address_id 
                        and saved in address book 
    """
    data = await crud_helper_func.get_by_id(address_id=address_id, db=db)
    if data == None:
        raise HTTPException(detail=f"error : address id is not valid!",
                                status_code=status.HTTP_400_BAD_REQUEST)
    

    location_address = dict(location_address)
    try:
        geolocation = Nominatim(user_agent = "MyApp")
        loc = geolocation.geocode(location_address["dest_address"])

        # # get the distance of provide address with current location and distance will found in KM.
        # loc_distance = others_helper_func.get_distance(location.latitude, location.longitude)
        if loc:
            res_data = await crud_helper_func.update(address_id, loc.address,
                                                    loc.latitude, loc.longitude, db)
            return res_data
        else:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT,
                                content={"message": "location addres is not valid!"})
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)



@routes.get('/get_address', response_model=List[OutAllAddressDetails])
async def get_address(skip: int = 0, limit: int = 10, db : Session = Depends(get_db)):
    """
    Use to get the address with co-ordinates from address book.

    Request Args:
        location_address (Address) : take the address as argument.

    Reposnse:
        output (message): return all address from address book.
    """
    try:
        res_data = await crud_helper_func.get(skip, limit, db)
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
        raise HTTPException(detail=f"error : address id is not valid!",
                            status_code=status.HTTP_400_BAD_REQUEST)

    try:
        res_data = await crud_helper_func.delete(address_id, db)
        if not res_data:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content={"message": "data deleted successfully!"})
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)
    


@routes.post('/search_address', response_model=List[OutSetAddressDetails])
async def search_address(loc_address: AddressDetails, db : Session = Depends(get_db)):
    """
    Use to get the all address which come under the destination co-ordinates and distance.

    Request Args:
        loc_address (AddressDetails) : take the current address and destination address
                                    as loc_address argument.

    Reposnse:
        output (message): return all address that come within coordinates from address book.
    """
    try:
        loc_address = dict(loc_address)

        geolocation = Nominatim(user_agent = "MyApp")
        # validate and get the current address coordinates
        curr_loc = geolocation.geocode(loc_address["curr_address"])
        if not curr_loc:
            raise ValueError("current location not valid!")
        
        dest_loc = geolocation.geocode(loc_address["dest_address"])
        if not dest_loc:
            raise ValueError("destination location not valid!")
        

        res_data = await crud_helper_func.search_address_details(curr_loc[1], dest_loc[1], db)
        return res_data
    except Exception as err:
        logger.info("address occurs some error.")
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)

