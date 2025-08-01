import io
import os
import requests
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import pdfplumber
from typing import List, Optional
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from google_gemini import GoogleGeminiClient
import asyncio

app = FastAPI(title="LLM Document Retrieval API", version="1.0.0")

# Constants
AUTHORIZED_TOKEN = "479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCyLEILSjE96HexvyxwFw_S-aEvz8GQ3NI")

security = HTTPBearer()

# Models
class QueryRequest(BaseModel):
    documents: str  # URL to PDF file
    questions: List[str]

class QueryResponse(BaseModel):
    answers: List[str]

# Auth Dependency
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.scheme.lower() != "bearer" or credentials.credentials != AUTHORIZED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing authentication token")
    return True

# Download and extract text from PDF
def extract_text_from_pdf_url(url: str) -> List[str]:
    try:
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Failed to download document from {url}")

        file_bytes = io.BytesIO(r.content)
        chunks = []

        with pdfplumber.open(file_bytes) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and text.strip():
                    # Split large pages into smaller chunks
                    paragraphs = text.split('\n\n')
                    for para in paragraphs:
                        if para.strip() and len(para.strip()) > 50:
                            chunks.append(para.strip())

        return chunks
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Document extraction failed: {str(e)}")

# Build FAISS index locally using SentenceTransformer embeddings
def build_faiss_index(chunks: List[str], embedder) -> tuple:
    embeddings = embedder.encode(chunks, convert_to_numpy=True, normalize_embeddings=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # inner product = cosine similarity after normalization
    index.add(embeddings)
    return index, embeddings

@app.get("/")
async def root():
    return {"message": "LLM Document Retrieval API is running", "status": "healthy"}

@app.post("/api/v1/hackrx/run", response_model=QueryResponse)
async def run_retrieval(request_data: QueryRequest, authorized: bool = Depends(verify_token)):
    try:
        # Step 1: Extract text from PDF
        chunks = extract_text_from_pdf_url(request_data.documents)
        if not chunks:
            raise HTTPException(status_code=400, detail="No text found in document")

        print(f"Extracted {len(chunks)} chunks from document")

        # Step 2: Build embedding index
        embedder = SentenceTransformer('all-MiniLM-L6-v2')
        index, chunk_embeddings = build_faiss_index(chunks, embedder)

        # Step 3: Init Google Gemini Client
        gemini_client = GoogleGeminiClient(api_key=GEMINI_API_KEY)

        answers = []
        for question in request_data.questions:
            try:
                # Embed question
                q_vec = embedder.encode([question], convert_to_numpy=True, normalize_embeddings=True)
                top_k = min(5, len(chunks))
                D, I = index.search(q_vec, top_k)

                # Gather candidate texts
                candidates = [chunks[i] for i in I[0] if i < len(chunks)]
                combined_context = "\n\n".join(candidates[:3])  # Use top 3 for context

                # Call Google Gemini LLM to generate answer
                prompt = (
                    f"Based on the following document excerpts, provide a concise and accurate answer to the question.\n\n"
                    f"Document Context:\n{combined_context}\n\n"
                    f"Question: {question}\n\n"
                    f"Answer (be specific and reference the document):"
                )

                response_text = await gemini_client.generate_text_async(prompt)
                answers.append(response_text.strip())

            except Exception as e:
                print(f"Error processing question '{question}': {str(e)}")
                answers.append(f"Unable to process question due to: {str(e)}")

        return QueryResponse(answers=answers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
