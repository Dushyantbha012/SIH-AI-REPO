import os
from dotenv import load_dotenv
from groq import Groq
import PyPDF2
import json

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def extract_text_from_pdf(pdf_path):
    """
    Extract text content from a PDF file.
    """
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def analyze_resume_and_generate_assignment(resume_text, job_description):
    """
    Generate an assessment based on the given resume and job description.
    """
    prompt = f"""
    Take the context of the following resume and job description:

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Create:
    A well formatted assessment - keep it standardized and professional.
    1. 10 aptitude questions covering logical reasoning, verbal ability, and quantitative aptitude. - give 4 options for each question.
    2. 2 programming questions with a maximum difficulty of LeetCode medium, to be completed in 90 minutes.
    3. Development assessment based on the job description and resume.

    Don't give the answers to the questions.

    Specify a submission window of 16 hours from the time candidates view the development assessment.  
    Close with asking to email the answers to sihdemo012@gmail.com.
    """

    try:
        # Make the API call
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert in analyzing resumes and creating personalized assessments for hiring purposes."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=1000
        )

        # Extract and return the raw response
        content = response.choices[0].message.content
        # print("Raw API response:", content)  # Debug print for raw response
        return content

    except Exception as e:
        print(f"Error in API call or JSON parsing: {e}")
        return None

def main():
    """
    Main function to extract resume data, load job description, and generate assessment.
    """
    # Path to the PDF resume
    pdf_path = "/Users/kabirarora/Desktop/Kabir_resume_oct.pdf"

    # Extract text from PDF
    resume_text = extract_text_from_pdf(pdf_path)

    # Load job description from a file
    with open('jobDescription.txt', 'r') as job_description_file:
        job_description = job_description_file.read()

    # Analyze resume and generate assignment
    result = analyze_resume_and_generate_assignment(resume_text, job_description)

    if result:
        print("Generated assessment:", result)
    else:
        print("Failed to generate assignment. Please check the error messages above.")

if __name__ == "__main__":
    main()
