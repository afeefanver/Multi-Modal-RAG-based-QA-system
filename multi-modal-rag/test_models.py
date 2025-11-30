from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

models_to_test = [
    "gpt-3.5-turbo",
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4",
    "gpt-4-turbo"
]

print("Testing which models you have access to...\n")

for model in models_to_test:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5
        )
        print(f"✓ {model} - WORKS")
    except Exception as e:
        if "model_not_found" in str(e) or "does not exist" in str(e):
            print(f"✗ {model} - NO ACCESS")
        else:
            print(f"✗ {model} - ERROR: {e}")