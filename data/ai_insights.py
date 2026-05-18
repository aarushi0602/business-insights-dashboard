import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def generate_insights(kpis, regional_data, product_data):
    """Generate AI-powered business insights using Claude API"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        return "❌ ANTHROPIC_API_KEY not found in .env file. Add your key to proceed."
    
    client = anthropic.Anthropic(api_key=api_key)
    
    prompt = f"""You are a senior business analyst. Analyze this sales data and write 3-4 concise, 
    executive-level insights. Be specific with numbers. Sound like a McKinsey slide.

    KPIs:
    {kpis}

    Regional performance:
    {regional_data.to_string()}

    Top products:
    {product_data.to_string()}

    Write bullet-point insights. Start each with a bold region or product name. 
    Example format: "**North region** sales increased 18% QoQ while churn reduced by 7%."
    Keep it under 150 words total."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    except Exception as e:
        return f"⚠️ Error generating insights: {str(e)}"