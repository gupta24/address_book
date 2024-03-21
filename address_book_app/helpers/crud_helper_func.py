from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from address_book_app.db_models.models import AddressBook
from address_book_app.helpers import others_helper_func



async def get_by_id(address_id: int, db: Session):
    try:
        all_record = db.query(AddressBook).filter(AddressBook.id == address_id).first()
        return all_record
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)


async def create(location_address: str, lat: float, lon: float, db: Session):
    try:
        book = AddressBook(
            address=location_address,
            x_coordinates=lat,
            y_coordinates=lon
        )
        db.add(book)
        db.commit()
        db.refresh(book)
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)


async def update(address_id: int, address: str, lat: float, lon: float, db: Session):
    try:
        db.query(AddressBook).filter(AddressBook.id == address_id).update({ 
            AddressBook.address:address, AddressBook.x_coordinates:lat, AddressBook.y_coordinates:lon})
        db.commit()
        return await get_by_id(address_id=address_id, db=db)
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
    

async def search_address_details(curr_loc_cor: tuple, dest_loc_cor: tuple, db: Session):
    try:
        all_record = db.query(AddressBook).all()
        all_search_records = others_helper_func.fiter_by_loc_distace(all_record,
                                                                    curr_loc_cor, dest_loc_cor)
        return all_search_records
    except Exception as err:
        raise HTTPException(detail=f"error : {err}", status_code=status.HTTP_400_BAD_REQUEST)