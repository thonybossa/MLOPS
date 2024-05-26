from pydantic import BaseModel
    
class HouseData(BaseModel):
    status: str = "for_sale"
    bed: float = 4.0
    bath: float = 2.0
    acre_lot: float = 0.38
    state: str = "Conneticut"
    house_size: float = 1617