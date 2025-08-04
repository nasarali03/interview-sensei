import os
import re
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGSMITH_API_KEY"]=os.getenv("LANGSMITH_API_KEY")
class InterviewQuestionGenerator:
    """
    Generates personalized interview questions and answers 
    based on job description and/or resume using Groq LLM.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be provided.")

        self.llm = ChatGroq(model="llama3-8b-8192", api_key=self.api_key,temperature=0.5)
        
        self.prompt = None
        self.llm_chain = None
        
    def is_irrelevant_input(self, text: str) -> bool:
        """
        Check if the input is irrelevant to interview preparation.
        """
        # Convert to lowercase for case-insensitive matching
        text_lower = text.lower().strip()
        
        # Patterns for irrelevant inputs
        irrelevant_patterns = [
            r'^hi\s*$',  # Just "hi"
            r'^hello\s*$',  # Just "hello"
            r'^hey\s*$',  # Just "hey"
            r'^thanks?\s*$',  # "thank you" or "thanks"
            r'^thank\s+you\s*$',  # "thank you"
            r'^gratitude\s*$',  # "gratitude"
            r'^bye\s*$',  # "bye"
            r'^goodbye\s*$',  # "goodbye"
            r'^how\s+are\s+you\s*\?*$',  # "how are you"
            r'^what\s+is\s+your\s+name\s*\?*$',  # "what is your name"
            r'^who\s+are\s+you\s*\?*$',  # "who are you"
            r'^what\s+can\s+you\s+do\s*\?*$',  # "what can you do"
            r'^help\s*$',  # "help"
            r'^\s*$',  # Empty or whitespace only
        ]
        
        for pattern in irrelevant_patterns:
            if re.match(pattern, text_lower):
                return True
        
        return False

    def get_irrelevant_response(self) -> str:
        """
        Return a short, helpful response for irrelevant inputs.
        """
        return """**I'm here to help you prepare for interviews!** 

This tool generates personalized interview questions based on job descriptions and resumes. To get started, please upload a job description document, paste a job description, or provide your resume details. I'll then create relevant interview questions tailored to your specific role and experience level.

**Tip:** For best results, include both the job description and your resume to get the most personalized questions."""
    
    def generate_questions(self, job_description: str = "", resume: str = "") -> str:
        # Check if the input is irrelevant
        combined_input = f"{job_description} {resume}".strip()
        if self.is_irrelevant_input(combined_input):
            return self.get_irrelevant_response()

        if not job_description.strip() and not resume.strip():
            return "Error: Please provide at least a job description or a resume."

        block_parts = []
        if job_description.strip():
            block_parts.append(f"Job Description:\n{job_description.strip()}")
        if resume.strip():
            block_parts.append(f"Resume:\n{resume.strip()}")

        document_block = "\n\n".join(block_parts)
        
        # Decide context label dynamically
        if job_description.strip() and resume.strip():
            context_label = "job description and resume"
        elif job_description.strip():
            context_label = "job description"
        elif resume.strip():
            context_label = "resume"
        else:
            context_label = "input"
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system","You are an expert hiring manager and technical interviewer."),
            ("human","""Your task is to generate 8-15 highly relevant, role-specific interview questions with detailed answers based on the following {context_label}.
            {document_block}

            IMPORTANT INSTRUCTIONS:
            1. Analyze the job role and generate questions specific to that position (e.g., Software Engineer, Data Scientist, Product Manager, etc.)
            2. For technical roles, include coding questions, algorithm problems, system design questions, and data structure problems
            3. For each question, provide a short descriptive answer (not just bullet points)
            4. For technical questions, include relevant code snippets (3-10 lines) in the answer
            5. Mix different types of questions: behavioral, technical, situational, and role-specific
            6. Ensure questions match the candidate's experience level and the job requirements

            FORMAT FOR EACH QUESTION:
            ## [Question Number]. [Question Title]
            
            **Question:** [Detailed question]
            
            **Answer:** [Comprehensive answer with explanations]
            
            **Code Example (if applicable):**
            ```[language]
            [Relevant code snippet]
            ```

            **Key Points:**
            - [Important point 1]
            - [Important point 2]
            - [Important point 3]

            Be precise, professional, and ensure the questions are challenging but appropriate for the role and experience level.""")
        ])
        
        self.llm_chain = self.prompt | self.llm | StrOutputParser()        
        
        try:
            response = self.llm_chain.invoke({"document_block": document_block,"context_label":context_label})
            return response
        except Exception as e:
            return f"An error occurred: {e}"

    def validate_document(self, text: str) -> bool:
        return bool(text and text.strip())

    def get_supported_document_types(self) -> list:
        return ["job description", "resume"]

# Optional CLI usage for testing
# if __name__ == '__main__':
#     generator = InterviewQuestionGenerator()
    
#     sample_resume = """
#     Nasar Ali, Software Engineer with 4+ years of experience in backend APIs and web development.
#     Proficient in Python, FastAPI, JavaScript, and DevOps tools like Docker, GitHub Actions.
#     """
#     sample_jd = """
#     We are hiring a backend engineer with expertise in Python and RESTful APIs.
#     Experience with FastAPI, containerization, and CI/CD pipelines is a must.
#     """

#     output = generator.generate_questions(job_description=sample_jd, resume=sample_resume)
#     print(output)
