import requests


class LLMService:

    OLLAMA_URL = "http://host.docker.internal:11434/api/generate"
    MODEL = "phi3"
    TIMEOUT = 30

    def generate(self, text):

        prompt = f"""
You are a professional AI banking assistant.

Answer politely and clearly.
Help users with banking services such as:
- balance inquiries
- transfers
- deposits
- loans
- cards
- investments
- insurance

User question:
{text}

Answer:
"""
        return self._call(prompt)

    def generate_with_prompt(self, prompt):
        return self._call(prompt)

    def _call(self, prompt):

        try:

            response = requests.post(
                "http://host.docker.internal:11434/api/generate",
                json={
                    "model": "phi3",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )

            data = response.json()

            return data.get("response", "I could not generate an answer.")

        except Exception as e:

            print("LLM ERROR:", e)

            return "Sorry, the AI assistant is temporarily unavailable."