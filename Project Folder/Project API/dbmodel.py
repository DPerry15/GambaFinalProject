from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class Cases(Base):
    __tablename__ = 'Cases'

    CaseID = Column(Integer, primary_key = True, autoincrement = False)
    Name = Column(String)
    Cost = Column(Integer)

    def __repr__(self):
        return f"<Cases(Case_ID={self.CaseID}, name={self.Name}, cost={self.Cost})>"
    
class CasesCreate(BaseModel):
    CaseID: int
    Name: str
    Cost: int

class CasesRead(CasesCreate):
    class config:
        orm_mode = True

class Item(Base):
    __tablename__ = 'Item'

    ItemID = Column(Integer, primary_key=True, autoincrement=True)
    Value = Column(Integer)
    Name = Column(String)
    Description = Column(String)

class ItemCreate(BaseModel):
    ItemID: int
    Value: int
    Name: str
    Description: str

class ItemRead(ItemCreate):
    class config:
        orm_mode = True


class Cases_Items(Base):
    __tablename__ = 'Case_Items'

    CaseItemID = Column(Integer, primary_key = True, autoincrement = False)
    ItemID = Column(Integer, ForeignKey('Item.ItemID'))
    CaseID = Column(Integer, ForeignKey('Cases.CaseID'))

    item = relationship("Item", backref="Cases_Items")
    cases = relationship("Cases", backref="Cases_items")

class CaseItemsCreate(BaseModel):
    CaseID: int
    ItemID: int
    CaseItemID: int

class CaseItemsRead(CaseItemsCreate):
    class config:
        orm_mode = True

