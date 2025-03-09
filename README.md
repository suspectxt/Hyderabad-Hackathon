# GrowMore - AI-Powered Business Growth Platform

GrowMore is a comprehensive business management platform designed to help small businesses thrive with intelligent analytics, AI-powered marketing plans, inventory management, and content generation.

## 🚀 Features

- **Data Analytics**: Visualize key business metrics and track performance.
- **AI Marketing Plan Generation**: Get customized marketing strategies based on your business profile.
- **Inventory Management**: Monitor and optimize your stock levels.
- **Content Suggestions**: AI-powered content ideas for your social media and marketing channels.
- **User Registration & Authentication**: Secure account management.

## 🏗️ Architecture

GrowMore follows a modern multi-service architecture:

- **Frontend**: Built with React and styled using TailwindCSS.
- **Node.js Backend**: Express server for user management and API routing.
- **Python Backend**: FastAPI for AI-powered features and data processing.
- **Database**: Firebase/Firestore for data storage.
- **AI Integration**: GROQ API for intelligent content generation.

## ⚙️ Setup & Installation

### Prerequisites

Ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v14+)
- [Python](https://www.python.org/) (v3.8+)
- A Firebase account
- Access to the GROQ API

### Frontend Setup

```sh
cd frontend
npm install
npm run dev
```

### Node.js Backend Setup

```sh
cd backend
npm install
node server.js
```

### Python Backend Setup

```sh
cd ai-backend
pip install -r requirements.txt
uvicorn main:app --reload
```

## 🔐 Configuration

Before running the application, set up the following:

1. **Create a `.env` file** with your API keys:
   ```ini
   GROQ_API_KEY=your_groq_api_key
   FIREBASE_CONFIG=your_firebase_config
   ```

2. **Configure Firebase**:
   - Create a Firebase project.
   - Set up Firestore database.
   - Generate a service account key and store it securely.

## 📋 Usage

1. **Register** your business by providing a description and product list.
2. **Access the dashboard** to monitor analytics and inventory status.
3. **Generate AI-powered marketing plans** tailored to your business.
4. **Manage content strategies** for different marketing channels.
5. **Track key performance indicators (KPIs)** and business growth.
