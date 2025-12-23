import PyPDF2
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Tuple, List
import io

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords

class ResumeAnalyzer:
    """Advanced AI-powered Resume Analysis Engine"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),  # Unigrams and bigrams
            stop_words='english'
        )
    
    def extract_text_from_pdf(self, pdf_file: bytes) -> str:
        """
        Extracts text from PDF using PyPDF2
        
        Args:
            pdf_file: PDF file as bytes
            
        Returns:
            Extracted text as string
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + " "
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error extracting PDF text: {str(e)}")
    
    def preprocess_text(self, text: str) -> str:
        """
        Cleans and normalizes text
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s+#]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def extract_keywords(self, text: str, top_n: int = 30) -> List[str]:
        """
        Extracts important keywords using TF-IDF
        
        Args:
            text: Input text
            top_n: Number of top keywords to extract
            
        Returns:
            List of keywords
        """
        # Fit vectorizer and get feature names
        tfidf_matrix = self.vectorizer.fit_transform([text])
        feature_names = self.vectorizer.get_feature_names_out()
        
        # Get TF-IDF scores
        scores = tfidf_matrix.toarray()[0]
        
        # Sort by score and get top keywords
        top_indices = scores.argsort()[-top_n:][::-1]
        keywords = [feature_names[i] for i in top_indices if scores[i] > 0]
        
        return keywords
    
    def calculate_match_score(self, resume_text: str, jd_text: str) -> Tuple[float, List[str], List[str]]:
        """
        Calculates cosine similarity between resume and job description
        
        Args:
            resume_text: Resume text
            jd_text: Job description text
            
        Returns:
            Tuple of (match_score, missing_keywords, matched_keywords)
        """
        # Preprocess texts
        resume_clean = self.preprocess_text(resume_text)
        jd_clean = self.preprocess_text(jd_text)
        
        # Calculate cosine similarity
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        # Convert to percentage
        match_score = round(similarity * 100, 2)
        
        # Extract keywords from both texts
        resume_keywords = set(self.extract_keywords(resume_clean, top_n=40))
        jd_keywords = set(self.extract_keywords(jd_clean, top_n=40))
        
        # Find matched and missing keywords
        matched = list(resume_keywords.intersection(jd_keywords))
        missing = list(jd_keywords - resume_keywords)
        
        return match_score, missing[:15], matched[:15]  # Limit for display
    
    def generate_summary(self, match_score: float, missing_count: int) -> str:
        """
        Generates human-readable summary based on match score
        
        Args:
            match_score: Match percentage
            missing_count: Number of missing keywords
            
        Returns:
            Summary string
        """
        if match_score >= 80:
            return f"🎯 Excellent Match! Your resume aligns strongly with the job requirements. Only {missing_count} skills to enhance."
        elif match_score >= 60:
            return f"✅ Good Match! Your resume shows solid alignment. Consider adding {missing_count} missing skills to strengthen your application."
        elif match_score >= 40:
            return f"⚠️ Moderate Match. Your resume has some relevant skills, but {missing_count} key skills are missing. Tailor your resume further."
        else:
            return f"❌ Low Match. Significant gaps detected. {missing_count} critical skills are missing. Consider gaining more relevant experience."
    
    def analyze(self, pdf_file: bytes, job_description: str) -> dict:
        """
        Main analysis function - orchestrates the entire process
        
        Args:
            pdf_file: PDF file as bytes
            job_description: Job description text
            
        Returns:
            Dictionary with analysis results
        """
        # Extract text from PDF
        resume_text = self.extract_text_from_pdf(pdf_file)
        
        if not resume_text or len(resume_text) < 50:
            raise ValueError("Could not extract sufficient text from PDF. Ensure it's a valid text-based PDF.")
        
        if not job_description or len(job_description) < 20:
            raise ValueError("Job description is too short. Please provide a detailed job description.")
        
        # Calculate match score and keywords
        match_score, missing_keywords, matched_keywords = self.calculate_match_score(
            resume_text, 
            job_description
        )
        
        # Generate summary
        summary = self.generate_summary(match_score, len(missing_keywords))
        
        return {
            "match_score": match_score,
            "missing_keywords": missing_keywords,
            "matched_keywords": matched_keywords,
            "summary": summary
        }