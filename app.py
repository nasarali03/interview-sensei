# interview_api.py

import os
import tempfile
from typing import Optional
from fastapi import FastAPI, Form, File, UploadFile, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import PyPDF2
from docx import Document
import io
import os

# Import the generator class
from groq_llm import InterviewQuestionGenerator

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize the generator
generator = InterviewQuestionGenerator()

# Request schema
class InterviewRequest(BaseModel):
    job_description: str = ""
    resume: str = ""

class DocumentHelper:
    """
    Helper class for reading and processing uploaded documents.
    """
    
    @staticmethod
    async def read_document(file: UploadFile) -> str:
        """
        Read content from uploaded document file.
        
        Args:
            file (UploadFile): The uploaded file object
            
        Returns:
            str: Extracted text content from the document
            
        Raises:
            HTTPException: If file format is not supported or reading fails
        """
        try:
            # Get file extension
            file_extension = file.filename.split('.')[-1].lower() if file.filename else ''
            
            # Read file content
            content = await file.read()
            
            if file_extension == 'txt':
                return content.decode('utf-8')
            
            elif file_extension == 'pdf':
                return DocumentHelper._read_pdf(content)
            
            elif file_extension in ['docx', 'doc']:
                return DocumentHelper._read_docx(content)
            
            else:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Unsupported file format: {file_extension}. Supported formats: txt, pdf, docx, doc"
                )
                
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error reading document: {str(e)}"
            )
    
    @staticmethod
    def _read_pdf(content: bytes) -> str:
        """
        Extract text from PDF content.
        
        Args:
            content (bytes): PDF file content
            
        Returns:
            str: Extracted text from PDF
        """
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def _read_docx(content: bytes) -> str:
        """
        Extract text from DOCX content.
        
        Args:
            content (bytes): DOCX file content
            
        Returns:
            str: Extracted text from DOCX
        """
        try:
            doc = Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def validate_file_size(file: UploadFile, max_size_mb: int = 10) -> bool:
        """
        Validate file size.
        
        Args:
            file (UploadFile): The uploaded file
            max_size_mb (int): Maximum file size in MB
            
        Returns:
            bool: True if file size is valid
        """
        # Read file to get size
        content = file.file.read()
        file.file.seek(0)  # Reset file pointer
        
        size_mb = len(content) / (1024 * 1024)
        return size_mb <= max_size_mb

@app.post("/generate")
async def generate_interview_questions(request: InterviewRequest):
    """
    Generate interview questions from text input.
    """
    jd = request.job_description.strip()
    resume = request.resume.strip()
    result = generator.generate_questions(job_description=jd, resume=resume)
    return {"questions_and_answers": result}

@app.post("/upload-and-generate")
async def upload_and_generate(
    job_description_file: Optional[UploadFile] = File(None),
    resume_file: Optional[UploadFile] = File(None),
    job_description_text: Optional[str] = Form(""),
    resume_text: Optional[str] = Form("")
):
    """
    Upload documents and generate interview questions.
    Supports both file uploads and text input.
    """
    try:
        job_description = job_description_text.strip()
        resume = resume_text.strip()
        
        # Process uploaded files
        if job_description_file:
            if not DocumentHelper.validate_file_size(job_description_file):
                raise HTTPException(
                    status_code=400, 
                    detail="Job description file is too large. Maximum size is 10MB."
                )
            job_description = await DocumentHelper.read_document(job_description_file)
        
        if resume_file:
            if not DocumentHelper.validate_file_size(resume_file):
                raise HTTPException(
                    status_code=400, 
                    detail="Resume file is too large. Maximum size is 10MB."
                )
            resume = await DocumentHelper.read_document(resume_file)
        
        # Validate that at least one document is provided
        if not job_description and not resume:
            raise HTTPException(
                status_code=400,
                detail="Please provide at least a job description or resume (as text or file upload)."
            )
        
        # Generate questions
        result = generator.generate_questions(job_description=job_description, resume=resume)
        
        return {
            "questions_and_answers": result,
            "job_description_length": len(job_description),
            "resume_length": len(resume)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and extract text from a single document.
    """
    try:
        if not DocumentHelper.validate_file_size(file):
            raise HTTPException(
                status_code=400, 
                detail="File is too large. Maximum size is 10MB."
            )
        
        content = await DocumentHelper.read_document(file)
        
        return {
            "filename": file.filename,
            "content": content,
            "content_length": len(content)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Health check route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/supported-formats")
def get_supported_formats():
    """
    Get list of supported file formats.
    """
    return {
        "supported_formats": ["txt", "pdf", "docx", "doc"],
        "max_file_size_mb": 10
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
