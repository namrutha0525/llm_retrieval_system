# LLM Document Retrieval API v2 - Render Optimized

This is a simplified, **Render-deployment-optimized** FastAPI application for document retrieval and Q&A using Google Gemini LLM.

## Key Features

- ✅ **Minimal dependencies** to avoid build issues
- ✅ **Google Gemini LLM integration** 
- ✅ **Bearer token authentication**
- ✅ **Simplified PDF processing** (no complex ML libraries)
- ✅ **JSON API responses**
- ✅ **Render-ready configuration**

## Quick Deploy on Render

### 1. Push to GitHub
- Create a new GitHub repository
- Upload all files from this folder to your repo
- Commit and push

### 2. Deploy on Render
- Go to [render.com](https://render.com)
- Create **New Web Service**
- Connect your GitHub repo
- Use these settings:

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Environment Variables:**
- Key: `GEMINI_API_KEY`
- Value: `AIzaSyCyLEILSjE96HexvyxwFw_S-aEvz8GQ3N`

### 3. Test Your API

Once deployed, your API will be available at:
- Health check: `https://your-app.onrender.com/health`
- Main endpoint: `https://your-app.onrender.com/api/v1/hackrx/run`

## API Usage

### Authentication
```
Authorization: Bearer 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba
```

### Sample Request
```bash
curl -X POST "https://your-app.onrender.com/api/v1/hackrx/run" \
  -H "Authorization: Bearer 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/document.pdf",
    "questions": [
      "What is the main topic of this document?",
      "What are the key terms mentioned?"
    ]
  }'
```

### Sample Response
```json
{
  "answers": [
    "The main topic of this document is...",
    "The key terms mentioned include..."
  ]
}
```

## Local Development

### Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

### Test locally
```bash
curl -X POST "http://localhost:8000/api/v1/hackrx/run" \
  -H "Authorization: Bearer 479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba" \
  -H "Content-Type: application/json" \
  -d '{
    "documents": "https://example.com/test.pdf",
    "questions": ["What is this document about?"]
  }'
```

## File Structure

```
llm_retrieval_system_v2/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies (minimal)
├── runtime.txt         # Python version for Render
├── README.md           # This file
├── deploy.sh           # Deployment script for local testing
└── Dockerfile          # Optional Docker setup
```

## Troubleshooting

### Common Issues

1. **Build Failed on Render**
   - Check that `requirements.txt` only contains the listed dependencies
   - Verify Python version in `runtime.txt` is supported
   - Clear build cache in Render dashboard

2. **Authentication Errors**
   - Ensure Bearer token is exactly: `479309883e76b7aff59e87e1e032ce655934c42516b75cc1ceaea8663351e3ba`
   - Check Authorization header format

3. **Gemini API Errors**
   - Verify `GEMINI_API_KEY` environment variable is set in Render
   - Check API key is valid and has quota

4. **Document Processing Issues**
   - Ensure document URL is publicly accessible
   - Check network connectivity from Render to document source

## Differences from v1

- **Removed complex ML libraries** (sentence-transformers, faiss-cpu) to avoid build issues
- **Simplified text extraction** - no pdfplumber dependency
- **Basic keyword matching** instead of semantic search
- **Minimal requirements** for stable Render deployment
- **Better error handling** and fallback responses

## Production Considerations

- For production use, consider adding:
  - Database for caching results
  - Redis for session management  
  - More sophisticated text extraction
  - Rate limiting
  - Monitoring and logging
  - Input validation and sanitization

## Support

If you encounter issues:
1. Check the Render build logs
2. Verify all environment variables are set
3. Test the API locally first
4. Review the troubleshooting section above

---

**Version:** 2.0.0  
**Last Updated:** August 2025  
**Optimized for:** Render.com deployment
