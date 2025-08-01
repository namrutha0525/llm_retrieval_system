import aiohttp
import asyncio
import json

class GoogleGeminiClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        # Using Gemini Pro model endpoint
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    async def generate_text_async(self, prompt: str) -> str:
        headers = {
            "Content-Type": "application/json"
        }

        body = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 1024,
            }
        }

        params = {
            "key": self.api_key
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, json=body, headers=headers, params=params) as resp:
                    if resp.status != 200:
                        text = await resp.text()
                        raise Exception(f"Google Gemini API error {resp.status}: {text}")

                    data = await resp.json()

                    # Extract text from Gemini response
                    candidates = data.get("candidates", [])
                    if not candidates:
                        raise Exception("No candidates in Gemini response")

                    content = candidates[0].get("content", {})
                    parts = content.get("parts", [])
                    if not parts:
                        raise Exception("No parts in Gemini response")

                    text_response = parts[0].get("text", "")
                    return text_response if text_response else "No response generated"

        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
