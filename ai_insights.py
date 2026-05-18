import os
from dotenv import load_dotenv

load_dotenv()

def generate_insights(kpis, regional_data, product_data):
    """Generate AI-powered business insights"""
    
    # Check for API keys
    google_key = os.getenv("GOOGLE_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    # Try Google Gemini first
    if google_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=google_key)
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""You are a senior business analyst. Analyze this sales data and write 3-4 concise, 
            executive-level insights. Be specific with numbers.

            KPIs:
            {kpis}

            Regional performance:
            {regional_data.to_string()}

            Top products:
            {product_data.to_string()}

            Write bullet-point insights. Start each with a bold region or product name. 
            Example format: "**North region** sales increased 18% QoQ while churn reduced by 7%."
            Keep it under 200 words total."""
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Google API Error: {e}")
    
    # Try Anthropic Claude
    if anthropic_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=anthropic_key)
            
            prompt = f"""You are a senior business analyst. Analyze this sales data and write 3-4 concise, 
            executive-level insights. Be specific with numbers.

            KPIs:
            {kpis}

            Regional performance:
            {regional_data.to_string()}

            Top products:
            {product_data.to_string()}

            Write bullet-point insights. Start each with a bold region or product name. 
            Example format: "**North region** sales increased 18% QoQ while churn reduced by 7%."
            Keep it under 200 words total."""
            
            message = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        except Exception as e:
            print(f"Anthropic API Error: {e}")
    
    # Return default insights if no API key
    return """### 📊 Default Business Insights

**To enable AI insights**, add an API key to your `.env` file:
- **Google Gemini** (FREE): `GOOGLE_API_KEY=your_key_here`
- **Anthropic Claude** (Paid): `ANTHROPIC_API_KEY=your_key_here`

#### Sample Insights:
- **North Region** demonstrates strongest performance with highest revenue contribution
- **Laptop Products** lead the portfolio with consistent sales momentum across all quarters
- **Customer Churn** shows seasonal patterns with opportunities for targeted retention campaigns
- **Q4 Performance** indicates seasonal growth potential with strategic focus on high-value regions
"""