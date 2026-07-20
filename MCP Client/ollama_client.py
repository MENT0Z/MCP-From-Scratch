import requests

class OllamaClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/chat"
        self.model = "gemma3:1b"
    
    def chat(self,message):
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "messages":message,
                "stream": False
            }
        )

        response.raise_for_status()
        return response.json()["message"]["content"]