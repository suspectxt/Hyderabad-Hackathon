from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn
from Onboarding import get_groq_response
from marketing.classifier import classify_marketing_channels
from marketing.plan_maker import create_marketing_plan, change_marketing_plan
import json
from utils.logger_config import setup_logger
from google.cloud import firestore
from inventory_alert import inventory_alert
logger = setup_logger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Business Management API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4000",
        "http://localhost:5173",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:4000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000"
    ],  # Specify your frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firestore client with credentials
db = firestore.Client.from_service_account_json('path/to/your/serviceAccountKey.json')

# Pydantic model for user onboarding data
class OnboardingRequest(BaseModel):
    company_name: str
    company_description: str

# Pydantic model for onboarding response
class OnboardingResponse(BaseModel):
    company_name: str
    message: str
    status: str
    recommended_features: List[str]
    marketing_channels: Dict
    marketing_plan: Dict

class MarketingPlanRequest(BaseModel):
    company_name: str
    user_prompt: str

class MarketingPlanResponse(BaseModel):
    company_name: str
    schedule_info: Dict
    plan: Optional[Dict] = None
    error: Optional[str] = None

class InventoryRequest(BaseModel):
    company_name: str
    change: str

class InventoryResponse(BaseModel):
    company_name: str
    alert: str
    reason: Optional[str] = None

class ContentSuggestionsRequest(BaseModel):
    company_name: str

class ContentSuggestionsResponse(BaseModel):
    content_suggestions: Dict

# Store users (in a real application, this would be a database)
users = {}

@app.post("/api/onboarding", response_model=OnboardingResponse)
async def start_onboarding(request: OnboardingRequest):
    try:
        logger.info(f"Starting onboarding process for company: {request.company_name}")
        
        # Create company info prompt
        company_info = f"""
        Company Name: {request.company_name or 'Not specified'}
        Company Description: {request.company_description or 'Not specified'}
        """
        
        logger.debug("Getting feature recommendations")
        groq_response = await get_groq_response(company_info)
        
        # Parse the JSON response for features
        try:
            features = json.loads(groq_response)
            recommended_features = features.get('features', [])
            logger.info(f"Found {len(recommended_features)} recommended features")
        except json.JSONDecodeError:
            logger.warning("Failed to parse feature recommendations")
            recommended_features = []
        
        logger.debug("Getting marketing channel recommendations")
        marketing_channels = await classify_marketing_channels(company_info)
        
        logger.debug("Creating marketing plan")
        marketing_plan = await create_marketing_plan(company_info, marketing_channels)
        
        response = OnboardingResponse(
            company_name=request.company_name,
            message="Onboarding successful",
            status="success",
            recommended_features=recommended_features,
            marketing_channels=marketing_channels,
            marketing_plan=marketing_plan
        )

        # Create the document first with set(), then update it
        doc_ref = db.collection('onboarding').document(request.company_name)
        doc_ref.set({})  # Initialize empty document
        doc_ref.update({
            'onboarding_data': {
                'features': recommended_features,
                'marketing_channels': marketing_channels,
                'marketing_plan': marketing_plan,
                'timestamp': firestore.SERVER_TIMESTAMP
            }
        })
        
        # Initialize inventory for products
        doc_snapshot = db.collection('users').document(request.company_name).get()
        if doc_snapshot.exists:
            logger.info("doc_snapshot")
            products_data = doc_snapshot.get('products')
            if products_data is None:
                products_data = {}
            
            # Check if products is a list (old format) and convert to dict if needed
            if isinstance(products_data, list):
                inventory = {product: random.randint(50, 200) for product in products_data}
                # Update the document with the new inventory format
                db.collection('users').document(request.company_name).update({
                    'products': inventory
                })
                logger.info(f"Initialized inventory for {len(inventory)} products")
            
        logger.info(f"Successfully completed onboarding for user {request.company_name}")
        return response

    except Exception as e:
        error_msg = f"Onboarding failed for company '{request.company_name}': {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=400, detail=error_msg)

@app.post("/api/resubmit_marketing_plan", response_model=MarketingPlanResponse)
async def resubmit_marketing_plan(request: MarketingPlanRequest):
    try:
        logger.info(f"Resubmitting marketing plan for company: {request.company_name}")
        company_name = request.company_name
        user_prompt = request.user_prompt
        
        # Get the company schedule from Firestore
        company_ref = db.collection('onboarding').document(company_name)
        company_doc = company_ref.get()
        
        if not company_doc.exists:
            logger.error(f"Company schedule not found for: {company_name}")
            raise HTTPException(status_code=404, detail="Company schedule not found")
            
        schedule_info = company_doc.to_dict()
        
        # Call the resubmit function with schedule from Firestore
        marketing_plan = await change_marketing_plan(schedule_info, user_prompt)
        
        # Update the marketing plan in Firestore
        company_ref.update({
            'marketing_plan': marketing_plan,
            'updated_at': firestore.SERVER_TIMESTAMP
        })
        
        response = MarketingPlanResponse(
            company_name=company_name,
            schedule_info=schedule_info,
            plan=marketing_plan,
            error=None
        )
        
        logger.info(f"Successfully resubmitted marketing plan for company {company_name}")
        return response
        
    except Exception as e:
        error_msg = f"Resubmission failed: {str(e)}"
        logger.error(
            error_msg,
            extra={
                'company_name': request.company_name,
                'error_type': type(e).__name__
            },
            exc_info=True
        )
        
        return MarketingPlanResponse(
            company_name=request.company_name,
            schedule_info={},
            plan=None,
            error=error_msg
        )
    

@app.post("/api/update_inventory", response_model=InventoryResponse)
async def update_inventory(request: InventoryRequest):
    try:
        db = firestore.Client.from_service_account_json('path/to/your/serviceAccountKey.json')
        company_name = request.company_name
        change = request.change
        date = "2022-10"
        
        # Get documents and immediately convert to dict
        monthly_sales_doc = db.collection('stats').document(company_name).collection('monthlySales').document(date).get()
        website_traffic_doc = db.collection('stats').document(company_name).collection('websiteTraffic').document(date).get()
        instagram_engagement_doc = db.collection('stats').document(company_name).collection('instagramEngagement').document(date).get()
        inventory_doc = db.collection('users').document(company_name).get()
        
        if not monthly_sales_doc.exists:
            raise HTTPException(status_code=404, detail="Monthly sales not found")
            
        # Convert documents to dictionaries
        monthly_sales = monthly_sales_doc.to_dict()
        website_traffic = website_traffic_doc.to_dict() if website_traffic_doc.exists else {"value": 0}
        instagram_engagement = instagram_engagement_doc.to_dict() if instagram_engagement_doc.exists else {"value": 0}
        inventory = inventory_doc.get('products') if inventory_doc.exists else {}
        
        # Log the actual data
        logger.info(f"Processing inventory update with data:")
        logger.info(f"Monthly sales: {monthly_sales}")
        logger.info(f"Website traffic: {website_traffic}")
        logger.info(f"Instagram engagement: {instagram_engagement}")
        logger.info(f"Current inventory: {inventory}")

        inventory_alert_getter = await inventory_alert(
            company_name=company_name,
            monthly_sales=monthly_sales.get('value', 0),
            website_traffic=website_traffic.get('value', 0),
            instagram_engagement=instagram_engagement.get('value', 0),
            inventory=inventory
        )

        return InventoryResponse(
            company_name=company_name,
            alert=inventory_alert_getter.get('alert'),
            reason=inventory_alert_getter.get('reason')
        )

    except Exception as e:
        error_msg = f"Inventory update failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        import traceback
        logger.error(f"Traceback:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.post("/api/content_suggestions", response_model=ContentSuggestionsResponse)
async def give_content_suggestions(request: ContentSuggestionsRequest):
    try:
        company_name = request.company_name
        
        company_ref = db.collection('onboarding').document(company_name)
        company_doc = company_ref.get()
        
        print("company_doc.to_dict()", company_doc.to_dict())
        return ContentSuggestionsResponse(
            content_suggestions=company_doc.to_dict()
        )
    except Exception as e:
        error_msg = f"Content suggestions failed: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise HTTPException(status_code=500, detail=error_msg)


@app.get("/")
async def root():
    return {"message": "Welcome to the Onboarding API"}

@app.get("/api/users/{user_id}")
async def get_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)