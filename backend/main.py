from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv
from backend.analyzer import ResumeAnalyzer
from backend.models import AnalysisResponse
from backend.job_fetcher import JobDescriptionGenerator
from typing import Optional
from contextlib import asynccontextmanager

# Load environment variables
load_dotenv()

# Global variables
db_client: Optional[AsyncIOMotorClient] = None
db = None
analyzer: ResumeAnalyzer = ResumeAnalyzer()
jd_generator: JobDescriptionGenerator = JobDescriptionGenerator()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "resume_analyzer")

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global db_client, db
    # Startup
    try:
        db_client = AsyncIOMotorClient(MONGODB_URL)
        db = db_client[DATABASE_NAME]
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
    except Exception as e:
        print(f"⚠️ MongoDB connection failed: {e}")
        print("⚠️ App will run without database persistence")
    
    yield
    
    # Shutdown
    if db_client is not None:
        db_client.close()
        print("✅ MongoDB connection closed")

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Advanced Resume Analysis using Machine Learning",
    version="1.0.0",
    lifespan=app_lifespan
)

# CORS Configuration
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://resume-analyser-gbp1.vercel.app",  # frontend URL
    "http://localhost:5173",  # local frontend (vite)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "AI Resume Analyzer API is running",
        "version": "1.0.0",
        "database": "connected" if db is not None else "not connected"
    }

@app.get("/job-roles")
async def get_available_roles():
    """Get list of available job role templates"""
    roles = jd_generator.get_available_roles()
    return {
        "success": True,
        "count": len(roles),
        "roles": sorted(roles)
    }

@app.post("/generate-jd")
async def generate_job_description(job_title: str = Form(...)):
    """Generate job description from job title"""
    try:
        jd = jd_generator.generate_job_description(job_title)
        return {
            "success": True,
            "job_title": job_title,
            "job_description": jd
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    file: UploadFile = File(..., description="Resume PDF file"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Main endpoint to analyze resume against job description
    
    Args:
        file: PDF resume file
        job_description: Job description text
        
    Returns:
        Analysis results with match score, keywords, and summary
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )
    
    # Validate file size (max 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size exceeds 5MB limit"
        )
    
    try:
        # Perform analysis
        result = analyzer.analyze(contents, job_description)
        
        # Save to database if connected
        analysis_id = None
        if db is not None:
            try:
                analysis_doc = {
                    "match_score": result["match_score"],
                    "missing_keywords": result["missing_keywords"],
                    "matched_keywords": result["matched_keywords"],
                    "summary": result["summary"],
                    "resume_filename": file.filename,
                    "job_description": job_description[:500],
                    "timestamp": datetime.utcnow()
                }
                
                insert_result = await db.analyses.insert_one(analysis_doc)
                analysis_id = str(insert_result.inserted_id)
            except Exception as db_error:
                print(f"Database save error: {db_error}")
        
        # Return response
        return AnalysisResponse(
            success=True,
            match_score=result["match_score"],
            missing_keywords=result["missing_keywords"],
            matched_keywords=result["matched_keywords"],
            summary=result["summary"],
            analysis_id=analysis_id
        )
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@app.get("/history")
async def get_analysis_history(limit: int = 10):
    """
    Retrieve analysis history from database
    
    Args:
        limit: Number of records to return (default: 10)
        
    Returns:
        List of past analyses
    """
    if db is None:
        raise HTTPException(
            status_code=503,
            detail="Database not connected"
        )
    
    try:
        cursor = db.analyses.find().sort("timestamp", -1).limit(limit)
        history = []
        
        async for doc in cursor:
            doc["_id"] = str(doc["_id"])
            history.append(doc)
        
        return {
            "success": True,
            "count": len(history),
            "data": history
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve history: {str(e)}"
        )

@app.delete("/history/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete a specific analysis record"""
    if db is None:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    try:
        from bson import ObjectId
        result = await db.analyses.delete_one({"_id": ObjectId(analysis_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {"success": True, "message": "Analysis deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)