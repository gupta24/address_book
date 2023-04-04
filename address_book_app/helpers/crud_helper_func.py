from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from address_book_app.db_models.models import AddressBook




async def create(location_address: str, lat: float, lon: float, loc_distance: float, db: Session):
    try:
        #import pdb; pdb.set_trace()
        #print(location_address, lat, lon)
        book = AddressBook(
            address=location_address,
            x_coordinates=lat,
            y_coordinates=lon,
            location_distance=loc_distance
        )
        db.add(book)
        db.commit()
        db.refresh(book)
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)



async def update(address_id: int, address: str, lat: float, lon: float, loc_address: float, db: Session):
    try:
        db.query(AddressBook).filter(AddressBook.id == address_id).update({ 
            AddressBook.address:address, AddressBook.x_coordinates:lat,  AddressBook.y_coordinates:lon, AddressBook.location_distance:loc_address})
        db.commit()
        return await get_by_id(address_id=address_id, db=db)
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)
    

async def get_by_id(address_id: int, db: Session):
    try:
        all_record = db.query(AddressBook).filter(AddressBook.id == address_id).first()
        return all_record
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)


async def get_by_obj_keys(lat: float, lon: float, loc_dis: float, db: Session):
    try:
        all_record = db.query(AddressBook).all()
        if all_record:
            list_record = []
            for item in all_record:
                filter_item = {}
                if (abs(item.x_coordinates) <= abs(lat)) and (abs(item.y_coordinates) <= abs(lon)) and (abs(item.location_distance) <= abs(loc_dis)):
                    filter_item["address"] = item.address
                    filter_item["x_coordinates"] = item.x_coordinates
                    filter_item["y_coordinates"] = item.y_coordinates
                    filter_item["location_distance"] = item.location_distance
                    list_record.append(filter_item)

        return list_record
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)


async def get(skip: int, limit: int, db: Session):
    try:
        all_record = db.query(AddressBook).offset(skip).limit(limit).all()
        return all_record
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)



async def delete(address_id: str, db: Session):
    try:
        db.query(AddressBook).filter(AddressBook.id == address_id).delete()
        db.commit()
        return await get_by_id(address_id=address_id, db=db)
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)