import os
import json
import requests
from typing import Dict, List, Optional
import time
from openai import OpenAI
from google import genai
from google.genai import types

class AIPlatformManager:
    """Manager for querying different AI platforms"""
    
    def __init__(self):
        # Initialize API clients
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))
        self.gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", ""))
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
        
    def query_platform(self, platform: str, prompt: str) -> str:
        """Query a specific AI platform with a prompt"""
        try:
            if platform == "openai":
                return self._query_openai(prompt)
            elif platform == "gemini":
                return self._query_gemini(prompt)
            elif platform == "perplexity":
                return self._query_perplexity(prompt)
            # Copilot and Meta AI disabled
            # elif platform == "copilot":
            #     return self._query_copilot(prompt)
            # elif platform == "meta":
            #     return self._query_meta(prompt)
            else:
                raise ValueError(f"Unsupported platform: {platform}")
        except Exception as e:
            return f"Error querying {platform}: {str(e)}"
    
    def _query_openai(self, prompt: str) -> str:
        """Query OpenAI's ChatGPT"""
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            return f"OpenAI API Error: {str(e)}"
    
    def _query_gemini(self, prompt: str) -> str:
        """Query Google's Gemini"""
        try:
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text or "No response generated"
        except Exception as e:
            return f"Gemini API Error: {str(e)}"
    
    def _query_perplexity(self, prompt: str) -> str:
        """Query Perplexity AI"""
        try:
            headers = {
                'Authorization': f'Bearer {self.perplexity_api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "llama-3.1-sonar-small-128k-online",
                "messages": [
                    {
                        "role": "system",
                        "content": "Be precise and concise in your response."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7,
                "top_p": 0.9,
                "return_images": False,
                "return_related_questions": False,
                "search_recency_filter": "month",
                "stream": False
            }
            
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Perplexity API Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Perplexity API Error: {str(e)}"
    
    def _query_copilot(self, prompt: str) -> str:
        """Query Microsoft Copilot (Bing-integrated AI)"""
        try:
            # Note: Microsoft Copilot doesn't have a direct public API
            # For demonstration purposes, we'll simulate responses
            # In a production environment, you would need to use Microsoft's Azure OpenAI Service
            # or the Bing Search API with AI-powered responses
            return f"[Microsoft Copilot Response - API Integration Pending]: For '{prompt}', Copilot would provide Bing-enhanced AI responses with real-time web search capabilities."
        except Exception as e:
            return f"Microsoft Copilot Error: {str(e)}"
    
    def _query_meta(self, prompt: str) -> str:
        """Query Meta AI"""
        try:
            # Note: Meta AI doesn't have a direct public API for external use
            # For demonstration purposes, we'll simulate responses
            # In a production environment, you would need proper Meta AI API access
            return f"[Meta AI Response - API Integration Pending]: For '{prompt}', Meta AI would provide conversational responses leveraging Facebook's AI technology."
        except Exception as e:
            return f"Meta AI Error: {str(e)}"
    
    def test_platform_connectivity(self, platform: str) -> bool:
        """Test if a platform is accessible"""
        try:
            test_prompt = "Hello, this is a test message."
            response = self.query_platform(platform, test_prompt)
            return not response.startswith("Error")
        except:
            return False
    
    def get_platform_status(self) -> Dict[str, bool]:
        """Get status of all platforms"""
        return {
            "openai": self.test_platform_connectivity("openai"),
            "gemini": self.test_platform_connectivity("gemini"),
            "perplexity": self.test_platform_connectivity("perplexity")
            # Copilot and Meta AI disabled
            # "copilot": self.test_platform_connectivity("copilot"),
            # "meta": self.test_platform_connectivity("meta")
        }
