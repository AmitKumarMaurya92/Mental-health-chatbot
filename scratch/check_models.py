import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

keys = [os.getenv('GEMINI_API_KEY_1'), os.getenv('GEMINI_API_KEY_2'), os.getenv('GEMINI_API_KEY_3')]

for i, key in enumerate(keys):
    if not key:
        print(f"Key {i+1} is missing")
        continue
    try:
        genai.configure(api_key=key)
        print(f"\n--- Key {i+1} ---")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print(f"Error with Key {i+1}: {e}")
