from fastapi import logger
from groq import Groq
from dotenv import load_dotenv
import json
import os

load_dotenv()

async def inventory_alert(
    company_name: str,
    monthly_sales: int,
    website_traffic: int,
    instagram_engagement: int,
    inventory: dict
):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    prompt = f"""You are an inventory management expert. Analyze the following metrics and determine if inventory levels need attention:

Company: {company_name}
Monthly Sales: {monthly_sales}
Website Traffic: {website_traffic}
Instagram Engagement: {instagram_engagement}
Current Inventory Levels: {json.dumps(inventory, indent=2)}

Return a JSON response with the following structure:
{{
    "alert": "high" if inventory needs attention, "low" if inventory levels are fine,
    "reason": "detailed explanation of the recommendation"
}}
"""

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )

    try:
        response_json = json.loads(response.choices[0].message.content)
        print(f"Inventory alert response: {response_json}")
        return response_json
    except json.JSONDecodeError as e:
        print(f"Failed to parse inventory alert response: {e}")
        return {
            "alert": "error",
            "reason": "Failed to analyze inventory levels"
        }