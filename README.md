# AI_Investment_Portfolio_Recommendation - RAG Project

## Overview

This is a basic stock recommendation system built using FastAPI, FAISS, and Gemini.

It takes user input like risk level, investment duration, and budget.  
It returns a suggested portfolio with allocation.

---

## Who is this for

This project is for:

- Students learning backend development  
- Beginners exploring AI + APIs  
- Anyone trying to understand RAG systems in a simple way  


---

## What it does

- Takes user input (risk, duration, budget)  
- Retrieves relevant stocks using FAISS  
- Sends context + input to Gemini  
- Returns a portfolio with allocation  

---

## How it works

### 1. Data Collection

Stock data is fetched using `yfinance`.

Ticker names are currently **hardcoded**.

Data includes:
- Market cap  
- PE ratio  
- Growth  
- Risk indicators  

---

### 2. Data Processing

Each stock is converted into a **text summary**.

Example:

- large cap  
- low risk  
- high growth  

This summary is important.  
FAISS works on text similarity, not numbers.

---

### 3. Embedding + Storage

- Text summaries are converted into embeddings using `sentence-transformers`  
- Stored in a FAISS index  

This step happens once during startup.

---

### 4. Retrieval

When user sends a query:

- Query is converted into embedding  
- FAISS finds similar stocks  

This gives context.

---

### 5. LLM (Gemini)

- User input + retrieved stocks → sent to Gemini  
- Gemini generates portfolio suggestions  

---

### 6. UI

A simple Streamlit UI is used.

User selects:
- Risk  
- Duration (years)  
- Budget  

Then sees recommended portfolio.

---

## Tech Stack

- FastAPI → backend APIs  
- Streamlit → UI  
- FAISS → vector search  
- Sentence Transformers → embeddings  
- Gemini API → LLM reasoning  
- yfinance → stock data  

---

## Limitations 

- Tickers are hardcoded  
- Data is not real-time  
- No proper financial modeling  
- No risk calculation engine  
- LLM output may not always be structured  

---

## What I learned

- How RAG systems work  
- Difference between retrieval and generation  
- Importance of good summaries  
- Why caching matters  
- Handling LLM output safely  

---

## Future Improvements

- Dynamic stock list (NIFTY 500)  
- Better risk scoring  
- Portfolio optimization logic  
- Real-time data updates  
- Better UI  

---



### Backend

```bash
uvicorn main:app --port 9000
