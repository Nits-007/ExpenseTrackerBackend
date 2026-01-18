import os
from groq import Groq
import logging
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

logger = logging.getLogger(__name__)

API_KEY = os.getenv("AI_API_KEY")

client = Groq(api_key = API_KEY)

def generate_financial_insights(summary_data):
    prompt = f"""
        You are a personal finance assistant.

        Monthly spending summary:
        Total spent: {summary_data['total_spent']}
        Category-wise breakdown:
        {summary_data['category_breakdown']}

        Provide:
        1. A short spending summary
        2. Overspending warning (if any)
        3. One practical suggestion
        4. Roast me in a playful manner
        5. Give a funny joke
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"GROQ API FAILED: {str(e)}")
        return fallback_insights(summary_data)


def fallback_insights(summary_data):
    total = summary_data['total_spent']
    return (
        f"You spent {total} this month. Consider reviewing your top spending categories "
        "and setting monthly budgets to control expenses."
    )
