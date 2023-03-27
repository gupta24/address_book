from pydantic import BaseModel, Field


class AddressDetails(BaseModel):
    """
    this base model use to take the body param
    """
    address: str = Field(default="1600 Amphitheatre Parkway, Mountain View, CA", description="set your address")
    
    class Config:
        orm_mode = True


class OutAddressDetails(BaseModel):
    """
    this base model use to take the body param
    """
    id : int
    address: str
    x_coordinates: float
    y_coordinates: float

    class Config:
        orm_mode = True