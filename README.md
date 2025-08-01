# LLM Document Retrieval API with Google Gemini

This is a FastAPI-based document retrieval system that uses Google Gemini LLM for intelligent question answering over PDF documents.

## Features

- PDF document processing from URLs
- Semantic search using FAISS and Sentence Transformers
- Google Gemini LLM integration
- Bearer token authentication
- JSON API responses

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables (Optional)

```bash
export GEMINI_API_KEY="your_google_gemini_api_key_here"
```

### 3. Run the Server

```bash
# Development mode
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
python main.py
```

### 4. Test the API

The server will be available at: `http://localhost:8000`

## API Usage

### Authentication
All requests require a Bearer token:
```
Authorization: Bearer 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba
```

### Endpoint: POST /api/v1/hackrx/run

**Request Body:**
```json
{
  "documents": "https://example.com/document.pdf",
  "questions": [
    "What is the grace period for premium payment?",
    "What is the waiting period for pre-existing diseases?"
  ]
}
```

**Response:**
```json
{
  "answers": [
    "A grace period of thirty days is provided for premium payment...",
    "There is a waiting period of thirty-six (36) months..."
  ]
}
```

## Deployment Options

### Local Development
```bash
uvicorn main:app --reload --port 8000
```

### Docker Deployment
Create a Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment
- Deploy to Heroku, AWS Lambda, Google Cloud Run, or Azure Container Instances
- Set environment variables for GEMINI_API_KEY
- Ensure proper security groups and networking

## API Testing

Use curl or Postman to test:

```bash
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Authorization: Bearer 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf",
    "questions": ["What is the grace period?"]
  }'
```

## Notes

- The system uses local FAISS indexing for semantic search
- Google Gemini Pro model is used for text generation
- PDF text extraction is handled by pdfplumber
- Authentication token is hardcoded for demo purposes
- For production, use environment variables and proper secret management

## Troubleshooting

1. **PDF Download Issues**: Ensure the document URL is publicly accessible
2. **Gemini API Errors**: Verify your API key and quota limits
3. **Memory Issues**: Large PDFs may require chunking optimization
4. **Token Authentication**: Ensure the Bearer token is correctly formatted

## Architecture

```
User Request → FastAPI → PDF Download → Text Extraction → 
Embedding Generation → FAISS Search → Context Retrieval → 
Gemini LLM → JSON Response
```
