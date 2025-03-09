const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const admin = require("firebase-admin");
const axios = require("axios"); // For making HTTP requests

// Initialize Express
const app = express();
app.use(cors());
app.use(bodyParser.json());

// Initialize Firebase Admin SDK
const serviceAccount = require("path/to/your/serviceAccountKey.json");

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore(); // Firestore instance

// Function to generate random inventory value
const generateRandomInventory = () => Math.floor(Math.random() * (10000 - 1 + 1)) + 1;

// 🔹 Registration API
app.post("/api/register", async (req, res) => {
    try {
        const { username, password, confirmPassword, companyName, companyDescription, products } = req.body;
        console.log("DATA RECEIVED:", { username, companyName, companyDescription, products });

        // Validate request body
        if (!username || !password || !confirmPassword || !companyName || !companyDescription) {
            return res.status(400).json({ success: false, message: "All fields are required" });
        }

        // Check if passwords match
        if (password !== confirmPassword) {
            return res.status(400).json({ success: false, message: "Passwords do not match" });
        }

        // Generate a clean document ID based on company name
        const cleanCompanyName = companyName.trim().toLowerCase().replace(/\s+/g, "-");

        const usersRef = db.collection("users");
        const companyDocRef = usersRef.doc(cleanCompanyName);

        // Ensure `products` is an array of strings
        const productList = Array.isArray(products) ? products : [];

        // Create inventory object with product names as keys
        const productsWithInventory = {};
        productList.forEach(productName => {
            productsWithInventory[productName] = generateRandomInventory();
        });

        // Store company data in Firestore
        await companyDocRef.set({
            username,
            password,  // 🔴 Storing password in plaintext (⚠️ Not recommended in production)
            companyDescription,
            products: productsWithInventory,
            createdAt: admin.firestore.FieldValue.serverTimestamp()
        });

        await axios.post("http://localhost:8000/api/onboarding", { 
            company_name: companyName, 
            company_description: companyDescription 
        });

        console.log(`✅ Successfully stored company with ID: ${cleanCompanyName}`);
        return res.status(200).json({ 
            success: true, 
            message: "Registration successful",
            companyName: cleanCompanyName 
        });

    } catch (error) {
        console.error("Registration error:", error);
        return res.status(500).json({ success: false, message: "Registration failed" });
    }
});


// 🔹 Content Suggestions API
app.post("/api/content_suggestions", async (req, res) => {
    try {
        const { companyName } = req.body;
        console.log("RECEIVED CONTENT SUGGESTIONS REQUEST:", { companyName });

        // Validate request body
        if (!companyName) {
            return res.status(400).json({ success: false, message: "Company name is required." });
        }

        // Forward request to another server
        const response = await axios.post("http://localhost:8000/api/content_suggestions", {
            company_name: companyName
        });

        // Parse the content suggestions from the response
        const contentSuggestions = response.data.content_suggestions;

        console.log(`✅ Successfully received content suggestions for ${companyName}`);
        console.log("CONTENT SUGGESTIONS:", contentSuggestions);
        res.json({ 
            success: true,
            contentSuggestions
        });

    } catch (error) {
        console.error("❌ Error during content suggestions:", error);
        res.status(500).json({ success: false, message: "Server error. Try again later." });
    }
});



// 🔹 Regeneration API for Marketing Plan
app.post("/api/regenerate-marketing-plan", async (req, res) => {
    try {
        const { companyName, userPrompt } = req.body;
        console.log("RECEIVED REGENERATION REQUEST:", { companyName, userPrompt });

        // Validate request body
        if (!companyName || !userPrompt) {
            return res.status(400).json({ success: false, message: "Company name and user prompt are required." });
        }

        // Generate a clean company name for Firestore
        const cleanCompanyName = companyName.trim().toLowerCase().replace(/\s+/g, "-");

        const usersRef = db.collection("users");
        const companyDocRef = usersRef.doc(cleanCompanyName);

        // Check if the company exists
        const existingCompany = await companyDocRef.get();
        if (!existingCompany.exists) {
            return res.status(404).json({ success: false, message: "Company not found." });
        }

        // Save user request under the company document in Firestore
        await companyDocRef.update({
            lastMarketingPrompt: userPrompt,
            lastUpdated: admin.firestore.FieldValue.serverTimestamp()
        });

        // Forward data to another server
        const response = await axios.post("http://localhost:8000/api/resubmit_marketing_plan", {
            company_name: companyName,
            user_prompt: userPrompt
        });

        console.log(`✅ Successfully forwarded request for ${companyName}`);
        res.json({ success: true, message: "Marketing plan request sent successfully!", response: response.data });

    } catch (error) {
        console.error("❌ Error during marketing plan regeneration:", error);
        res.status(500).json({ success: false, message: "Server error. Try again later." });
    }
});

// Start the server
const PORT = 4000;
app.listen(PORT, () => {
    console.log(`🚀 Server running on http://localhost:${PORT}`);
    console.log("✅ Registration & Marketing Plan APIs are ready!");
});
