from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Card
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://cards_db_ka8q_user:oJ8c77zdqnrsrgAPT7TlQSoqTAvXLiBt@dpg-d0a58kjuibrs73augn2g-a/cards_db_ka8q")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic model for card creation
class CardCreate(BaseModel):
    title: str
    category: str

# Route to fetch cards based on category
@app.get("/cards")
def get_cards(category: str = Query(None)):
    db = SessionLocal()
    if category:
        cards = db.query(Card).filter(Card.is_active == True, Card.category == category).all()
    else:
        cards = db.query(Card).filter(Card.is_active == True).all()
    return cards

# Route to handle click on a card
@app.post("/cards/{card_id}/click")
def click_card(card_id: int):
    db = SessionLocal()
    card = db.query(Card).filter(Card.id == card_id).first()
    if card:
        card.click_count += 1
        db.commit()
        return {"message": "Click recorded"}
    return {"error": "Card not found"}

# Admin route to create a new card
@app.post("/admin/cards")
def create_card(card: CardCreate):
    db = SessionLocal()
    db_card = Card(title=card.title, category=card.category)
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

# Route to add sample cards (for testing purposes)
@app.post("/admin/add-sample-cards")
def add_sample_cards():
    db = SessionLocal()
    sample_data = [
        {"title": "Electric Beast", "category": "Electric Bike"},
        {"title": "Cycle King", "category": "E-Cycles"},
        {"title": "Zoom 3000", "category": "High-Speed Scooter"},
        {"title": "Eco Comfy", "category": "Low-Speed Scooter"},
    ]
    for item in sample_data:
        card = Card(title=item["title"], category=item["category"])
        db.add(card)
    db.commit()
    return {"message": "Sample cards added!"}

# Route to check if the API is running
@app.get("/")
def root():
    return {"message": "Vehicle Cards API is running!"}
