from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

app = FastAPI()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_sentiment_ai"]
collection = db["messages"]
users_collection = db["users"]
login_history_collection = db["login_history"]

# Hugging Face Model
MODEL = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
labels = ['negative', 'neutral', 'positive']

# Models
class TextInput(BaseModel):
    text: str
    username: str  # <-- NEW: Added username

class UserAuth(BaseModel):
    username: str
    email: str = None
    password: str

# Utils
def get_sentiment(text):
    encoded_input = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        output = model(**encoded_input)
    scores = output[0][0].numpy()
    scores = np.exp(scores) / np.sum(np.exp(scores))
    top = np.argmax(scores)
    label = labels[top]
    confidence = float(scores[top])
    sentiment_score = {"negative": -confidence, "neutral": 0, "positive": confidence}[label]
    return label, confidence, sentiment_score

# Routes
@app.get("/")
def root():
    return {"message": "API Running!"}

@app.post("/analyze/")
def analyze(input: TextInput):
    label, confidence, sentiment_score = get_sentiment(input.text)
    collection.insert_one({
        "username": input.username,  # <-- Save username with the message
        "text": input.text,
        "label": label,
        "confidence": confidence,
        "sentiment": sentiment_score,
        "timestamp": datetime.utcnow()
    })
    return {"label": label, "confidence": confidence, "sentiment": sentiment_score}

@app.post("/register")
def register(user: UserAuth):
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username already exists.")
    users_collection.insert_one({
        "username": user.username,
        "email": user.email,
        "password": user.password,
        "created_at": datetime.utcnow()
    })
    return {"message": "Registered Successfully!"}

@app.post("/login")
def login(user: UserAuth):
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or db_user['password'] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password.")
    login_history_collection.insert_one({
        "username": user.username,
        "login_time": datetime.utcnow()
    })
    return {"message": "Login Successful!"}
