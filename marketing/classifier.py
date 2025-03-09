from groq import Groq
import os
from dotenv import load_dotenv
import json
from typing import List, Dict
from utils.logger_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()

async def classify_marketing_channels(company_info: str) -> Dict:
    """
    Classify which marketing channels would be most effective for a company
    based on their information.
    
    Args:
        company_info (str): Information about the company
        
    Returns:
        Dict: Dictionary containing recommended marketing channels and explanations
    """
    logger.info(f"Starting marketing channel classification for company info: {company_info}")
    
    try:
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        logger.debug("Successfully initialized Groq client")
        
        system_prompt = """You are a marketing channel classifier expert. 
        Based on the company information provided, analyze and recommend the most effective marketing channels.
        Consider factors like:
        - Company type (B2B, B2C, etc.)
        - Target audience
        - Industry
        - Company size and resources
        - Business goals
        
        Return recommendations in the following JSON format (and ONLY this format, no additional text):
        {
            "recommended_channels": [
                {
                    "channel": "channel_name",
                    "priority": "high/medium/low",
                    "reason": "explanation why this channel is recommended"
                }
            ]
        }
        
        Available channels to consider:
        - LinkedIn
        - Instagram
        - Facebook
        - Twitter/X
        - TikTok
        - Email Marketing
        - WhatsApp Business
        - Phone Calls
        - SMS Marketing
        - YouTube
        - Google Ads
        - Content Marketing/Blog
        - Podcasts
        - Trade Shows
        - Direct Mail
        """
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": company_info
            }
        ]
        
        logger.debug("Sending request to Groq API")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        logger.debug(f"Received response from Groq: {response_text}")
        
        recommendations = json.loads(response_text)
        logger.info(f"Successfully classified marketing channels: {len(recommendations.get('recommended_channels', []))} channels found")
        
        return recommendations
        
    except json.JSONDecodeError as e:
        error_msg = f"Error parsing JSON response: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "recommended_channels": []
        }
    except Exception as e:
        error_msg = f"Error in channel classification: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "recommended_channels": []
        }
