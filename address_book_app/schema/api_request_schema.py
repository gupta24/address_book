from pydantic import BaseModel, Field


class SetAddress(BaseModel):
    """
    this base model use to take the body param
    """
    dest_address: str = Field(default="1600 Amphitheatre Parkway, Mountain View, CA",
                              description="set current address")
    
    class Config:
        orm_mode = True


class AddressDetails(SetAddress):
    """
    this base model use to take the body param
    """
    curr_address: str = Field(default="1600 Amphitheatre Parkway, Mountain View, CA",
                              description="set destination address")



class OutSetAddressDetails(BaseModel):
    """
    this base model use to take the body param
    """
    id : int
    address: str
    x_coordinates: float
    y_coordinates: float

    class Config:
        orm_mode = True


class OutAllAddressDetails(BaseModel):
    """
    this base model use to take the body param
    """
    id : int
    address: str

    class Config:
        orm_mode = True