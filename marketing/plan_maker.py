from groq import Groq
import os
from dotenv import load_dotenv
import json
from typing import List, Dict
from get_current_trending_songs import get_current_trending_songs
from utils.logger_config import setup_logger
from datetime import datetime, timedelta
import groq  # Add this import

logger = setup_logger(__name__)
load_dotenv()

async def create_marketing_plan(company_info: str, marketing_channels: Dict) -> Dict:
    """
    Create a detailed marketing plan with schedules based on company info and classified channels.
    
    Args:
        company_info (str): Information about the company
        marketing_channels (Dict): Previously classified marketing channels and their priorities
        
    Returns:
        Dict: Dictionary containing the marketing plan with schedules and action items
    """
    logger.info(f"Creating marketing plan for company")
    
    try:
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # Simplify the system prompt to reduce JSON complexity
        system_prompt = """You are a marketing strategy expert. Create a 90-day marketing plan based on the company information 
        and classified marketing channels provided. Return only valid JSON in this exact format:
        {
            "plan_overview": {
                "duration_days": 90,
                "start_date": "YYYY-MM-DD",
                "primary_goals": []
            },
            "phases": [{
                "phase": "",
                "duration_days": 0,
                "start_day": 0,
                "end_day": 0,
                "description": "",
                "objectives": []
            }],
            "channel_schedules": [{
                "channel": "",
                "priority": "",
                "frequency": "",
                "best_posting_times": [],
                "content_types": [],
                "weekly_schedule": null
            }],
            "resource_allocation": {
                "budget_distribution": {},
                "team_requirements": {}
            },
            "kpis": [{
                "metric": "",
                "target": "",
                "measurement_frequency": ""
            }]
        }
        In content_types, suggest the exact things the user has to do, it could be a reel with the script or an instagram post with some caption and hashtags (decided by you) or anything else that you think is relevant. If songs are relevant then highlight which one and the content for it"""
        
        # Get trending songs first
        try:
            trending_songs = get_current_trending_songs()
            if not trending_songs:  # If empty list returned
                trending_songs = ["No trending songs available"]
            trending_songs_str = json.dumps(trending_songs)
        except Exception as e:
            logger.error(f"Error getting trending songs: {e}")
            trending_songs_str = json.dumps(["Error getting trending songs"])
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""Based on this information, create a marketing plan:

Company Information: {company_info}

Marketing Channels: {json.dumps(marketing_channels, indent=2)}

Important: 
1. Use only valid JSON format
2. Use null for any non-applicable fields
3. All string values must be properly escaped
4. All arrays must be properly formatted with square brackets
5. All objects must be properly formatted with curly braces
6. If Instagram is selected as a channel, include content suggestions using these trending songs: {trending_songs_str}"""
            }
        ]
        
        logger.debug("Sending request to Groq API for marketing plan generation")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.5,  # Reduced temperature for more consistent output
            max_tokens=4096,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        logger.debug("Received marketing plan from Groq")
        
        try:
            # First validate the JSON structure
            marketing_plan = json.loads(response_text)
            
            # Add metadata
            marketing_plan["generated_at"] = datetime.now().isoformat()
            marketing_plan["plan_version"] = "1.0"
            
            logger.info("Successfully created marketing plan")
            return marketing_plan
            
        except json.JSONDecodeError as json_err:
            logger.error(f"JSON parsing error: {str(json_err)}")
            logger.debug(f"Problematic response: {response_text}")
            return {
                "error": "Invalid JSON format in response",
                "plan": None,
                "details": str(json_err)
            }
            
    except groq.BadRequestError as e:
        error_msg = f"Groq API error: {str(e)}"
        logger.error(error_msg)
        return {
            "error": error_msg,
            "plan": None
        }
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            "error": error_msg,
            "plan": None
        }

async def change_marketing_plan(schedule_info: Dict, user_prompt: str) -> Dict:
    """
    Resubmit the marketing plan to Groq API for resubmission
    
    Args:
        schedule_info (Dict): Information about the company
        user_prompt (str): User prompt for the new marketing plan
        
    Returns:
        Dict: Dictionary containing the marketing plan with schedules and action items
    """
    try:
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        
        # Clean the schedule_info to ensure JSON serialization
        cleaned_schedule = {
            "marketing_channels": schedule_info.get("marketing_channels", {}),
            "company_description": schedule_info.get("company_description", ""),
            "company_name": schedule_info.get("company_name", ""),
            "current_plan": schedule_info.get("marketing_plan", {}).get("plan", {})
        }
        
        system_prompt = """You are a marketing strategy expert. Updating a marketing plan based on the company information 
        and user request. Make the changes to the plan dynamically as asked by the user. If the user request is to remove something then remove it from the entire plan. 
        If the user request is to add something then add it to the plan. If the user request is to change something then change it in the plan.
        Basically do exactly what the user asks for and dont dumbly return the same schedule with no change.
        and return only valid JSON in this exact format:
        {
            "plan_overview": {
                "duration_days": 90,
                "start_date": "YYYY-MM-DD",
                "primary_goals": []
            },
            "phases": [{
                "phase": "",
                "duration_days": 0,
                "start_day": 0,
                "end_day": 0,
                "description": "",
                "objectives": []
            }],
            "channel_schedules": [{
                "channel": "",
                "priority": "",
                "frequency": "",
                "best_posting_times": [],
                "content_types": [],
                "weekly_schedule": {}
            }],
            "resource_allocation": {
                "budget_distribution": {},
                "team_requirements": {}
            },
            "kpis": [{
                "metric": "",
                "target": "",
                "measurement_frequency": ""
            }]
        }"""
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
                Current Company Info: {json.dumps(cleaned_schedule, default=str)}
                User Request: {user_prompt}
                
                Important:
                1. Maintain the exact JSON structure
                2. Use empty arrays [] for lists with no items
                3. Use empty objects {{}} for empty weekly_schedule
                4. All dates must be in YYYY-MM-DD format
                5. Do not include any datetime objects
                """
            }
        ]
        
        logger.debug("Sending request to Groq API for marketing plan update")
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="mixtral-8x7b-32768",
            temperature=0.3,
            max_tokens=10000,
            response_format={"type": "json_object"}
        )
        
        response_text = chat_completion.choices[0].message.content
        
        try:
            marketing_plan = json.loads(response_text)
            marketing_plan["generated_at"] = datetime.now().isoformat()
            marketing_plan["plan_version"] = "1.0"
            
            logger.info("Successfully updated marketing plan")
            return marketing_plan
            
        except json.JSONDecodeError as json_err:
            logger.error(
                "JSON parsing error in marketing plan update",
                extra={
                    'error': str(json_err),
                    'response': response_text[:500]
                }
            )
            return {
                "error": "Invalid JSON format in response",
                "plan": None
            }
            
    except Exception as e:
        error_msg = f"Error updating marketing plan: {str(e)}"
        logger.error(
            error_msg,
            extra={'error_type': type(e).__name__},
            exc_info=True
        )
        return {
            "error": error_msg,
            "plan": None
        }