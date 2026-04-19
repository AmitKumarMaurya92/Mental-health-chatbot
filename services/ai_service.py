import google.generativeai as genai
from config import GEMINI_API_KEYS
from services.sentiment_service import analyze_sentiment, get_sentiment_label
from services.safety_service import check_safety, get_emergency_response
from services.suggestion_service import get_suggestion_for_mood
from services.memory_service import load_history, save_message
from services.db_service import log_mood
import random

def get_gemini_model(system_instruction=None):
    """Configures and returns a Gemini model instance, skipping invalid/leaked keys."""
    preferred_models = [
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-1.0"
    ]
    
    for key in GEMINI_API_KEYS:
        try:
            genai.configure(api_key=key)
            available_models = [m.name for m in genai.list_models()]
            
            # Choose the first preferred model available on this key
            model_name = next((m for m in preferred_models if m in available_models), None)
            if not model_name:
                # Fall back to any Gemini model that supports text/chat generation
                for m in genai.list_models():
                    if m.name.startswith("gemini-") and any(
                        method in getattr(m, "supported_generation_methods", [])
                        for method in ["generateMessage", "generateContent", "chat"]
                    ):
                        model_name = m.name
                        break

            if not model_name:
                raise RuntimeError("No compatible Gemini model found for this API key.")

            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
            ]

            model = genai.GenerativeModel(
                model_name,
                system_instruction=system_instruction,
                safety_settings=safety_settings
            )
            return model
        except Exception as e:
            print(f"Skipping API key due to error: {e}")
            continue
    return None

def generate_response(user_message: str) -> str:
    """Sends a message to the Gemini API and returns the response, incorporating memory, safety and sentiment analysis."""
    
    # 0. Save the user's message to memory immediately
    save_message("user", user_message)

    # 1. Internal Safety Check (Keyword based for immediate crisis)
    if not check_safety(user_message):
        reply = get_emergency_response()
        save_message("assistant", reply)
        return reply
        
    # 2. Analyze sentiment and get suggestions
    sentiment_scores = analyze_sentiment(user_message)
    sentiment_label = get_sentiment_label(sentiment_scores['compound'])
    suggestion = get_suggestion_for_mood(sentiment_label)
    
    # 2.5 Log mood for tracking
    log_mood(sentiment_scores['compound'], sentiment_label)
    
    # 3. Build system prompt
    system_prompt = (
        "You are a gentle, supportive, and empathetic mental health companion. "
        f"The user's current emotional tone is: {sentiment_label.upper()}. "
        "Adapt your response accordingly. Be extra empathetic if they are struggling. "
        "Keep responses concise, warm, and conversational. "
        f"Naturally suggest this tip if appropriate: '{suggestion}'"
    )
    
    # 4. Get model with system instruction
    model = get_gemini_model(system_instruction=system_prompt)
        
    if not model:
        # Mock responses for offline mode
        mock_responses = [
            "I'm currently in offline mode, but I'm still here to listen. How else can I support you?",
            "I'm resting my AI brain right now, but feel free to keep sharing your thoughts.",
            "I've received your message! I'm here for you, even in my limited state."
        ]
        reply = random.choice(mock_responses)
        save_message("assistant", reply)
        return reply
        
    # 5. Load Conversation Memory (last 10 messages)
    history = load_history()[-10:]
    
    # 6. Convert history to Gemini format
    chat_history = []
    # Gemini history shouldn't include the current message yet
    for msg in history[:-1]: 
        role = "user" if msg["role"] == "user" else "model"
        chat_history.append({"role": role, "parts": [msg["content"]]})
    
    try:
        # Start a chat session with history
        chat = model.start_chat(history=chat_history)
        
        # Send message
        response = chat.send_message(user_message)
        ai_reply = response.text.strip()
        
        # Save the AI's reply to memory
        save_message("assistant", ai_reply)
        return ai_reply
        
    except Exception as e:
        reply = f"I'm sorry, I'm having a bit of trouble thinking right now. Could you try again? (Error: {str(e)})"
        save_message("assistant", reply)
        return reply

