import os
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class InterviewQuestionGenerator:
    """
    Generates personalized interview questions and answers 
    based on job description and/or resume using Groq LLM.
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY must be provided.")

        self.llm = ChatGroq(model="llama3-8b-8192", api_key=self.api_key)

        self.template = """
        You are an expert hiring manager and technical interviewer with deep knowledge of various job roles and industries.
        Your task is to generate 8-12 highly relevant, role-specific interview questions with detailed answers based on the provided job description and resume.

        {document_block}

        IMPORTANT INSTRUCTIONS:
        1. Analyze the job role and generate questions specific to that position (e.g., Software Engineer, Data Scientist, Product Manager, etc.)
        2. For technical roles, include coding questions, algorithm problems, system design questions, and data structure problems
        3. For each question, provide a comprehensive answer (not just bullet points)
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

        Be precise, professional, and ensure the questions are challenging but appropriate for the role and experience level.
        """

        self.prompt = PromptTemplate(
            input_variables=["document_block"],
            template=self.template
        )

        self.llm_chain = LLMChain(prompt=self.prompt, llm=self.llm)

    def generate_questions(self, job_description: str = "", resume: str = "") -> str:
        if not job_description.strip() and not resume.strip():
            return "Error: Please provide at least a job description or a resume."

        block_parts = []
        if job_description.strip():
            block_parts.append(f"Job Description:\n{job_description.strip()}")
        if resume.strip():
            block_parts.append(f"Resume:\n{resume.strip()}")

        document_block = "\n\n".join(block_parts)

        try:
            response = self.llm_chain.invoke({"document_block": document_block})
            return response['text']
        except Exception as e:
            return f"An error occurred: {e}"

    def validate_document(self, text: str) -> bool:
        return bool(text and text.strip())

    def get_supported_document_types(self) -> list:
        return ["job description", "resume"]

# # Optional CLI usage for testing
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
