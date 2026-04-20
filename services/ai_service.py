import google.generativeai as genai
from openai import OpenAI
from config import GEMINI_API_KEYS, GROQ_API_KEY
from services.sentiment_service import analyze_sentiment, get_sentiment_label
from services.safety_service import check_safety, get_emergency_response
from services.suggestion_service import get_suggestion_for_mood
from services.memory_service import load_history, save_message
from services.db_service import log_mood
import random
import unicodedata

def detect_language(text: str) -> str:
    """Detects if the user's message is primarily Hindi, English, or Hinglish."""
    hindi_chars = sum(1 for ch in text if '\u0900' <= ch <= '\u097F')
    total_alpha = sum(1 for ch in text if ch.isalpha())
    if total_alpha == 0:
        return "English"
    hindi_ratio = hindi_chars / total_alpha
    if hindi_ratio > 0.4:
        return "Hindi"
    elif hindi_ratio > 0.1:
        return "Hinglish (a mix of Hindi and English)"
    return "English"

# Initialize Groq client if available
groq_client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
) if GROQ_API_KEY else None

def get_gemini_model(system_instruction=None):
    """Configures and returns a Gemini model instance by directly trying preferred models."""
    preferred_models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-1.0-pro",
    ]

    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
    ]

    for key in GEMINI_API_KEYS:
        genai.configure(api_key=key)
        for model_name in preferred_models:
            try:
                model = genai.GenerativeModel(
                    model_name,
                    system_instruction=system_instruction,
                    safety_settings=safety_settings
                )
                # Quick validation — will throw if key or model is invalid
                model.generate_content("hi")
                print(f"[OK] Using Gemini model: {model_name}")
                return model
            except Exception as e:
                print(f"  [WARN] Model '{model_name}' failed: {e}")
                continue
        print(f"  [FAIL] All models failed for this key, trying next...")

    print("[ERROR] No valid API key / model combination found. Falling back to offline mode.")
    return None


def generate_response(user_message: str, username: str = "default") -> str:
    """Sends a message to the Gemini API and returns the response, incorporating memory, safety and sentiment analysis."""
    
    # 0. Save the user's message to memory immediately
    save_message("user", user_message, username)

    # 1. Internal Safety Check (Keyword based for immediate crisis)
    if not check_safety(user_message):
        reply = get_emergency_response()
        save_message("assistant", reply, username)
        return reply
        
    # 2. Analyze sentiment and get suggestions
    sentiment_scores = analyze_sentiment(user_message)
    sentiment_label = get_sentiment_label(sentiment_scores['compound'])
    suggestion = get_suggestion_for_mood(sentiment_label, user_message)
    
    # 2.5 Log mood for tracking
    log_mood(sentiment_scores['compound'], sentiment_label, username)
    
    # 3. Detect language and build system prompt
    detected_lang = detect_language(user_message)
    system_prompt = (
        f"You are MindMate AI, a gentle, supportive, and empathetic mental health companion speaking to {username}. "
        f"The user's current emotional tone is: {sentiment_label.upper()}. "
        "Adapt your response accordingly. Be extra empathetic if they are struggling. "
        "Keep responses concise, warm, and conversational. "
        f"Naturally suggest this tip if appropriate: '{suggestion}'. "
        f"CRITICAL LANGUAGE RULE: The user's message is written in {detected_lang}. "
        f"You MUST reply ONLY in {detected_lang}. "
        "Do NOT mix languages. Do NOT translate. Match the user's language exactly."
    )
    
    # 4. Use Groq if available
    if groq_client:
        history = load_history(username)[-10:]
        messages = [{"role": "system", "content": system_prompt}]
        for msg in history[:-1]:
            role = "user" if msg["sender"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["text"]})
        messages.append({"role": "user", "content": user_message})

        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=0.7
            )
            ai_reply = response.choices[0].message.content.strip()
            save_message("assistant", ai_reply, username)
            return ai_reply
        except Exception as e:
            print(f"[WARN] Groq failed: {e}. Falling back to Gemini.")
            
    # 5. Get model with system instruction (Fallback to Gemini)
    model = get_gemini_model(system_instruction=system_prompt)
        
    if not model:
        # Mock responses for offline mode
        mock_responses = [
            "I'm currently in offline mode, but I'm still here to listen. How else can I support you?",
            "I'm resting my AI brain right now, but feel free to keep sharing your thoughts.",
            "I've received your message! I'm here for you, even in my limited state."
        ]
        reply = random.choice(mock_responses)
        save_message("assistant", reply, username)
        return reply
        
        return reply
        
    # 6. Load Conversation Memory (last 10 messages)
    history = load_history(username)[-10:]
    
    # 7. Convert history to Gemini format
    chat_history = []
    # Gemini history shouldn't include the current message yet
    for msg in history[:-1]: 
        role = "user" if msg["sender"] == "user" else "model"
        chat_history.append({"role": role, "parts": [msg["text"]]})
    
    try:
        # Start a chat session with history
        chat = model.start_chat(history=chat_history)
        
        # Send message
        response = chat.send_message(user_message)
        ai_reply = response.text.strip()
        
        # Save the AI's reply to memory
        save_message("assistant", ai_reply, username)
        return ai_reply
        
    except Exception as e:
        reply = f"I'm sorry, I'm having a bit of trouble thinking right now. Could you try again? (Error: {str(e)})"
        save_message("assistant", reply, username)
        return reply

