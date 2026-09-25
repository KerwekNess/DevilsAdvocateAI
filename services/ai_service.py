import json
from enum import Enum
from openai import OpenAI

class AIMode(Enum):
    FORMAL = 'formal'
    ROAST = 'roast'

class AIService:
    def __init__(self, settings):
        self.settings = settings
        self.client = OpenAI(
            api_key=self.settings.API_KEY,
            base_url=self.settings.BASE_URL,
            timeout=90.0
        )
        self.prompts = {
            AIMode.FORMAL: "You are a professional and formal critic. Analyze the user's idea. Provide a polite, sophisticated, and highly professional critique of the idea. Output a JSON object with keys 'text' (a single sentence professional critique) and 'items' (a list of 6 alternative formal critiques).",
            AIMode.ROAST: "You are a brutal, sarcastic, and evil roast master. Your goal is to destroy the user's idea with sharp wit, dark humor, and savage sarcasm. Output a JSON object with keys 'text' (a single sentence devastating roast) and 'items' (a list of 6 alternative savage/evil roasts)."
        }

    def analyze(self, idea: str, mode: AIMode) -> tuple[str, list[str]]:
        prompt = self.prompts.get(mode, self.prompts[AIMode.ROAST])
        
        response = self.client.chat.completions.create(
            model=self.settings.MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": idea},
            ],
            response_format={"type": "json_object"},
            temperature=0.8,
        )
        
        data = json.loads(response.choices[0].message.content)
        
        text = data.get("text", "").strip()
        items = data.get("items", [])
        
        if not items:
            items = [text]
            
        return text, items[:6]
