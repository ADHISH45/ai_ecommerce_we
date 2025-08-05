import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def get_ai_recommendation(user_input, product_titles):
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""You are an intelligent product assistant. Based on this query: "{user_input}", 
    recommend relevant products from this list: {product_titles}."""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
