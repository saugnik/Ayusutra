#!/usr/bin/env python3
"""
AyurSutra RAG Fine-tuning Service
Knowledge base and retrieval system for Panchakarma treatments using ChromaDB and Google Gemini.
"""

import os
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

import chromadb
from chromadb.config import Settings
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import numpy as np
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Initialize Gemini
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    logger.warning("Google API key not found. AI responses will use mock data.")
    model = None

# Initialize embedding model
try:
    embedding_model = SentenceTransformer(EMBEDDING_MODEL)
    logger.info(f"Loaded embedding model: {EMBEDDING_MODEL}")
except Exception as e:
    logger.error(f"Error loading embedding model: {e}")
    embedding_model = None

# Initialize ChromaDB
try:
    chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = chroma_client.get_or_create_collection(
        name="ayursutra_knowledge",
        metadata={"description": "AyurSutra Panchakarma Knowledge Base"}
    )
    logger.info("ChromaDB initialized successfully")
except Exception as e:
    logger.error(f"Error initializing ChromaDB: {e}")
    chroma_client = None
    collection = None

# FastAPI app
app = FastAPI(
    title="AyurSutra RAG Service",
    description="Retrieval-Augmented Generation service for Ayurveda and Panchakarma knowledge",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    query: str
    answer: Dict[str, Any]
    context: List[Dict[str, Any]]
    processing_time: float

class DocumentRequest(BaseModel):
    content: str
    title: str
    category: str
    metadata: Optional[Dict[str, Any]] = None

# Knowledge base data
AYURVEDA_KNOWLEDGE = [
    {
        "title": "Abhyanga Therapy",
        "content": "Abhyanga is a form of Ayurvedic medicine that involves massage of the body with large amounts of warm oil. The oil is often pre-medicated with herbs for specific conditions. It is one of the most important Panchakarma therapies. Benefits include improved circulation, stress relief, joint mobility, skin health, and detoxification. The therapy typically lasts 45-60 minutes and uses specific oils based on individual dosha constitution.",
        "category": "panchakarma",
        "metadata": {"dosha": "all", "duration": "45-60 minutes", "benefits": ["circulation", "stress_relief", "joint_mobility"]}
    },
    {
        "title": "Shirodhara Therapy",
        "content": "Shirodhara involves the continuous pouring of liquids over the forehead, specifically on the 'third eye'. The liquid used can be oil, milk, buttermilk, or even plain water. This therapy is excellent for stress, anxiety, depression, and various mental disorders. It balances the nervous system and promotes deep relaxation. Duration is typically 30-45 minutes.",
        "category": "panchakarma", 
        "metadata": {"dosha": "vata_pitta", "duration": "30-45 minutes", "benefits": ["stress_relief", "mental_balance", "nervous_system"]}
    },
    {
        "title": "Nasya Therapy",
        "content": "Nasya is the nasal administration of medicated oils, ghee, or herbal preparations. It is particularly effective for diseases of the head, neck, throat, and nervous system. Nasya cleanses the nasal passages and sinuses, improving breathing and mental clarity. It helps with headaches, sinusitis, allergies, and neurological conditions.",
        "category": "panchakarma",
        "metadata": {"dosha": "kapha_vata", "duration": "15-20 minutes", "benefits": ["respiratory_health", "mental_clarity", "sinus_relief"]}
    },
    {
        "title": "Virechana Therapy", 
        "content": "Virechana is therapeutic purgation using herbal medicines. It is one of the five main procedures of Panchakarma. This therapy eliminates excess Pitta dosha from the body through controlled purgation. It is effective for skin diseases, liver disorders, digestive issues, and inflammatory conditions. Proper preparation and post-treatment care are essential.",
        "category": "panchakarma",
        "metadata": {"dosha": "pitta", "duration": "1-3 days", "benefits": ["detoxification", "pitta_balance", "liver_health"]}
    },
    {
        "title": "Basti Therapy",
        "content": "Basti involves the introduction of medicated liquids including oils and decoctions in a liquid medium into the rectum. It is considered the most important of the five main procedures of Panchakarma, especially for Vata disorders. Types include Niruha Basti (decoction enema) and Anuvasana Basti (oil enema). It treats constipation, arthritis, neurological disorders, and reproductive issues.",
        "category": "panchakarma",
        "metadata": {"dosha": "vata", "duration": "varies", "benefits": ["vata_disorders", "digestive_health", "neurological_support"]}
    },
    {
        "title": "Vata Dosha",
        "content": "Vata is one of the three fundamental doshas in Ayurveda, composed of air and space elements. It governs movement, circulation, breathing, and nervous system functions. When balanced, Vata provides energy, creativity, and flexibility. When imbalanced, it causes anxiety, dryness, constipation, and joint pain. Vata types benefit from warm, oily, and grounding treatments.",
        "category": "ayurveda_fundamentals",
        "metadata": {"elements": ["air", "space"], "functions": ["movement", "circulation", "nervous_system"]}
    },
    {
        "title": "Pitta Dosha",
        "content": "Pitta dosha is composed of fire and water elements and governs metabolism, digestion, and transformation in the body. It controls body temperature, hunger, thirst, and intellectual capacity. Balanced Pitta provides good digestion, sharp intellect, and leadership qualities. Imbalanced Pitta causes anger, inflammation, skin problems, and digestive disorders. Pitta types need cooling and calming treatments.",
        "category": "ayurveda_fundamentals", 
        "metadata": {"elements": ["fire", "water"], "functions": ["digestion", "metabolism", "transformation"]}
    },
    {
        "title": "Kapha Dosha",
        "content": "Kapha dosha is made up of earth and water elements and provides structure, strength, and immunity to the body. It governs growth, lubrication of joints, and emotional stability. Balanced Kapha gives physical strength, immunity, and emotional stability. Imbalanced Kapha leads to weight gain, lethargy, congestion, and depression. Kapha types benefit from stimulating and warming treatments.",
        "category": "ayurveda_fundamentals",
        "metadata": {"elements": ["earth", "water"], "functions": ["structure", "immunity", "lubrication"]}
    },
    {
        "title": "Panchakarma Preparation",
        "content": "Proper preparation (Purvakarma) is essential before starting main Panchakarma procedures. This includes Pachana (digestive fire enhancement), Snehana (oleation therapy), and Swedana (sudation therapy). Pachana improves digestion with digestive herbs. Snehana involves internal and external oil application. Swedana uses steam therapy to open channels and prepare for detoxification.",
        "category": "panchakarma",
        "metadata": {"phases": ["pachana", "snehana", "swedana"], "importance": "preparation", "duration": "3-7 days"}
    },
    {
        "title": "Post-Panchakarma Care",
        "content": "Paschatkarma or post-treatment care is crucial for maintaining benefits of Panchakarma. It includes gradual return to normal diet, lifestyle modifications, and rejuvenation therapies. Samsarjana Krama involves systematic dietary progression from light to normal food. Rasayana therapy helps rebuild tissues and immunity. Proper rest, mild exercise, and stress management are essential.",
        "category": "panchakarma",
        "metadata": {"phases": ["samsarjana", "rasayana"], "importance": "integration", "duration": "1-2 weeks"}
    },
    {
        "title": "Ayurvedic Consultation Process",
        "content": "Ayurvedic consultation begins with detailed examination including pulse diagnosis (Nadi Pariksha), tongue examination, eye examination, and comprehensive health history. The practitioner assesses Prakriti (natural constitution), Vikriti (current imbalances), and Agni (digestive fire). Treatment plans are personalized based on individual constitution, current health status, lifestyle, and environmental factors.",
        "category": "consultation",
        "metadata": {"duration": "60-90 minutes", "includes": ["pulse_diagnosis", "constitution_assessment", "treatment_planning"], "frequency": "initial_detailed"}
    },
    {
        "title": "Ayurvedic Diet Guidelines",
        "content": "Ayurvedic nutrition emphasizes eating according to one's constitution and current imbalances. Vata types benefit from warm, moist, grounding foods. Pitta types need cooling, less spicy foods. Kapha types require light, warm, stimulating foods. The six tastes (sweet, sour, salty, bitter, pungent, astringent) should be balanced in each meal. Eating practices include mindful eating, proper food combinations, and eating at regular times.",
        "category": "lifestyle",
        "metadata": {"tastes": ["sweet", "sour", "salty", "bitter", "pungent", "astringent"], "principles": ["constitutional_eating", "food_combining", "mindful_eating"]}
    },
    {
        "title": "Yoga and Ayurveda Integration",
        "content": "Yoga and Ayurveda are sister sciences that complement each other perfectly. Yoga practices should be adapted to individual constitution. Vata types benefit from gentle, grounding practices. Pitta types need moderate, cooling practices. Kapha types require vigorous, energizing practices. Pranayama (breathing techniques) helps balance doshas and supports overall health. Regular practice enhances the effects of Ayurvedic treatments.",
        "category": "lifestyle",
        "metadata": {"practices": ["asana", "pranayama", "meditation"], "adaptation": "constitutional", "benefits": ["dosha_balance", "stress_relief", "flexibility"]}
    },
    {
        "title": "Seasonal Ayurvedic Routines",
        "content": "Ayurveda emphasizes living in harmony with seasonal cycles (Ritucharya). Spring requires detoxification and Kapha-pacifying practices. Summer needs cooling and Pitta-balancing approaches. Monsoon season requires gentle digestion support and Vata awareness. Autumn focuses on Vata pacification and grounding. Winter emphasizes nourishment and building strength. Seasonal adjustments in diet, lifestyle, and treatments optimize health.",
        "category": "lifestyle",
        "metadata": {"seasons": ["spring", "summer", "monsoon", "autumn", "winter"], "focus": ["seasonal_adaptation", "dosha_balancing", "natural_cycles"]}
    },
    {
        "title": "Ayurvedic Herbs and Medicines",
        "content": "Ayurvedic pharmacology uses single herbs (Dravyaguna) and classical formulations (Rasayana) for treatment. Common herbs include Ashwagandha for stress, Triphala for digestion, Brahmi for mental clarity, and Turmeric for inflammation. Medicines are prescribed based on individual constitution, current imbalances, and specific health conditions. Proper dosage, timing, and vehicle (Anupana) are crucial for effectiveness.",
        "category": "medicines",
        "metadata": {"types": ["single_herbs", "classical_formulations", "rasayana"], "common_herbs": ["ashwagandha", "triphala", "brahmi", "turmeric"], "factors": ["constitution", "dosage", "timing"]}
    }
]

async def initialize_knowledge_base():
    """Initialize the knowledge base with sample data"""
    if not collection or not embedding_model:
        logger.error("ChromaDB or embedding model not available")
        return False
    
    try:
        # Check if collection already has data
        existing_count = collection.count()
        if existing_count > 0:
            logger.info(f"Knowledge base already initialized with {existing_count} documents")
            return True
        
        logger.info("Initializing knowledge base with sample data...")
        
        documents = []
        metadatas = []
        ids = []
        
        for i, item in enumerate(AYURVEDA_KNOWLEDGE):
            content = f"{item['title']}: {item['content']}"
            documents.append(content)
            
            # Clean metadata - ChromaDB only accepts simple values
            base_metadata = item.get("metadata", {})
            clean_metadata = {
                "title": item["title"],
                "category": item["category"],
                "timestamp": datetime.now().isoformat()
            }
            
            # Convert complex metadata to strings
            for key, value in base_metadata.items():
                if isinstance(value, list):
                    clean_metadata[key] = ", ".join(str(v) for v in value)
                elif isinstance(value, (str, int, float, bool)):
                    clean_metadata[key] = value
                else:
                    clean_metadata[key] = str(value)
            
            metadatas.append(clean_metadata)
            ids.append(f"doc_{i}")
        
        # Generate embeddings
        embeddings = embedding_model.encode(documents).tolist()
        
        # Add to ChromaDB
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings
        )
        
        logger.info(f"Successfully initialized knowledge base with {len(documents)} documents")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing knowledge base: {e}")
        return False

def generate_embedding(text: str) -> List[float]:
    """Generate embedding for given text"""
    if not embedding_model:
        logger.warning("Embedding model not available, using mock embedding")
        return [0.0] * 384  # Mock embedding for all-MiniLM-L6-v2 dimensions
    
    try:
        embedding = embedding_model.encode([text])[0]
        return embedding.tolist()
    except Exception as e:
        logger.error(f"Error generating embedding: {e}")
        return [0.0] * 384

def query_knowledge_base(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Query the knowledge base and return relevant documents"""
    if not collection:
        logger.error("ChromaDB collection not available")
        return []
    
    try:
        # Generate query embedding
        query_embedding = generate_embedding(query)
        
        # Query ChromaDB
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=min(top_k, 10)
        )
        
        context_documents = []
        
        if results and results['documents'] and results['documents'][0]:
            for i in range(len(results['documents'][0])):
                doc = {
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i] if results['metadatas'] and results['metadatas'][0] else {},
                    "similarity": float(1.0 - results['distances'][0][i]) if results['distances'] and results['distances'][0] else 0.0
                }
                context_documents.append(doc)
        
        return context_documents
    
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        return []

async def generate_ai_response(query: str, context: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate AI response using Google Gemini or mock response"""
    
    # Prepare context for AI
    context_text = "\n\n".join([doc["content"] for doc in context[:3]])
    
    if model:
        try:
            # Create prompt for Gemini
            prompt = f"""You are an expert Ayurveda practitioner specializing in Panchakarma treatments. 
            Answer the following question based on the provided context about Ayurveda and Panchakarma therapies.
            
            Context:
            {context_text}
            
            Question: {query}
            
            Please provide a comprehensive answer that includes:
            1. Direct answer to the question
            2. Relevant benefits and contraindications if applicable  
            3. Practical recommendations
            4. Any important safety considerations
            
            Answer in a clear, professional manner suitable for both patients and practitioners."""

            response = model.generate_content(prompt)
            
            answer_text = response.text
            confidence = "high"
            evidence = [doc["metadata"].get("title", "Unknown") for doc in context[:2]]
            
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            # Fallback to knowledge base response
            answer_text = generate_knowledge_based_response(query, context)
            confidence = "medium"
            evidence = [doc["metadata"].get("title", "Knowledge Base") for doc in context[:2]]
    else:
        # Knowledge base response when no API key
        answer_text = generate_knowledge_based_response(query, context)
        confidence = "high" if context else "medium"
        evidence = [doc["metadata"].get("title", "Knowledge Base") for doc in context[:2]]
    
    return {
        "text": answer_text,
        "confidence": confidence,
        "evidence": evidence,
        "timestamp": datetime.now().isoformat()
    }

def generate_knowledge_based_response(query: str, context: List[Dict[str, Any]]) -> str:
    """Generate response based on knowledge base context, not hardcoded answers"""
    
    if not context:
        return "I don't have specific information about your query in my current knowledge base. Please ask about Ayurveda treatments, Panchakarma procedures, or dosha-related topics for more detailed information."
    
    # Use the most relevant document from knowledge base
    primary_doc = context[0]
    content = primary_doc.get('content', '')
    metadata = primary_doc.get('metadata', {})
    
    # Extract the main content after the title
    if ': ' in content:
        title, main_content = content.split(': ', 1)
    else:
        title = metadata.get('title', 'Ayurveda Information')
        main_content = content
    
    # Build comprehensive response from knowledge base
    response_parts = []
    
    # Main information
    response_parts.append(main_content)
    
    # Add specific details from metadata if available
    if metadata:
        details = []
        
        if 'duration' in metadata:
            details.append(f"Duration: {metadata['duration']}")
        
        if 'dosha' in metadata:
            dosha_info = metadata['dosha']
            if dosha_info != 'all':
                details.append(f"Best for: {dosha_info.replace('_', ' and ').title()} dosha types")
            else:
                details.append("Suitable for all dosha types")
        
        if 'benefits' in metadata:
            benefits = metadata['benefits'].replace('_', ' ').title()
            details.append(f"Key benefits: {benefits}")
        
        if 'elements' in metadata:
            elements = metadata['elements'].title()
            details.append(f"Composed of: {elements} elements")
        
        if 'functions' in metadata:
            functions = metadata['functions'].replace('_', ' ').title()
            details.append(f"Primary functions: {functions}")
        
        if details:
            response_parts.append("\n\nAdditional Details:")
            for detail in details:
                response_parts.append(f"• {detail}")
    
    # Add information from secondary documents if available
    if len(context) > 1:
        related_info = []
        for doc in context[1:3]:  # Max 2 additional documents
            doc_title = doc.get('metadata', {}).get('title', 'Related Information')
            if doc_title and doc_title != title:
                related_info.append(doc_title)
        
        if related_info:
            response_parts.append(f"\n\nRelated topics you might find helpful: {', '.join(related_info)}")
    
    # Professional disclaimer
    response_parts.append("\n\nNote: This information is for educational purposes. Please consult with a qualified Ayurveda practitioner for personalized treatment recommendations.")
    
    return ''.join(response_parts)

# API Endpoints

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AyurSutra RAG Service is running",
        "version": "1.0.0",
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "chromadb": "connected" if collection else "disconnected",
        "embedding_model": "loaded" if embedding_model else "not_loaded",
        "knowledge_base_size": collection.count() if collection else 0,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/ask", response_model=QueryResponse)
async def ask_question(request: QueryRequest):
    """Ask a question to the AI assistant"""
    start_time = datetime.now()
    
    try:
        # Query knowledge base for relevant context
        context = query_knowledge_base(request.query, request.top_k)
        
        # Generate AI response
        answer = await generate_ai_response(request.query, context)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return QueryResponse(
            query=request.query,
            answer=answer,
            context=context,
            processing_time=processing_time
        )
    
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail="Error processing query")

@app.post("/add_document")
async def add_document(request: DocumentRequest):
    """Add a new document to the knowledge base"""
    if not collection or not embedding_model:
        raise HTTPException(status_code=503, detail="Service not available")
    
    try:
        # Generate embedding
        content = f"{request.title}: {request.content}"
        embedding = generate_embedding(content)
        
        # Add to ChromaDB
        doc_id = f"doc_{datetime.now().timestamp()}"
        metadata = {
            "title": request.title,
            "category": request.category,
            "timestamp": datetime.now().isoformat(),
            **(request.metadata or {})
        }
        
        collection.add(
            documents=[content],
            metadatas=[metadata],
            ids=[doc_id],
            embeddings=[embedding]
        )
        
        return {
            "message": "Document added successfully",
            "document_id": doc_id,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        raise HTTPException(status_code=500, detail="Error adding document")

@app.get("/search")
async def search_knowledge_base(query: str, limit: int = 10):
    """Search the knowledge base"""
    try:
        results = query_knowledge_base(query, limit)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        logger.error(f"Error searching knowledge base: {e}")
        raise HTTPException(status_code=500, detail="Error searching knowledge base")

@app.on_event("startup")
async def startup_event():
    """Initialize the service on startup"""
    logger.info("Starting AyurSutra RAG Service...")
    
    # Initialize knowledge base
    await initialize_knowledge_base()
    
    logger.info("AyurSutra RAG Service started successfully")

if __name__ == "__main__":
    uvicorn.run(
        "rag_finetune_service:app",
        host="0.0.0.0", 
        port=8000,
        reload=True,
        log_level="info"
    )
