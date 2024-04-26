from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from dbmodel import Base
from dbmodel import Cases, CasesCreate, CasesRead, Item, ItemCreate, ItemRead, Cases_Items, CaseItemsCreate, CaseItemsRead

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"], # set to * here to allow all origins because Blazor does not have a set origin port for all users. 
						 # Ideally, you would set this to the port that Blazor is running on (e.g. http://localhost:7134 for me)
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

SQLALCHEMY_DATABASE_URL = "sqlite:///./Gambleproj.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create sessionmaker to create database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables based on SQLAlchemy models
Base.metadata.create_all(bind=engine)

# API route to get all cases
@app.get("/cases", response_model=list[CasesRead])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Cases).all()

# API route to get items from a specific case
@app.get("/cases/{case_id}/items", response_model=list[ItemRead])
def get_items_from_case(case_id: int, db: Session = Depends(get_db)):
    case = db.query(Cases).filter(Cases.CaseID == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    
    return [case_item.item for case_item in case.case_items]

@app.get("/items", response_model=list[ItemRead])
def get_items(db: Session = Depends(get_db)):
    return db.query(Item).all() 

@app.get("/caseitems/{case_id}", response_model=CaseItemsRead)
def get_case_items(case_id: int, db: Session = Depends(get_db)):
    try:
        case_items = db.query(Cases_Items).filter(Cases_Items.CaseID == case_id).all()
        if not case_items:
            raise HTTPException(status_code=404, detail="Items not found for this case")
        return case_items
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid case_id provided. Please provide a valid integer.")
