from groq import Groq
import os
from dotenv import load_dotenv
from utils.logger_config import setup_logger

logger = setup_logger(__name__)
load_dotenv()

async def get_groq_response(user_input: str) -> str:
    """
    Send a prompt to Groq API and get the response
    
    Args:
        user_input (str): The user's input prompt
        
    Returns:
        str: The response from Groq
    """
    logger.info(f"Processing feature classification request")
    
    try:
        # Initialize the Groq client with API key
        client = Groq(api_key=os.environ["GROQ_API_KEY"])
        logger.debug("Successfully initialized Groq client")
        
        # Define system prompt
        system_prompt = """You are a smart feature classifier. 
        You will be provided with a company's info, eg, what they are, what they do, what they want to do, etc.
        Your Job is to select the most relevant features for the company.
        You will return a list of features in a json format.
        {
            "features": ["feature1", "feature2", "feature3"]
        }
        Actual features are:
            - marketing and content generation
            - sales manager for hardware
            - sales manager for software
            - inventory management
            - revenue management
            - customer support
            - engineering
            - warehouse management
            - accounting        
        """
        
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_input
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
        
        response = chat_completion.choices[0].message.content
        logger.debug(f"Received response from Groq: {response}")
        logger.info("Successfully processed feature classification")
        
        return response
        
    except Exception as e:
        error_msg = f"Error occurred while calling Groq API: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return error_msg